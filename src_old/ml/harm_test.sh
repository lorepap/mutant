# Create the first network interface with congestion control algorithm CCA1
mm-dummy-netem --delay 20 --downlink-queue="droptail" --downlink-queue-args="packets=100" --downlink-queue-args="bytes=1000000" --congestion-control="bbr" -- sh -c 'ip route add default via 192.168.0.1 dev dummy0'

# Create the second network interface with congestion control algorithm CCA2
mm-dummy-netem --delay 20 --downlink-queue="droptail" --downlink-queue-args="packets=100" --downlink-queue-args="bytes=1000000" --congestion-control="cubic" -- sh -c 'ip route add default via 192.168.0.1 dev dummy1'

# Create the common link
mm-link config --downlink-queue="droptail" --downlink-queue-args="packets=100" --downlink-queue-args="bytes=1000000" -- sh -c 'ip route add default via 192.168.0.1 dev eth0'

# Start the server
iperf -s -p 5201 &

# Start the client with CCA1
iperf -c server_ip -p 5201 -t 10 &

# Start the client with CCA2
iperf -c server_ip -p 5201 -t 10 &

# Wait for the iperf tests to complete
wait

# Cleanup
killall iperf
mm-dummy-netem --cleanup
