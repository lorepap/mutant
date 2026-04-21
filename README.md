# Mutant Kernel Components

- the Linux 5.4.231 patch in `linux/linux-5.4.231-mutant.patch`
- the out-of-tree module sources in `src/kernel/`
- helper scripts to load the required TCP modules and enable `mutant`

## Contents

- `linux/readme.MD`: detailed kernel patch and kernel build instructions
- `src/kernel/`: `mutant` kernel module source and Makefile
- `ins_proto.sh`: loads the TCP congestion-control modules Mutant wraps
- `init_kernel.sh`: builds and inserts `mutant.ko`, then selects it via `sysctl`

## Install the Patched Kernel

Mutant depends on a patched Linux 5.4.231 tree. Build and install that kernel first.

1. Install the build dependencies:

```bash
sudo apt update
sudo apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev dwarves
```

2. Download and unpack Linux 5.4.231:

```bash
cd ~
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.4.231.tar.xz
tar -xf linux-5.4.231.tar.xz
```

3. Apply the patch from inside the kernel source tree:

```bash
cd ~/linux-5.4.231
patch -p1 < /path/to/mutant-master/linux/linux-5.4.231-mutant.patch
```

4. Reuse your current kernel config, then prepare and build:

```bash
cp /boot/config-$(uname -r) .config
make olddefconfig
make -j"$(nproc)"
```

5. Install the kernel and reboot into it:

```bash
sudo make modules_install
sudo make install
sudo update-grub
sudo reboot
```

After reboot, confirm you are running the patched 5.4.231 kernel before building the module.

## Build and Load the Mutant Module

From this repository:

```bash
./init_kernel.sh
```

That script:

- loads the patched TCP congestion-control modules with `modprobe`
- rebuilds `src/kernel/mutant.ko`
- unloads any existing `mutant` instance
- inserts the new module
- sets `net.ipv4.tcp_congestion_control=mutant`

Verify the active congestion control:

```bash
sysctl net.ipv4.tcp_congestion_control
```

The result should be `net.ipv4.tcp_congestion_control = mutant`.
```
