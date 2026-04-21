# Linux 5.4.231 Patch Installation

Mutant requires the patched Linux 5.4.231 kernel included in this repository as `linux-5.4.231-mutant.patch`.

## Prerequisites

- Ubuntu 20.04 or a similar distribution
- enough disk space and build time for a full kernel build
- the packages needed for kernel compilation

Install dependencies:

```bash
sudo apt update
sudo apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev dwarves
```

## 1. Download the kernel source

```bash
cd ~
wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.4.231.tar.xz
tar -xf linux-5.4.231.tar.xz
cd linux-5.4.231
```

## 2. Apply the Mutant patch

Run the patch from the root of the unpacked kernel tree:

```bash
patch -p1 < /path/to/mutant-master/linux/linux-5.4.231-mutant.patch
```

If `patch` reports rejected hunks, stop there and resolve them before continuing. The module sources in `src/kernel/` assume this patch is present.

## 3. Configure the patched kernel

Start from your current kernel config:

```bash
cp /boot/config-$(uname -r) .config
make olddefconfig
```

Use `make menuconfig` only if you need to adjust additional options.

## 4. Build and install

```bash
make -j"$(nproc)"
sudo make modules_install
sudo make install
sudo update-grub
```

## 5. Reboot into the patched kernel

```bash
sudo reboot
```

After the machine comes back:

```bash
uname -r
```

Confirm the running kernel is the patched 5.4.231 build you just installed.

## 6. Build and load the Mutant module

Once the patched kernel is active, return to this repository and run:

```bash
./init_kernel.sh
```

That script loads the required TCP modules, builds `mutant.ko`, inserts it, and selects `mutant` as the active congestion control.
