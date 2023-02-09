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
	{ 0x49691ab3, "module_layout" },
	{ 0x71ce3f39, "param_ops_int" },
	{ 0xace21714, "tcp_unregister_congestion_control" },
	{ 0xaedc24d7, "netlink_kernel_release" },
	{ 0x2bbd90d8, "tcp_register_congestion_control" },
	{ 0x9adc6860, "__netlink_kernel_create" },
	{ 0x21a079f8, "init_net" },
	{ 0x7fccc099, "__ubsan_handle_load_invalid_value" },
	{ 0x2d7a483b, "tcp_reno_cong_avoid" },
	{ 0x332b73a1, "__ubsan_handle_out_of_bounds" },
	{ 0x7b37b558, "__ubsan_handle_type_mismatch_v1" },
	{ 0xed16e127, "tcp_cong_avoid_ai" },
	{ 0x7f02188f, "__msecs_to_jiffies" },
	{ 0x59e85da3, "tcp_slow_start" },
	{ 0xe5c51729, "__ubsan_handle_divrem_overflow" },
	{ 0xb384ca2e, "cpu_hwcap_keys" },
	{ 0x14b89635, "arm64_const_caps_ready" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0xa209e489, "tcp_reno_undo_cwnd" },
	{ 0xfda9581f, "prandom_u32" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xdecd0b29, "__stack_chk_fail" },
	{ 0xc5850110, "printk" },
	{ 0x3854774b, "kstrtoll" },
	{ 0x4b990136, "tcp_reno_ssthresh" },
	{ 0x1fdc7df2, "_mcount" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "89131ACE6A86B92A6E6925E");
