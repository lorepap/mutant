#include <asm-generic/errno.h>
#include <asm-generic/errno-base.h>
#include <net/tcp.h>
#include "mutant.h"

#define NETLINK_USER 25
#define MAX_PAYLOAD 256 /* maximum payload size*/

// Communication Flags
#define COMM_END 0
#define COMM_BEGIN 1
#define COMM_SELECT_ARM 2
#define TEST 3

// Netlink comm variables
struct sock *nl_sk = NULL;
static u32 socketId = -1;
static u32 selected_proto_id = CUBIC;
static u32 prev_proto_id = CUBIC;
static bool switching_flag = false;

struct mutant_state {
    struct bictcp *cubic_state;
    struct hybla *hybla_state;
    struct bbr *bbr_state;
    struct westwood *westwood_state;
    // Add more pointers for other congestion control schemes as needed
};

// Global variable to store the state
static struct mutant_state *saved_states;


// Netlink comm APIs
static void send_msg(char *message, int socketId)
{
    int retryCounter = 0;
    int messageSize;
    int messageSentReponseCode;
    struct sk_buff *socketMessage;
    struct nlmsghdr *reply_nlh = NULL;

    if (socketId == -1)
    {
        printk(KERN_INFO "Message not sent: socket not initialized (-1)");
        return;
    }

    messageSize = strlen(message);

    socketMessage = nlmsg_new(messageSize, 0);

    if (!socketMessage)
    {
        printk(KERN_ERR "Mutant | %s: Failed to allocate new skb | (PID = %d)\n", __FUNCTION__, socketId);
        return;
    }

    reply_nlh = nlmsg_put(socketMessage, 0, 0, NLMSG_DONE, messageSize, 0);

    NETLINK_CB(socketMessage).dst_group = 0; /* not in mcast group */

    strncpy(NLMSG_DATA(reply_nlh), message, messageSize);

    if (nl_sk == NULL)
    {
        printk(KERN_ERR "Mutant | %s: nl_sk is NULL | (PID = %d)\n", __FUNCTION__, socketId);
        return;
    }

    messageSentReponseCode = nlmsg_unicast(nl_sk, socketMessage, socketId);

    if (messageSentReponseCode < 0)
    {
        printk(KERN_ERR "Mutant | %s: Error while sending message | (PID = %d) | (Error = %d) | (Count = %d)\n", __FUNCTION__, socketId, messageSentReponseCode, retryCounter);
    }
    // else
    // {
    //     printk("Mutant | %s: Correctly sent message to app layer | PID = %d | Message: %s", __FUNCTION__, socketId, message);
    // }
}

static void start_connection(struct nlmsghdr *nlh)
{

    // Initialize saved_states
    init_saved_states();

	printk(KERN_INFO "User-kernel communication initialized");
    char message[MAX_PAYLOAD - 1];

    socketId = nlh->nlmsg_pid;

    // Send application layer a message to inform that the connection has started
    snprintf(message, MAX_PAYLOAD - 1, "%u", 0);
    send_msg(message, socketId);
}

static void end_connection(struct nlmsghdr *nlh)
{
    printk(KERN_INFO "User-kernel communication ended");
    char message[MAX_PAYLOAD - 1];

    // Send application layer a message to inform that the connection has ended
    snprintf(message, MAX_PAYLOAD - 1, "%u", -1);
    send_msg(message, socketId);

    // free all the memory allocated for the saved states
    if (saved_states) {
        if (saved_states->cubic_state) {
            kfree(saved_states->cubic_state);
        }
        if (saved_states->hybla_state) {
            kfree(saved_states->hybla_state);
        }
        if (saved_states->bbr_state) {
            kfree(saved_states->bbr_state);
        }
        if (saved_states->westwood_state) {
            kfree(saved_states->westwood_state);
        }
        kfree(saved_states);
    }
    
    socketId = -1;
}


