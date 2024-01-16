// #include "all_headers.h"
#include <asm-generic/errno.h>
#include <asm-generic/errno-base.h>
#include "protocol/cubic.h"
// #include <stdlib.h>

#define NETLINK_USER 25
#define MAX_RETRY 5
#define MAX_PAYLOAD 256 /* maximum payload size*/

// Communication Flags
#define COMM_END 0
#define COMM_BEGIN 1
#define COMM_SELECT_ARM 2

// static struct sock *socket = NULL;
static __u32 socketId = -1;
static __u32 minCongestionWindow __read_mostly = 10;
static __u32 selectedProtocolId = 0; // cubic
static __u32 lastMinRTT = 0;
// static struct arm *tcpMimic = NULL; // global mimic struct with CC parameters

// cubic variable
// extern __u32 beta_scale __read_mostly;
// extern __u32 cube_rtt_scale __read_mostly;


//////////////////////// KERNEL-USER COMMUNICATION //////////////////////
// /**
//  * @brief Sends a message to the application layer via a socket
//  * 
//  * @param message - message to be sent
//  * @param socketId - socket id
//  */
// static void sendMessageToApplicationLayer(char *message, int socketId)
// {
//     int retryCounter = 0;
//     int messageSize;
//     int messageSentReponseCode;
//     struct sk_buff *socketMessage;
//     struct nlmsghdr *reply_nlh = NULL;

//     if (socketId == -1)
//     {
//         return;
//     }

//     messageSize = strlen(message);

//     socketMessage = nlmsg_new(messageSize, 0);

//     if (!socketMessage)
//     {
//         printk(KERN_ERR "mimic | %s: Failed to allocate new skb | (PID = %d)\n", __FUNCTION__, socketId);
//         return;
//     }

//     reply_nlh = nlmsg_put(socketMessage, 0, 0, NLMSG_DONE, messageSize, 0);

//     NETLINK_CB(socketMessage).dst_group = 0; /* not in mcast group */

//     strncpy(NLMSG_DATA(reply_nlh), message, messageSize);

//     messageSentReponseCode = nlmsg_unicast(socket, socketMessage, socketId);

//     if (messageSentReponseCode < 0)
//     {
//         printk(KERN_ERR "mimic | %s: Error while sending message | (PID = %d) | (Error = %d) | (Count = %d)\n", __FUNCTION__, socketId, messageSentReponseCode, retryCounter);
//     }
// }

// static void onConnectionStarted(struct nlmsghdr *nlh)
// {
//     char message[MAX_PAYLOAD - 1];

//     socketId = nlh->nlmsg_pid;

//     // Inform application layer of the number of protocols available
//     snprintf(message, MAX_PAYLOAD - 1, "%u;%s", ARM_COUNT, INIT_MSG);
//     sendMessageToApplicationLayer(message, socketId);
// }

// /**
//  * @brief Handles incoming messages from the application layer
//  * 
//  * @param skb 
//  */
// static void onMessageRecievedFromApplicationLayer(struct sk_buff *skb)
// {
//     struct nlmsghdr *nlh = NULL;

//     if (skb == NULL)
//     {
//         printk(KERN_ERR "mimic | %s: skb is NULL\n", __FUNCTION__);
//         return;
//     }

//     nlh = (struct nlmsghdr *)skb->data;

//     switch (nlh->nlmsg_flags)
//     {
//     case COMM_END:
//         socketId = -1;
//         break;

//     case COMM_BEGIN:
//         onConnectionStarted(nlh);
//         break;

//     case COMM_SELECT_ARM:
//         selectedProtocolId = nlh->nlmsg_seq;
//         // selectedProtocolId = ARM_VEGAS;
//         break;

//     case 3: // = 3 if testing
//         break;
//     }
// }

// /**
//  * @brief Prepares and sends a response to the application layer after each acknowledgement
//  * 
//  * @param tp 
//  * @param socketId 
//  */
// static void replyToApplicationLayer(struct tcp_sock *tp, int socketId, __u32 protocolId)
// {
//     // message vars
//     char message[MAX_PAYLOAD - 1];

//     __u32 cwnd = tp->snd_cwnd;
//     __u32 rtt = tp->srtt_us;
//     __u32 rtt_dev = tp->mdev_us;
//     __u16 MSS = tp->advmss;
//     __u32 delivered = tp->delivered;
//     __u32 lost = tp->lost_out;
//     __u32 in_flight = tp->packets_out;
//     __u32 retransmitted = tp->retrans_out;
//     __u32 now = tcp_jiffies32;

//     snprintf(message, MAX_PAYLOAD - 1, "%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;",
//              now, cwnd, rtt, rtt_dev, MSS, delivered, lost,
//              in_flight, retransmitted, protocolId);

//     sendMessageToApplicationLayer(message, socketId);
// }
////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * @brief Handles logic after a packet is acknowledged, like replying to application layer
 * 
 * @param sk 
 * @param sample 
 */
