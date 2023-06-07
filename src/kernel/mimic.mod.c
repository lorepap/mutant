#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(.gnu.linkonce.this_module) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section(__versions) = {
<<<<<<< HEAD
	{ 0x4142e96d, "module_layout" },
	{ 0x4e82243e, "param_ops_int" },
	{ 0x6a70c480, "tcp_unregister_congestion_control" },
	{ 0xdd453c3e, "netlink_kernel_release" },
	{ 0x346581a8, "tcp_register_congestion_control" },
	{ 0xf005b060, "__netlink_kernel_create" },
	{ 0x33cd4d84, "init_net" },
	{ 0x56470118, "__warn_printk" },
	{ 0xb911bb58, "minmax_running_max" },
	{ 0x2ea2c95c, "__x86_indirect_thunk_rax" },
	{ 0xdee4abea, "tcp_reno_ssthresh" },
	{ 0x92928499, "tcp_reno_cong_avoid" },
	{ 0x87ae370c, "tcp_cong_avoid_ai" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x93752a3c, "tcp_slow_start" },
	{ 0x656e4a6e, "snprintf" },
	{ 0xa6d82ce1, "netlink_unicast" },
	{ 0x9166fada, "strncpy" },
	{ 0x6b7abfff, "__nlmsg_put" },
	{ 0x723f78ae, "__alloc_skb" },
	{ 0x754d539c, "strlen" },
	{ 0xea8a0879, "tcp_reno_undo_cwnd" },
	{ 0xfda9581f, "prandom_u32" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0xacdaef45, "kmem_cache_alloc_trace" },
	{ 0xe7d7e16f, "kmalloc_caches" },
	{ 0x15ba50a6, "jiffies" },
	{ 0x37a0cba, "kfree" },
	{ 0xdecd0b29, "__stack_chk_fail" },
	{ 0x41ed3709, "get_random_bytes" },
	{ 0xc5850110, "printk" },
	{ 0xbdfb6dbb, "__fentry__" },
=======
	{ 0x49691ab3, "module_layout" },
	{ 0xf96ee445, "kmalloc_caches" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0x1fdc7df2, "_mcount" },
	{ 0x71ce3f39, "param_ops_int" },
	{ 0x98cf60b3, "strlen" },
	{ 0x7fccc099, "__ubsan_handle_load_invalid_value" },
	{ 0x7b37b558, "__ubsan_handle_type_mismatch_v1" },
	{ 0x41ed3709, "get_random_bytes" },
	{ 0x56470118, "__warn_printk" },
	{ 0xedfbf652, "__ubsan_handle_shift_out_of_bounds" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xe5c51729, "__ubsan_handle_divrem_overflow" },
	{ 0xc5850110, "printk" },
	{ 0x386e1c62, "tcp_register_congestion_control" },
	{ 0xaedc24d7, "netlink_kernel_release" },
	{ 0x9166fada, "strncpy" },
	{ 0xeb56395e, "netlink_unicast" },
	{ 0xfda9581f, "prandom_u32" },
	{ 0x21a079f8, "init_net" },
	{ 0x332b73a1, "__ubsan_handle_out_of_bounds" },
	{ 0xb3c8c318, "tcp_unregister_congestion_control" },
	{ 0xab477748, "__alloc_skb" },
	{ 0xdecd0b29, "__stack_chk_fail" },
	{ 0xb384ca2e, "cpu_hwcap_keys" },
	{ 0xa9bb8ca3, "tcp_reno_ssthresh" },
	{ 0xc7f88d29, "tcp_cong_avoid_ai" },
	{ 0xb911bb58, "minmax_running_max" },
	{ 0x8a2eaf5c, "kmem_cache_alloc_trace" },
	{ 0x9adc6860, "__netlink_kernel_create" },
	{ 0x44d2e8f8, "tcp_slow_start" },
	{ 0x37a0cba, "kfree" },
	{ 0x4cab7e73, "tcp_reno_undo_cwnd" },
	{ 0x656e4a6e, "snprintf" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0xc25a198, "__nlmsg_put" },
	{ 0x14b89635, "arm64_const_caps_ready" },
	{ 0xdf71daad, "tcp_reno_cong_avoid" },
>>>>>>> be8a8ec201dda079c8a10daab8e90c9d7771800d
};

MODULE_INFO(depends, "");


<<<<<<< HEAD
MODULE_INFO(srcversion, "41CCC4DE1397EB231929DF0");
=======
MODULE_INFO(srcversion, "1AF6F4D0F72A3A47AD147FD");
>>>>>>> be8a8ec201dda079c8a10daab8e90c9d7771800d
