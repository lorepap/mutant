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
	{ 0x4142e96d, "module_layout" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0x4e82243e, "param_ops_int" },
	{ 0x754d539c, "strlen" },
	{ 0x56470118, "__warn_printk" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xc5850110, "printk" },
	{ 0x346581a8, "tcp_register_congestion_control" },
	{ 0xdd453c3e, "netlink_kernel_release" },
	{ 0x9166fada, "strncpy" },
	{ 0xa6d82ce1, "netlink_unicast" },
	{ 0xfda9581f, "prandom_u32" },
	{ 0x33cd4d84, "init_net" },
	{ 0x6a70c480, "tcp_unregister_congestion_control" },
	{ 0x723f78ae, "__alloc_skb" },
	{ 0xdecd0b29, "__stack_chk_fail" },
	{ 0x2ea2c95c, "__x86_indirect_thunk_rax" },
	{ 0xdee4abea, "tcp_reno_ssthresh" },
	{ 0xbb9356bf, "tcp_cong_avoid_ai" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0xb911bb58, "minmax_running_max" },
	{ 0xf005b060, "__netlink_kernel_create" },
	{ 0x76ec4752, "tcp_slow_start" },
	{ 0xea8a0879, "tcp_reno_undo_cwnd" },
	{ 0x656e4a6e, "snprintf" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x6b7abfff, "__nlmsg_put" },
	{ 0x92928499, "tcp_reno_cong_avoid" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "069781ADC02B06CB006F10E");
