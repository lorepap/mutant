#include <asm-generic/errno.h>
#include <asm-generic/errno-base.h>
#include "protocol/cubic.h"
#include "protocol/hybla.h"
#include "protocol/bbr.h"

#include "protocol/mimic.h"

#define NETLINK_USER 25

// Netlink comm variables
struct sock *nl_sk = NULL;

static u32 selectedProtocolId = 0;

/*
protocols:
cubic 0
bbr 1
hybla 2
*/

/*
 BBR does not implement cong_avoid but only cong_control. All protocols have 
 cong_avoid but not cong_control. In tcp_input.c you can see how they are used.
 Both APIs are mutually exclusive, meaning that they cannot live in the same
 tcp_congestion_ops structure.

 Sol 1: protocol registration at runtime? testing in progress. In this case we
		will need a different congestion_ops for bbr to implement. It is not a problem
		as long as we can really unregister the previous structure and register a new one.

 Sol 2: using a single congestion function for both and modify the kernel file tcp_input.c.
		It means that we have to correct the input parameters as cong_control takes the sock and rate_sample
		whereas cong_avoid takes sock, ack value and acked (# acked packets). In tcp.h we
		will need to modify tcp_congestion_ops functions declarations.
*/

// Netlink comm APIs
static void nl_recv_msg(struct sk_buff *skb)
{
    struct nlmsghdr *nlh;
	long result;
	int res;
	char *msg;
    nlh = (struct nlmsghdr*)skb->data;

	msg = (char*)nlmsg_data(nlh);
	res = kstrtol(msg, 10, &result);
	if (res!=0)
		printk(KERN_ALERT "Error while converting");
	printk(KERN_INFO "Netlink received msg payload: %ld\n", result);
	
	// Change protocol
	selectedProtocolId = (int)result;

	// // Testing new congestion_ops registration
	// tcp_unregister_congestion_control(&tcp_mimic);
	// tcp_register_congestion_control(&tcp_mimic_test);
	// printk(KERN_INFO "New registration done successfully");

}