static void onPacketsAcked(struct sock *sk, const struct ack_sample *sample)
{
    // struct tcp_sock *tp = tcp_sk(sk);

    // if (tcpMimic == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }

    // @TODO : uncomment this when it will be needed
    // replyToApplicationLayer(tp, socketId, selectedProtocolId);

    // doPacketsAcked(sk, sample, selectedProtocolId);
    bictcp_acked(sk, sample);
}

// static __u32 onSsthresh(struct sock *sk){

//     struct tcp_sock *tp = tcp_sk(sk);

//     if (tcpMimic == NULL)
//     {
//         printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
//         tcpMimic = to_arm(sk);
//     }

//     return mimicSsthresh(sk, selectedProtocolId);

// }

static __u32 onUndoCwnd(struct sock *sk){

    // struct tcp_sock *tp = tcp_sk(sk);

    // if (tcpMimic == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }

    // return mimicUndoCwnd(sk, selectedProtocolId);
    return tcp_reno_undo_cwnd(sk);
}

static void onAvoidCongestion(struct sock *sk, __u32 ack, __u32 acked){

    // if (tcpMimic == NULL)
    // { 
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }

    // mimicCongAvoid(sk, ack, acked, selectedProtocolId);
    bictcp_cong_avoid(sk, ack, acked);
}


static void onCongestionEvent(struct sock *sk, enum tcp_ca_event event)
{

    // if (tcpMimic == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }
   
    // mimicCongestionEvent(sk, event, selectedProtocolId);
     bictcp_cwnd_event(sk, event);

}

static void onInit(struct sock *sk)
{
    // if (tcpMimic == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }

    // doInit(sk, selectedProtocolId);
    bictcp_init(sk);
}

// static void onCongControl(struct sock *sk, const struct rate_sample *rs){
     
//      if (tcpMimic == NULL)
//     {
//         printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
//         tcpMimic = to_arm(sk);
//     }

//     mimicMain(sk, rs, selectedProtocolId);
// }

static void onSetState (struct sock *sk, __u8 new_state){

    // if (tcpMimic == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: tcpMimic is null\n", __FUNCTION__);
    //     tcpMimic = to_arm(sk);
    // }

    // mimicState(sk, new_state);
    bictcp_state(sk, new_state);
}

// static __u32 onSndbufExpand(struct sock *sk){
//    return mimicSndbufExpand(sk);
// }

static __u32 mimicRecalcSshthresh(struct sock *sk){
    // return mimicSsthresh(sk, selectedProtocolId);
    return bictcp_recalc_ssthresh(sk);
}

static struct tcp_congestion_ops tcp_mimic __read_mostly = {
    .init = onInit,
    .pkts_acked = onPacketsAcked,
    .undo_cwnd = onUndoCwnd,
    .undo_cwnd = tcp_reno_undo_cwnd,
    .ssthresh = mimicRecalcSshthresh,
    // .ssthresh = tcp_reno_ssthresh,
    .cong_avoid = onAvoidCongestion,
    .cwnd_event = onCongestionEvent, // only defined in cubic
	// .cong_control	= onCongControl,   // only defined in BBR
	// .sndbuf_expand	= onSndbufExpand, // only defined in BBR
	// .ssthresh	= onSsthresh,
	// // .min_tso_segs	= bbr_min_tso_segs, // only defined in BBR
	// // .get_info	= bbr_get_info, // only defined in BBR
	.set_state	= onSetState,
    .owner = THIS_MODULE,
    .name = "mimic"
};

static int __init onRegister(void)
{
    // struct netlink_kernel_cfg cfg = {
    //     .input = onMessageRecievedFromApplicationLayer,
    // };

    // /* Initialize Netlink Socket */
    // socket = netlink_kernel_create(&init_net, NETLINK_USER, &cfg);

    // if (socket == NULL)
    // {
    //     printk(KERN_ERR "mimic | %s: Unable to create socket\n", __FUNCTION__);
    //     return -1;
    // }

    // @todo check if there is any consequence by commenting this line
    // it throws an exception because struct arm is bigger than ICSK_CA_PRIV_SIZE
    // modify ICSK_CA_PRIV_SIZE in /usr/src/$(uname -r)/include/net/inet_connection_sock.h
    BUILD_BUG_ON(sizeof(struct arm) > ICSK_CA_PRIV_SIZE); 

    return tcp_register_congestion_control(&tcp_mimic);
}

static void __exit onUnRegister(void)
{
    // /* Release Netlink Socket */
    // if (socket)
    // {
    //     sock_release(socket->sk_socket);
    // }

    tcp_unregister_congestion_control(&tcp_mimic);
}

module_init(onRegister);
module_exit(onUnRegister);

MODULE_AUTHOR("Lorenzo Pappone");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mimic");
MODULE_VERSION("1.0");