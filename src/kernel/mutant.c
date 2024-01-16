#include <stddef.h>
#include <asm-generic/errno.h>
#include <asm-generic/errno-base.h>
#include "protocol/mimic.h"
#include <net/tcp.h>
#include <linux/string.h>  // Include this line to provide declaration for strlen


#define NETLINK_USER 25
#define MAX_RETRY 5
#define MAX_PAYLOAD 256 /* maximum payload size*/

// Communication Flags
#define COMM_END 0
#define COMM_BEGIN 1
#define COMM_SELECT_ARM 2
#define COMM_TEST_NATIVE_PROT 3

// Netlink comm variables
static struct sock *socket = NULL;
struct sock *nl_sk = NULL;
static u32 socketId = -1;
static u32 selectedProtocolId = 0;
static struct mutant *tcpMutant = NULL;
 

// Netlink comm APIs
static void sendMessageToApplicationLayer(char *message, int socketId)
{
    int retryCounter = 0;
    int messageSize;
    int messageSentReponseCode;
    struct sk_buff *socketMessage;
    struct nlmsghdr *reply_nlh = NULL;

    if (socketId == -1)
    {
        return;
    }

    messageSize = strlen(message);

    socketMessage = nlmsg_new(messageSize, 0);

    if (!socketMessage)
    {
        printk(KERN_ERR "mimic | %s: Failed to allocate new skb | (PID = %d)\n", __FUNCTION__, socketId);
        return;
    }

    reply_nlh = nlmsg_put(socketMessage, 0, 0, NLMSG_DONE, messageSize, 0);

    NETLINK_CB(socketMessage).dst_group = 0; /* not in mcast group */

    strncpy(NLMSG_DATA(reply_nlh), message, messageSize);

    messageSentReponseCode = nlmsg_unicast(nl_sk, socketMessage, socketId);
}

static void onConnectionStarted(struct nlmsghdr *nlh)
{
	printk(KERN_INFO "User-kernel communication initialized");
    char message[MAX_PAYLOAD - 1];

    socketId = nlh->nlmsg_pid;

    // Inform application layer of the number of protocols available
    sendMessageToApplicationLayer(message, socketId);
}

static void onMessageReceivedFromApplicationLayer(struct sk_buff *skb)
{
    struct nlmsghdr *nlh = NULL;

    if (skb == NULL)
    {
        printk(KERN_ERR "mimic | %s: skb is NULL\n", __FUNCTION__);
        return;
    }

    nlh = (struct nlmsghdr *)skb->data;

    switch (nlh->nlmsg_flags)
    {
    case COMM_END:
        socketId = -1;
        break;

    case COMM_BEGIN:
        onConnectionStarted(nlh);
        break;

    // TODO: replace protocol selection with cwnd 
    case COMM_SELECT_ARM:
        selectedProtocolId = nlh->nlmsg_seq;
        break;

    case 3: // = 3 if testing
        break;
    }
}


// static void onStartSingleProtocol(struct nlmsghdr *nlh)
// {
// 	printk(KERN_INFO "MODE SINGLE PROTOCOL ON: User-kernel communication initialized");
// 	char message[MAX_PAYLOAD - 1];

// 	socketId = nlh->nlmsg_pid;

// 	snprintf(message, MAX_PAYLOAD - 1, "%u;%s", 1, INIT_MSG);
//     sendMessageToApplicationLayer(message, socketId);

// }

/**
 * @brief Handles incoming messages from the application layer
 * 
 * @param skb 
 */
static void onMessageRecievedFromApplicationLayer(struct sk_buff *skb)
{
    struct nlmsghdr *nlh = NULL;

    if (skb == NULL)
    {
        printk(KERN_ERR "mimic | %s: skb is NULL\n", __FUNCTION__);
        return;
    }

    nlh = (struct nlmsghdr *)skb->data;
	// printk(KERN_INFO "received data");
    switch (nlh->nlmsg_flags)
    {
    case COMM_END:
        socketId = -1;
        break;

    case COMM_BEGIN:
        onConnectionStarted(nlh);
        break;

    case COMM_SELECT_ARM:
        selectedProtocolId = nlh->nlmsg_seq;
		// printk(KERN_INFO "protocol selected: %d", selectedProtocolId);
        break;

    default: // testing
		printk(KERN_INFO "Test message received!");
        break;
    }
}

