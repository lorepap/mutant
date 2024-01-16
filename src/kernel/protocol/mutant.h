#ifndef __MIMIC_H
#define __MIMIC_H 1

#include <linux/types.h>  // Include this line


#endif /* __MIMIC_H */

struct mutant
{
    u32 cnt;                   /* increase cwnd by 1 after ACKs */
    u32 last_max_cwnd;         /* last maximum snd_cwnd */
    u32 last_cwnd;             /* the last snd_cwnd */
    u32 last_cwnd_update_time; /* time when updated last_cwnd */
    u32 bic_origin_point;      /* origin point of bic function */
    u32 bic_K;                 /* time to origin point from the beginning of the current epoch */
    u32 delay_min;             /* min delay (usec) */
    u32 epoch_start;           /* beginning of an epoch */
    u32 acked_count;           /* number of acks */
    u32 estimated_cwnd;        /* estimated tcp cwnd */
    u16 unused;
    u8 sample_cnt;   /* number of samples to decide curr_rtt */
    u8 found;        /* the exit point is found? */
    u32 round_start; /* beginning of each round */
    u32 last_ack;    /* last time when the ACK spacing is close */
    u32 curr_rtt;    /* the minimum rtt of current round */

    // cubic + illinois
    u32 end_seq;  /* end_seq of the round */
    u16 rttCount; /* # of RTTs measured within last RTT */
    u32 minRTT;   /* min of RTTs measured within last RTT (in usec) */
    u32 baseRTT;  /* the min of all RTT measurements seen (in usec) */

    // hybla
    u32 snd_cwnd_cents; /* Keeps increment values when it is <1, <<7 */
    u32 rho;            /* Rho parameter, integer part  */
    u32 rho2;           /* Rho * Rho, integer part */
    u32 rho_3ls;        /* Rho parameter, <<3 */
    u32 rho2_7ls;       /* Rho^2, <<7	*/

    // vegas
    u32 beg_snd_nxt;
};