static void receive_msg(struct sk_buff *skb)
{
    struct nlmsghdr *nlh = NULL;

    if (skb == NULL)
    {
        printk(KERN_ERR "Mutant | %s: skb is NULL\n", __FUNCTION__);
        return;
    }

    nlh = (struct nlmsghdr *)skb->data;
	// printk(KERN_INFO "received data");
    switch (nlh->nlmsg_flags)
    {
    case COMM_END:
        printk(KERN_INFO "%s: End connection signal received.", __FUNCTION__);
        end_connection(nlh);
        socketId = -1;
        break;

    case COMM_BEGIN:
        printk(KERN_INFO "%s: Start connection signal received.", __FUNCTION__);
        start_connection(nlh);
        break;

    case COMM_SELECT_ARM:
        if (nlh->nlmsg_seq != selected_proto_id) {
            switching_flag = true;
            prev_proto_id = selected_proto_id;
            selected_proto_id = nlh->nlmsg_seq; 
            printk("%s: received switching signal (id: %d->%d)", __FUNCTION__, prev_proto_id, selected_proto_id);
        }
        break;
    default: // testing
		printk("Test message received!");
        break;
    }
}


static int __init netlink_init(void)
{
    struct netlink_kernel_cfg cfg = {
        .input = receive_msg,
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


static void init_saved_states(void) {
    // TODO: The state could be initialized with the init function (see load_state)
    saved_states = kmalloc(sizeof(struct mutant_state), GFP_KERNEL);
    if (!saved_states) {
        pr_err("Failed to allocate memory for saved_states\n");
        return;
    }
    // Initialize pointers to NULL initially
    saved_states->cubic_state = NULL;
    saved_states->hybla_state = NULL;
    saved_states->bbr_state = NULL;
    saved_states->westwood_state = NULL;
    // Initialize other pointers as needed
}



// FOR DEBUG
static void print_bictcp(struct bictcp *cubic) {
    printk("BiC-TCP State:\n");
    printk("[DEBUG] cnt: %d\n", cubic->cnt);
    printk("[DEBUG] last_max_cwnd: %d\n", cubic->last_max_cwnd);
    printk("[DEBUG] last_cwnd: %d\n", cubic->last_cwnd);
    printk("[DEBUG] last_time: %d\n", cubic->last_time);
    printk("[DEBUG] bic_origin_point: %d\n", cubic->bic_origin_point);
    printk("[DEBUG] bic_K: %d\n", cubic->bic_K);
    printk("[DEBUG] delay_min: %d\n", cubic->delay_min);
    printk("[DEBUG] ack_cnt: %d\n", cubic->ack_cnt);
    printk("[DEBUG] tcp_cwnd: %d\n", cubic->tcp_cwnd);
    printk("[DEBUG] found: %d\n", cubic->found);
    // Print other fields as needed
}

static void print_hybla(struct hybla *hybla) {
    printk("Hybla State:\n");
    printk("[DEBUG] hybla_en: %d\n", hybla->hybla_en);
    printk("[DEBUG] snd_cwnd_cents: %d\n", hybla->snd_cwnd_cents);
    printk("[DEBUG] rho: %d\n", hybla->rho);
    printk("[DEBUG] rho2: %d\n", hybla->rho2);
    printk("[DEBUG] rho_3ls: %d\n", hybla->rho_3ls);
    printk("[DEBUG] rho2_7ls: %d\n", hybla->rho2_7ls);
    printk("[DEBUG] minrtt_us: %d\n", hybla->minrtt_us);
}

static void print_bbr(struct bbr *bbr){
    return;
}

static void print_mutant_state(struct sock *sk) {
    if (selected_proto_id == CUBIC && saved_states->cubic_state) {
        memcpy(saved_states->cubic_state, inet_csk_ca(sk), sizeof(struct bictcp));
        print_bictcp(saved_states->cubic_state);
    }
    else if (selected_proto_id == HYBLA && saved_states->hybla_state) {
        printk("print hybla state\n");
        memcpy(saved_states->hybla_state, inet_csk_ca(sk), sizeof(struct hybla));
        print_hybla(saved_states->hybla_state);
    }
    else return;
    // else if (selected_proto_id == 3) {
    //     print_bbr(saved_states->bbr_state);
    // } else {
    //     printk("BBR state is NULL\n");
    // }

    // Add more conditions for other congestion control schemes as needed
}
////////////////////////////////////////////////

// Wrapper struct to call the tcp_congestion_ops of the selected policy
struct tcp_mutant_wrapper {
    struct tcp_congestion_ops *current_ops;
};

static struct tcp_mutant_wrapper mutant_wrapper;
extern struct tcp_congestion_ops cubictcp;
extern struct tcp_congestion_ops tcp_hybla;
extern struct tcp_congestion_ops tcp_bbr_cong_ops;
extern struct tcp_congestion_ops tcp_westwood;
    

// Function to save the state of a specific congestion control scheme
static void save_state(struct sock *sk) {
    if (!saved_states) {
        pr_err("saved_states not initialized\n");
        return;
    }
    printk("Saving state of %d", prev_proto_id);
    // Save state of the current congestion control protocol
    if (prev_proto_id == CUBIC) {
        if (saved_states->cubic_state) {
            kfree(saved_states->cubic_state);
        }
        saved_states->cubic_state = kmalloc(sizeof(struct bictcp), GFP_KERNEL);
        if (saved_states->cubic_state) {
            memcpy(saved_states->cubic_state, inet_csk_ca(sk), sizeof(struct bictcp));
        } else {
            pr_err("Failed to allocate memory for cubic_state\n");
        }
    } else if (prev_proto_id == HYBLA) {
        if (saved_states->hybla_state) {
            kfree(saved_states->hybla_state);
        }
        saved_states->hybla_state = kmalloc(sizeof(struct hybla), GFP_KERNEL);
        if (saved_states->hybla_state) {
            memcpy(saved_states->hybla_state, inet_csk_ca(sk), sizeof(struct hybla));
        } else {
            pr_err("Failed to allocate memory for hybla_state\n");
        }
    } else if (prev_proto_id == BBR) {
        if (saved_states->bbr_state) {
            kfree(saved_states->bbr_state);
        }
        saved_states->bbr_state = kmalloc(sizeof(struct bbr), GFP_KERNEL);
        if (saved_states->bbr_state) {
            memcpy(saved_states->hybla_state, inet_csk_ca(sk), sizeof(struct bbr));
        } else {
            pr_err("Failed to allocate memory for bbr_state\n");
        }
    } else if(prev_proto_id == WESTWOOD) {
        if (saved_states->westwood_state) {
            kfree(saved_states->westwood_state);
        }
        saved_states->westwood_state = kmalloc(sizeof(struct westwood), GFP_KERNEL);
        if (saved_states->westwood_state) {
            memcpy(saved_states->westwood_state, inet_csk_ca(sk), sizeof(struct westwood));
        } else {
            pr_err("Failed to allocate memory for westwood_state\n");
        }
    }
}

// Function to load the state of a specific congestion control scheme
static void load_state(struct sock *sk){
    struct tcp_congestion_ops *cubic;
    struct tcp_congestion_ops *hybla;
    struct tcp_congestion_ops *bbr;
    struct tcp_congestion_ops *westwood;
    cubic = &cubictcp;
    hybla = &tcp_hybla;
    bbr = &tcp_bbr_cong_ops;
    westwood = &tcp_westwood;

    if (!saved_states) {
        pr_err("saved_states not initialized\n");
        return;
    }

    switch (selected_proto_id)
    {
    case CUBIC:
        if (saved_states->cubic_state) {
            printk("%s: Saving Cubic state.", __FUNCTION__);
            memcpy(inet_csk_ca(sk), saved_states->cubic_state, sizeof(struct bictcp));
        }
        else{
            printk("%s: Initializing Cubic state", __FUNCTION__);
            saved_states->cubic_state = kmalloc(sizeof(struct bictcp), GFP_KERNEL);
            memcpy(inet_csk_ca(sk), saved_states->cubic_state, sizeof(struct bictcp));
            cubic->init(sk);
            memcpy(saved_states->cubic_state, inet_csk_ca(sk), sizeof(struct bictcp));
        }
        break;
    case HYBLA:
        if (saved_states->hybla_state) {
            printk("%s: Saving Hybla state.", __FUNCTION__);
            memcpy(inet_csk_ca(sk), saved_states->hybla_state, sizeof(struct hybla));
        }
        else{
            printk("%s: Initializing Hybla state", __FUNCTION__);
            saved_states->hybla_state = kmalloc(sizeof(struct hybla), GFP_KERNEL);
            memcpy(inet_csk_ca(sk), saved_states->hybla_state, sizeof(struct hybla));
            hybla->init(sk);
            memcpy(saved_states->hybla_state, inet_csk_ca(sk), sizeof(struct hybla));
        }
        break;
     case BBR:
        if (saved_states->bbr_state) {
            printk("%s: Saving BBR state.", __FUNCTION__);
            memcpy(inet_csk_ca(sk), saved_states->bbr_state, sizeof(struct bbr));
        }
        else{
            printk("%s: Initializing BBR state", __FUNCTION__);
            saved_states->bbr_state = kmalloc(sizeof(struct bbr), GFP_KERNEL);
            memcpy(inet_csk_ca(sk), saved_states->bbr_state, sizeof(struct bbr));
            bbr->init(sk);
            memcpy(saved_states->bbr_state, inet_csk_ca(sk), sizeof(struct bbr));
        }
        break;
    case WESTWOOD:
        if (saved_states->westwood_state) {
            printk("%s: Saving Westwood state.", __FUNCTION__);
            memcpy(inet_csk_ca(sk), saved_states->westwood_state, sizeof(struct westwood));
        }
        else{
            printk("%s: Initializing Westwood state", __FUNCTION__);
            saved_states->westwood_state = kmalloc(sizeof(struct westwood), GFP_KERNEL);
            memcpy(inet_csk_ca(sk), saved_states->westwood_state, sizeof(struct westwood));
            westwood->init(sk);
            memcpy(saved_states->westwood_state, inet_csk_ca(sk), sizeof(struct westwood));
        }
        break;
    default:
        break;
    }
}

// Swicthing congestion control function
void mutant_switch_congestion_control(void) {

    switch (selected_proto_id)
    {
    case CUBIC:
        printk(KERN_INFO "Switching to Cubic (ID: %d)", selected_proto_id);
        mutant_wrapper.current_ops = &cubictcp;
        break;
    case HYBLA:
        printk(KERN_INFO "Switching to Hybla (ID: %d)", selected_proto_id);
        mutant_wrapper.current_ops = &tcp_hybla;
        break;
    case BBR:
        printk(KERN_INFO "Switching to BBR (ID: %d)", selected_proto_id);
        mutant_wrapper.current_ops = &tcp_bbr_cong_ops;
        break;
    case WESTWOOD:
        printk(KERN_INFO "Switching to Westwood (ID: %d)", selected_proto_id);
        mutant_wrapper.current_ops = &tcp_westwood;
        break;
    default:
        printk(KERN_INFO "Switching to default (Cubic)");
        mutant_wrapper.current_ops = &cubictcp;
        break;
    }
}


static void send_net_params(struct tcp_sock *tp, int socketId)
{
    // message vars
    char message[MAX_PAYLOAD - 1];

    __u32 now = tcp_jiffies32;
    __u32 cwnd = tp->snd_cwnd;
    __u32 rtt = tp->srtt_us;
    __u32 rtt_dev = tp->mdev_us;
	__u32 rtt_min = tcp_min_rtt(tp);
    __u16 MSS = tp->advmss;
    __u32 delivered = tp->delivered;
    __u32 lost = tp->lost_out;
    __u32 in_flight = tp->packets_out;
    __u32 retransmitted = tp->retrans_out;

    snprintf(message, MAX_PAYLOAD - 1, "%u;%u;%u;%u;%u;%u;%u;%u;%u;%u;%u",
             now, cwnd, rtt, rtt_dev, rtt_min, MSS, delivered, lost,
             in_flight, retransmitted, selected_proto_id);
    
    // printk("Mutant %s: Sending message to user: %s", __FUNCTION__, message);

    send_msg(message, socketId);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


static void mutant_tcp_init(struct sock *sk) {
    // Initialize the selected protocol
    if (mutant_wrapper.current_ops->init){
        mutant_wrapper.current_ops->init(sk);
        printk("Mutant %s: init %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
}

static void mutant_tcp_cong_avoid(struct sock *sk, u32 ack, u32 acked) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->cong_avoid){
        mutant_wrapper.current_ops->cong_avoid(sk, ack, acked);
        // printk("Mutant %s: cong_avoid %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
    // Handle null value
    if (sk == NULL) {
        printk("Mutant %s: sk is NULL", __FUNCTION__);
        return;
    }
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
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->cwnd_event){
        mutant_wrapper.current_ops->cwnd_event(sk, event);
        // printk("Mutant %s: cwnd_event %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
}

static void mutant_tcp_pkts_acked(struct sock *sk, const struct ack_sample *sample) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->pkts_acked){
        mutant_wrapper.current_ops->pkts_acked(sk, sample);
        // printk("Mutant %s: acked %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
    // Send network features every ack (for now)    
    struct tcp_sock *tp = tcp_sk(sk);
    send_net_params(tp, socketId);
    // Switching operation
    if (switching_flag) {
        printk("%s: Switching flag ON", __FUNCTION__);
        save_state(sk);
        mutant_switch_congestion_control();
        load_state(sk);
        switching_flag = false;
    }
    // print_mutant_state(sk);
}

static void mutant_tcp_ack_event(struct sock *sk, u32 flags) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->in_ack_event)
        mutant_wrapper.current_ops->in_ack_event(sk, flags);
}

static u32 mutant_tcp_cong_control(struct sock *sk, const struct rate_sample *rs, u32 ack, u32 acked, int flag) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->cong_control){
        mutant_wrapper.current_ops->cong_control(sk, rs);
        // printk("Mutant %s: cong_control %s", __FUNCTION__, mutant_wrapper.current_ops->name);
        return 0;
    }
    // printk("Mutant %s: cong_control %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    return 1;
}

