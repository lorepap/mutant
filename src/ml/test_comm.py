# USER-SPACE MIMIC SENDER TEST
import time
from argparse import ArgumentParser
from network.netlink_communicator import NetlinkCommunicator
from network.kernel_feedback import KernelRequest

NETLINK_TEST = 25

def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--prot", default=0)
    args = parser.parse_args()
    prot = int(args.prot)

    netcomm = NetlinkCommunicator()

    print("Initiating communication...")

    # Thread for kernel info
    kernel_thread = KernelRequest(
        netcomm, num_fields_kernel=10)

    kernel_thread.start()

    print("Communication initiated")

    # Initiate communication
    msg = netcomm.create_netlink_msg(
        'INIT', msg_flags=netcomm.INIT_COMM_FLAG, msg_seq=int(args.prot))
    netcomm.send_msg(msg)    
    start = time.time()
    while (True):
        params = kernel_thread.queue.get()
        print("[RECEIVED DATA]\n")
        print(params)
        if (time.time()-start > 5):
            prot=(prot+1)%2
            print("[DEBUG] Selected protocol:", prot)
            msg = netcomm.create_netlink_msg(
                'ACTION', msg_flags=netcomm.ACTION_FLAG, msg_seq=prot)
            netcomm.send_msg(msg)
            start = time.time()
    
if __name__=="__main__":
    main()