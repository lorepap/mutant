#ifndef __MIMIC_H
#define __MIMIC_H 1

// Cubic variables
static u32 cube_rtt_scale __read_mostly;
static u32 beta_scale __read_mostly;
static u64 cube_factor __read_mostly;

struct arm {

/* BIC TCP Parameters */
	u32	cnt;		/* increase cwnd by 1 after ACKs */
	u32	last_max_cwnd;	/* last maximum snd_cwnd */
	u32	last_cwnd;	/* the last snd_cwnd */
	u32	last_time;	/* time when updated last_cwnd */
	u32	bic_origin_point;/* origin point of bic function */
	u32	bic_K;		/* time to origin point
				   from the beginning of the current epoch */
	u32	delay_min;	/* min delay (msec << 3) */
	u32	epoch_start;	/* beginning of an epoch */
	u32	ack_cnt;	/* number of acks */
	u32	tcp_cwnd;	/* estimated tcp cwnd */
	u16	cubic_unused;
	u8	sample_cnt;	/* number of samples to decide curr_rtt */
	u8	found;		/* the exit point is found? */
	u32	round_start;	/* beginning of each round */
	u32	end_seq;	/* end_seq of the round */
	u32	last_ack;	/* last time when the ACK spacing is close */
	u32	curr_rtt;	/* the minimum rtt of current round */

// /* Vegas variables */
// 	u32	beg_snd_nxt;	/* right edge during last RTT */
// 	u32	beg_snd_una;	/* left edge  during last RTT */
// 	u32	beg_snd_cwnd;	/* saves the size of the cwnd */
// 	u8	doing_vegas_now;/* if true, do vegas for this RTT */
// 	u16	cntRTT;		/* # of RTTs measured within last RTT */
// 	u32	minRTT;		/* min of RTTs measured within last RTT (in usec) */
// 	u32	baseRTT;	/* the min of all Vegas RTT measurements seen (in usec) */

/* Tcp Hybla structure. */
	bool  hybla_en;
	u32   snd_cwnd_cents; /* Keeps increment values when it is <1, <<7 */
	u32   rho;	      /* Rho parameter, integer part  */
	u32   rho2;	      /* Rho * Rho, integer part */
	u32   rho_3ls;	      /* Rho parameter, <<3 */
	u32   rho2_7ls;	      /* Rho^2, <<7	*/
	u32   minrtt_us;      /* Minimum smoothed round trip time value seen */

/* BBR */
	u32	min_rtt_us;	        /* min RTT in min_rtt_win_sec window */
	u32	min_rtt_stamp;	        /* timestamp of min_rtt_us */
	u32	probe_rtt_done_stamp;   /* end time for BBR_PROBE_RTT mode */
	struct minmax bw;	/* Max recent delivery rate in pkts/uS << 24 */
	u32	rtt_cnt;	    /* count of packet-timed rounds elapsed */
	u32     next_rtt_delivered; /* scb->tx.delivered at end of round */
	u64	cycle_mstamp;	     /* time of this cycle phase start */
	u32     mode:3,		     /* current bbr_mode in state machine */
		prev_ca_state:3,     /* CA state on previous ACK */
		packet_conservation:1,  /* use packet conservation? */
		bbr_round_start:1,	     /* start of packet-timed tx->ack round? */
		idle_restart:1,	     /* restarting after idle? */
		probe_rtt_round_done:1,  /* a BBR_PROBE_RTT round at 4 pkts? */
		unused:13,
		lt_is_sampling:1,    /* taking long-term ("LT") samples now? */
		lt_rtt_cnt:7,	     /* round trips in long-term interval */
		lt_use_bw:1;	     /* use lt_bw as our bw estimate? */
	u32	lt_bw;		     /* LT est delivery rate in pkts/uS << 24 */
	u32	lt_last_delivered;   /* LT intvl start: tp->delivered */
	u32	lt_last_stamp;	     /* LT intvl start: tp->delivered_mstamp */
	u32	lt_last_lost;	     /* LT intvl start: tp->lost */
	u32	pacing_gain:10,	/* current gain for setting pacing rate */
		cwnd_gain:10,	/* current gain for setting cwnd */
		full_bw_reached:1,   /* reached full bw in Startup? */
		full_bw_cnt:2,	/* number of rounds without large bw gains */
		cycle_idx:3,	/* current index in pacing_gain cycle array */
		has_seen_rtt:1, /* have we seen an RTT sample yet? */
		unused_b:5;
	u32	prior_cwnd;	/* prior cwnd upon entering loss recovery */
	u32	full_bw;	/* recent bw, to estimate if pipe is full */

	/* For tracking ACK aggregation: */
	u64	ack_epoch_mstamp;	/* start of ACK sampling epoch */
	u16	extra_acked[2];		/* max excess data ACKed in epoch */
	u32	ack_epoch_acked:20,	/* packets (S)ACKed in sampling epoch */
		extra_acked_win_rtts:5,	/* age of extra_acked, in round trips */
		extra_acked_win_idx:1,	/* current index in extra_acked array */
		unused_c:6;

};

// Cubic headers
static inline void bictcp_reset(struct arm *ca);
static inline u32 bictcp_clock(void);
static inline void bictcp_hystart_reset(struct sock *sk);
static void bictcp_init(struct sock *sk);
static void bictcp_cwnd_event(struct sock *sk, enum tcp_ca_event event);
static u32 cubic_root(u64 a);
static inline void bictcp_update(struct arm *ca, u32 cwnd, u32 acked);
static void bictcp_cong_avoid(struct sock *sk, u32 ack, u32 acked);
static u32 bictcp_recalc_ssthresh(struct sock *sk);
static void bictcp_state(struct sock *sk, u8 new_state);
static void hystart_update(struct sock *sk, u32 delay);
static void bictcp_acked(struct sock *sk, const struct ack_sample *sample);

// // Vegas headers
// void tcp_vegas_init(struct sock *sk);
// void tcp_vegas_state(struct sock *sk, u8 ca_state);
// void tcp_vegas_pkts_acked(struct sock *sk, const struct ack_sample *sample);
// void tcp_vegas_cwnd_event(struct sock *sk, enum tcp_ca_event event);
// size_t tcp_vegas_get_info(struct sock *sk, u32 ext, int *attr,
// 			  union tcp_cc_info *info);

// Hybla headers
static inline void hybla_recalc_param (struct sock *sk);
static void hybla_init(struct sock *sk);
static void hybla_state(struct sock *sk, u8 ca_state);
static inline u32 hybla_fraction(u32 odds);
static void hybla_cong_avoid(struct sock *sk, u32 ack, u32 acked);



#endif /* __MIMIC_H */