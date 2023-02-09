/*
* A sample template of new congestion control algorithm
* Steps:
* 1. Implement the following methods
* 2. Change method name "template_init" to "xxx_init" where xxx is name of new algorithm
* 3. Change method name "template_cong_avoid" to "xxxx_cong_avoid" where xxx is name of new algorithm
* 3. Change all instances of "__TEMPLATE" to "__xxx" where xxx is name of new algorithm
* 2. Copy and paste file in src/kernel/protocols
* 3. Follow the set up steps to rebuild & retrain
*/

#include <asm-generic/int-ll64.h>
#include "../mimic.h"


#ifndef __TEMPLATE
#define __TEMPLATE 1

void template_init(struct sock *sk, struct arm *ca)
{
    // TODO: Add code here
}

static void template_acked(struct sock *sk, const struct ack_sample *sample, struct arm *ca)
{
    // TODO: Add code here
}

static __u32 template_cong_avoid(struct sock *sk, __u32 ack, __u32 acked)
{
    __u32 cwnd_delta;
    

    // TODO: Add code here

    return cwnd_delta;
}

#endif /* __TEMPLATE */