/**
 * @brief Prepares and sends a response to the application layer after each acknowledgement
 * 
 * @param tp 
 * @param socketId 
 */
static void replyToApplicationLayer(struct tcp_sock *tp, int socketId, __u32 protocolId)
{
    // message vars
    char message[MAX_PAYLOAD - 1];

    __u32 cwnd = tp->snd_cwnd;
    __u32 rtt = tp->srtt_us;
    __u32 rtt_dev = tp->mdev_us;
	__u32 rtt_min = tcp_min_rtt(tp);
    __u16 MSS = tp->advmss;
    __u32 delivered = tp->delivered;
    __u32 lost = tp->lost_out;
    __u32 in_flight = tp->packets_out;
    __u32 retransmitted = tp->retrans_out;
    __u32 now = tcp_jiffies32;

    snprintf(message, MAX_PAYLOAD - 1, "%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u",
             now, cwnd, rtt, rtt_dev, rtt_min, MSS, delivered, lost,
             in_flight, retransmitted, protocolId);

    sendMessageToApplicationLayer(message, socketId);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


static void tcp_mutant_cong_avoid(struct sock *sk, __u32 ack, __u32 acked)
{
    __u32 cwnd_delta;
    
	struct tcp_sock *tp = tcp_sk(sk);
	tp->snd_cwnd += cwnd_delta;

}
EXPORT_SYMBOL_GPL(tcp_mutant_cong_avoid);

static void tcp_mutant_pkts_acked(struct sock *sk, const struct ack_sample *sample)
{
    const struct tcp_sock *tp = tcp_sk(sk);
    // reply vars
    char msg[MAX_PAYLOAD - 1];
    u32 cwnd = tp->snd_cwnd;
    u32 rtt = tp->srtt_us;
    u32 rtt_dev = tp->mdev_us;
    u16 MSS = tp->advmss;
    u32 delivered = tp->delivered;
    u32 lost = tp->lost_out;
    u32 in_flight = tp->packets_out;
    u32 retransmitted = tp->retrans_out;
    u32 now = tcp_jiffies32;

    snprintf(msg, MAX_PAYLOAD - 1, "%u;%u;%u;%u;%u;%u;%u;%u;%u;",
                now, cwnd, rtt, rtt_dev, MSS, delivered, lost,
                in_flight, retransmitted);
    sendMessageToApplicationLayer(msg, socketId);
}
EXPORT_SYMBOL_GPL(tcp_mutant_pkts_acked);


static struct tcp_congestion_ops tcp_mutant = {
    .ssthresh   = tcp_reno_ssthresh,
    .cong_avoid = tcp_mutant_cong_avoid,
    .undo_cwnd  = tcp_reno_undo_cwnd,
    .pkts_acked = tcp_mutant_pkts_acked,

    .owner = THIS_MODULE,
    .name = "mutant",
};

static int __init tcp_mutant_register(void)
{
    struct netlink_kernel_cfg cfg = {
            .input = onMessageReceivedFromApplicationLayer,
    };

    /* Initialize Netlink Socket */    
    socket = netlink_kernel_create(&init_net, NETLINK_USER, &cfg);

    if (socket == NULL)
    {
        printk(KERN_ERR "mimic | %s: Unable to create socket\n", __FUNCTION__);
        return -1;
    }

    BUILD_BUG_ON(sizeof(struct mutant) > ICSK_CA_PRIV_SIZE);
    tcp_register_congestion_control(&tcp_mutant);
    return 0;
}

static void __exit tcp_mutant_unregister(void)
{
    /* Release Netlink Socket */
    if (socket)
    {
        sock_release(socket->sk_socket);
    }

    tcp_unregister_congestion_control(&tcp_mutant);
}

module_init(tcp_mutant_register);
module_exit(tcp_mutant_unregister);

MODULE_AUTHOR("Lorenzo Pappone");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mutant");
MODULE_VERSION("1.0");