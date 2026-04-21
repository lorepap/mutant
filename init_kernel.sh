#!/bin/bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
kernel_dir="$script_dir/src/kernel"

"$script_dir/ins_proto.sh"

cd "$kernel_dir"
echo ''
echo '--- Building mutant kernel module ---'
echo ''
make clean
make

if lsmod | grep -q '^mutant\b'; then
    echo '--- Removing existing mutant module ---'
    sudo rmmod mutant
fi

echo '--- Inserting mutant kernel module ---'
echo ''
# Uncomment the following line if your platform requires module signing.
# sudo /usr/src/linux-$(uname -r)/scripts/sign-file sha256 ./key/MOK.priv ./key/MOK.der mutant.ko
sudo insmod mutant.ko

echo ''
echo '--- Selecting mutant as the active congestion control ---'
echo ''
sudo sysctl -w net.ipv4.tcp_congestion_control=mutant