static int __init netlink_init(void)
{
    struct netlink_kernel_cfg cfg = {
        .input = nl_recv_msg,
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

static void onInit(struct sock *sk)
{
    bictcp_init(sk);
    // tcp_vegas_init(sk);
	bbr_init(sk);
	hybla_init(sk);
}

static void onPacketsAcked(struct sock *sk, const struct ack_sample *sample)
{
	// NOTE: printk increases overhead (tested with iperf3)
	// printk(KERN_INFO "acked - protocol selected: %d\n", selectedProtocolId);
	switch (selectedProtocolId) 
	{
		case 0: bictcp_acked(sk, sample);
		// case 1: tcp_vegas_pkts_acked(sk, sample);
		case 1: return;
		case 2: return;
		default: bictcp_acked(sk, sample);
	}
}

static u32 onUndoCwnd(struct sock *sk){
	switch (selectedProtocolId)
	{
		case 0: return tcp_reno_undo_cwnd(sk);
		// case 1: return tcp_reno_undo_cwnd(sk);
		case 1: return bbr_undo_cwnd(sk);
		case 2: return tcp_reno_undo_cwnd(sk);
		default: return tcp_reno_undo_cwnd(sk);
	}
}

static u32 onSshthresh(struct sock *sk){
	switch (selectedProtocolId)
	{
    	case 0: return bictcp_recalc_ssthresh(sk);
		// case 1: return tcp_reno_ssthresh(sk);
		case 1: return bbr_ssthresh(sk);
		case 2: return tcp_reno_ssthresh(sk);
		default: return bictcp_recalc_ssthresh(sk);
	}
}

static void onAvoidCongestion(struct sock *sk, u32 ack, u32 acked){
	
	switch (selectedProtocolId)
	{
    	case 0: bictcp_cong_avoid(sk, ack, acked);
		// case 1: tcp_vegas_cong_avoid(sk, ack, acked);
		case 1: return;
		case 2: hybla_cong_avoid(sk, ack, acked);
		default: bictcp_cong_avoid(sk, ack, acked);
	}
}

static void onCongestionEvent(struct sock *sk, enum tcp_ca_event event)
{
	switch (selectedProtocolId)
	{
     	case 0: bictcp_cwnd_event(sk, event);
		// case 1: tcp_vegas_cwnd_event(sk, event);
		case 1: bbr_cwnd_event(sk, event);
		case 2: return;
		default: bictcp_cwnd_event(sk, event);
	}
}

static void onSetState (struct sock *sk, __u8 new_state)
{
	switch (selectedProtocolId)
	{
		case 0:	bictcp_state(sk, new_state);
		// case 1:	tcp_vegas_state(sk, new_state);
		case 1: bbr_set_state(sk, new_state);
		case 2: hybla_state(sk, new_state);
		default: bictcp_state(sk, new_state);
	}
}

// static void onCongControl(struct sock *sk, const struct rate_sample *rs)
// {
// 	// bbr has not cong_avoid but only cong_control (for pacing rate)
// 	// we will use default API to update pacing rate and be responsive to cong_control API
// 	switch (selectedProtocolId)
// 	{
// 		case 0:	return tcp_update_pacing_rate(sk);
// 		case 1: bbr_main(sk, rs);
// 		case 2:	return tcp_update_pacing_rate(sk);
// 		default: return tcp_update_pacing_rate(sk);
// 	}
// }

// check this
static u32 onSndbuf_expand(struct sock *sk)
{
	switch (selectedProtocolId)
	{
		case 0:	return 1;
		case 1:	return bbr_sndbuf_expand(sk);
		case 2:	return 1;
		default: return 1;
	}
}

static u32 onMintso_segs(struct sock *sk)
{
	switch (selectedProtocolId)
	{
		case 0:	return 1;
		case 1: return bbr_min_tso_segs(sk);
		case 2:	return 1;
		default: return 1;
	}
}

static struct tcp_congestion_ops tcp_mimic __read_mostly = {
    .init = onInit,
    .pkts_acked = onPacketsAcked,
    .undo_cwnd = onUndoCwnd,
    .ssthresh = onSshthresh,
    .cong_avoid = onAvoidCongestion,
    .cwnd_event = onCongestionEvent,
	.set_state	= onSetState,
	// .cong_control = onCongControl,
	// .sndbuf_expand	= onSndbuf_expand,
	// .min_tso_segs	= onMintso_segs,
    .owner = THIS_MODULE,
    .name = "mimic"
};

static struct tcp_congestion_ops tcp_mimic_test __read_mostly = {
    .init = onInit,
    .pkts_acked = onPacketsAcked,
    .undo_cwnd = onUndoCwnd,
    .ssthresh = onSshthresh,
    .cong_avoid = onAvoidCongestion,
    .cwnd_event = onCongestionEvent,
	.set_state	= onSetState,
	// .cong_control = onCongControl,
	// .sndbuf_expand	= onSndbuf_expand,
	// .min_tso_segs	= onMintso_segs,
    .owner = THIS_MODULE,
    .name = "mimic"
};

static int __init onRegister(void)
{

	netlink_init();

    BUILD_BUG_ON(sizeof(struct arm) > ICSK_CA_PRIV_SIZE);

	/* Precompute a bunch of the scaling factors that are used per-packet
	 * based on SRTT of 100ms
	 */

	beta_scale = 8*(BICTCP_BETA_SCALE+beta) / 3
		/ (BICTCP_BETA_SCALE - beta);

	cube_rtt_scale = (bic_scale * 10);	/* 1024*c/rtt */

	/* calculate the "K" for (wmax-cwnd) = c/rtt * K^3
	 *  so K = cubic_root( (wmax-cwnd)*rtt/c )
	 * the unit of K is bictcp_HZ=2^10, not HZ
	 *
	 *  c = bic_scale >> 10
	 *  rtt = 100ms
	 *
	 * the following code has been designed and tested for
	 * cwnd < 1 million packets
	 * RTT < 100 seconds
	 * HZ < 1,000,00  (corresponding to 10 nano-second)
	 */

	/* 1/c * 2^2*bictcp_HZ * srtt */
	cube_factor = 1ull << (10+3*BICTCP_HZ); /* 2^40 */

	/* divide by bic_scale and by constant Srtt (100ms) */
	do_div(cube_factor, bic_scale * 10);

    return tcp_register_congestion_control(&tcp_mimic);
}

static void __exit onUnRegister(void)
{
	netlink_exit();
    tcp_unregister_congestion_control(&tcp_mimic);
}

module_init(onRegister);
module_exit(onUnRegister);

MODULE_AUTHOR("Lorenzo Pappone");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mimic");
MODULE_VERSION("1.0");