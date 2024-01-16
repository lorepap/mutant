#include <asm-generic/errno.h>
#include <asm-generic/errno-base.h>
#include <net/tcp.h>
// #include "protocol/cubic.h"
// #include "protocol/hybla.h"
// #include "protocol/bbr.h"
// #include "protocol/vegas.h"
// #include "protocol/pcc.h"

// #include "protocol/mutant.h"

#define NETLINK_USER 25
#define MAX_RETRY 5
#define MAX_PAYLOAD 256 /* maximum payload size*/

// Communication Flags
#define COMM_END 0
#define COMM_BEGIN 1
#define COMM_SELECT_ARM 2
#define TEST 3

// Netlink comm variables
struct sock *nl_sk = NULL;
static u32 socketId = -1;
static u32 selectedProtocolId = 0;

#define ARM_COUNT 2
// #define INIT_MSG "CUBIC;HYBLA;BBR;VEGAS;PCC"
#define INIT_MSG "cubic:0;reno:1"

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

    if (messageSentReponseCode < 0)
    {
        printk(KERN_ERR "mimic | %s: Error while sending message | (PID = %d) | (Error = %d) | (Count = %d)\n", __FUNCTION__, socketId, messageSentReponseCode, retryCounter);
    }
    else
    {
        printk("mimic | %s: Correctly sent message to app layer | PID = %d", __FUNCTION__, socketId);
    }
}

static void onConnectionStarted(struct nlmsghdr *nlh)
{
	printk(KERN_INFO "User-kernel communication initialized");
    char message[MAX_PAYLOAD - 1];

    socketId = nlh->nlmsg_pid;

    // Send application layer a message to inform that the connection has started
    snprintf(message, MAX_PAYLOAD - 1, "%u", 0);
    sendMessageToApplicationLayer(message, socketId);
}

static void onConnectionEnded(struct nlmsghdr *nlh)
{
    printk(KERN_INFO "User-kernel communication ended");
    char message[MAX_PAYLOAD - 1];

    socketId = -1;

    // Send application layer a message to inform that the connection has ended
    snprintf(message, MAX_PAYLOAD - 1, "%u", -1);
    sendMessageToApplicationLayer(message, socketId);
}


struct tcp_mutant_wrapper {
    struct tcp_congestion_ops *current_ops;
    // Additional state or control variables can be added here
};

static struct tcp_mutant_wrapper mutant_wrapper;
extern struct tcp_congestion_ops cubictcp; // reference to CUBIC ops
extern struct tcp_congestion_ops tcp_reno; // reference to CUBIC ops


// Swicthing congestion control function
void mutant_switch_congestion_control(u32 protocolId) {
    switch (protocolId)
    {
    case 0:
        printk(KERN_INFO "Switching to CUBIC");
        mutant_wrapper.current_ops = &cubictcp;
        break;
    case 1:
        printk(KERN_INFO "Switching to Reno");
        mutant_wrapper.current_ops = &tcp_reno;
        break;
    default:
        printk(KERN_INFO "Switching to default (CUBIC)");
        mutant_wrapper.current_ops = &cubictcp;
        break;
    }
}
    

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
        onConnectionEnded(nlh);
        socketId = -1;
        break;

    case COMM_BEGIN:
        onConnectionStarted(nlh);
        break;

    case COMM_SELECT_ARM:
        selectedProtocolId = nlh->nlmsg_seq;
        mutant_switch_congestion_control(selectedProtocolId);
        // wait for some time (TODO: forward the waiting time with the protocol ID)
        msleep(1000);
        // Send features to user module
        replyToApplicationLayer(tcp_sk(skb->sk), socketId, selectedProtocolId);      
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


static int __init netlink_init(void)
{
    struct netlink_kernel_cfg cfg = {
        .input = onMessageRecievedFromApplicationLayer,
    };

    nl_sk = netlink_kernel_create(&init_net, NETLINK_USER, &cfg);
    if (!nl_sk) {
        printk(KERN_ALERT "Error creating netlink socket.\n");
        return -10;
    }

    printk(KERN_INFO "Netlink socket created successfully.\n");
    return 0;
}

static void __exit netlink_exit(void)
{
    netlink_kernel_release(nl_sk);
    printk(KERN_INFO "Netlink socket released.\n");
}

//////////////////////////////////////////////////////////

static void mutant_tcp_init(struct sock *sk) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->init)
        mutant_wrapper.current_ops->init(sk);
}

static void mutant_tcp_cong_avoid(struct sock *sk, u32 ack, u32 acked) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->cong_avoid)
        mutant_wrapper.current_ops->cong_avoid(sk, ack, acked);
}

static u32 mutant_tcp_ssthresh(struct sock *sk) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->ssthresh)
        return mutant_wrapper.current_ops->ssthresh(sk);

    return TCP_INFINITE_SSTHRESH; // Default value in case of no function
}

static void mutant_tcp_set_state(struct sock *sk, u8 new_state) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->set_state)
        mutant_wrapper.current_ops->set_state(sk, new_state);
}

static u32 mutant_tcp_undo_cwnd(struct sock *sk) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->undo_cwnd)
        return mutant_wrapper.current_ops->undo_cwnd(sk);

    return tcp_sk(sk)->snd_cwnd; // Default behavior
}

static void mutant_tcp_cwnd_event(struct sock *sk, enum tcp_ca_event event) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->cwnd_event)
        mutant_wrapper.current_ops->cwnd_event(sk, event);
}

static void mutant_tcp_pkts_acked(struct sock *sk, const struct ack_sample *sample) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->pkts_acked)
        mutant_wrapper.current_ops->pkts_acked(sk, sample);
}


static struct tcp_congestion_ops mutant_cong_ops __read_mostly = {
    .init       = mutant_tcp_init,
    .ssthresh   = mutant_tcp_ssthresh,
    .cong_avoid = mutant_tcp_cong_avoid,
    .set_state  = mutant_tcp_set_state,
    .undo_cwnd  = mutant_tcp_undo_cwnd,
    .cwnd_event = mutant_tcp_cwnd_event,
    .pkts_acked = mutant_tcp_pkts_acked,
    .owner      = THIS_MODULE,
    .name       = "mutant",
};


static int __init mutant_tcp_module_init(void) {
    // Netlink init
    if (netlink_init() < 0) {
        pr_err("Netlink could not be initialized\n");
        return -EINVAL;
    }
    
    // Initial setup or default congestion control selection
    mutant_wrapper.current_ops = &cubictcp; // For example, defaulting to Reno

    // Register the custom congestion control
    if (tcp_register_congestion_control(&mutant_cong_ops) < 0) {
        pr_err("Mutant congestion control could not be registered\n");
        return -EINVAL;
    }

    return 0;
}

static void __exit mutant_tcp_module_exit(void) {
    tcp_unregister_congestion_control(&mutant_cong_ops);
}

module_init(mutant_tcp_module_init);
module_exit(mutant_tcp_module_exit);
MODULE_AUTHOR("Lorenzo Pappone");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mutant");
MODULE_VERSION("1.0");