static u32 mutant_tcp_sndbuf_expand(struct sock *sk) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->sndbuf_expand){
        return mutant_wrapper.current_ops->sndbuf_expand(sk);
        printk("Mutant %s: sndbuf_expand %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
    // printk("Mutant %s: sndbuf_expand %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    return 2;
}

static u32 mutant_tcp_min_tso_segs(struct sock *sk) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->min_tso_segs){
        return mutant_wrapper.current_ops->min_tso_segs(sk);
        printk("Mutant %s: min_tso_segs %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    }
    // printk("Mutant %s: min_tso_segs %s", __FUNCTION__, mutant_wrapper.current_ops->name);
    return 2;
}

static size_t mutant_tcp_get_info(struct sock *sk, u32 ext, int *attr,
			   union tcp_cc_info *info) {
    if (mutant_wrapper.current_ops && mutant_wrapper.current_ops->get_info)
        return mutant_wrapper.current_ops->get_info(sk, ext, attr, info);
    else
        return 0; // or some other default value
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


static struct tcp_congestion_ops mutant_cong_ops __read_mostly = {
    .flags		= TCP_CONG_NON_RESTRICTED,
    .init       = mutant_tcp_init,
    .ssthresh   = mutant_tcp_ssthresh,
    .cong_avoid = mutant_tcp_cong_avoid,
    .set_state  = mutant_tcp_set_state,
    .undo_cwnd  = mutant_tcp_undo_cwnd,
    .cwnd_event = mutant_tcp_cwnd_event,
    .pkts_acked = mutant_tcp_pkts_acked,
    .in_ack_event	= mutant_tcp_ack_event,
    .sndbuf_expand = mutant_tcp_sndbuf_expand,
    .min_tso_segs = mutant_tcp_min_tso_segs,
    .get_info   = mutant_tcp_get_info,
    .mutant_tcp_cong_control = mutant_tcp_cong_control,
    .owner      = THIS_MODULE,
    .name       = "mutant",
};


static int __init mutant_tcp_module_init(void) {
    // Netlink init
    if (netlink_init() < 0) {
        pr_err("Netlink could not be initialized\n");
        return -EINVAL;
    }
    
    // Initialize saved_states
    init_saved_states();

    // Initial setup or default congestion control selection
    mutant_wrapper.current_ops = &cubictcp;

    // Register the custom congestion control
    if (tcp_register_congestion_control(&mutant_cong_ops) < 0) {
        pr_err("Mutant congestion control could not be registered\n");
        return -EINVAL;
    }

    return 0;
}

static void __exit mutant_tcp_module_exit(void) {
    netlink_exit();
    tcp_unregister_congestion_control(&mutant_cong_ops);
}

module_init(mutant_tcp_module_init);
module_exit(mutant_tcp_module_exit);
MODULE_AUTHOR("Lorenzo Pappone");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mutant");
MODULE_VERSION("1.0");