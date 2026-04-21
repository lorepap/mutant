ifneq ($(KERNELRELEASE),)
obj-m   := mutant.o
else
KDIR    := /lib/modules/$(shell uname -r)/build 
PWD     := $(shell pwd)
MY_CFLAGS += -g -DDEBUG

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

debug:
	$(MAKE) -C $(KDIR) M=$(PWD) modules EXTRA_CFLAGS="$(MY_CFLAGS)"

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install

%:
	$(MAKE) -C $(KDIR) M=$(PWD) $@

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

endif
