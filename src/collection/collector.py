import yaml
import time
from collection.kernel_comm import CollectionCommManager
from comm.kernel_thread import KernelRequest

class Collector():
    """ Collector class
    The collector runs a data collection campaign by running a specific protocol for a predefined time period.
    It setup a communication with Mutant kernel module (client) to collect the traffic data (network statistics).
    The data collected are stored locally as a csv file.

    Inputs: protocol, data collection time (running_time).
    Output: csv file of data collected
    """

    def __init__(self, protocol, running_time):
        self.cm = CollectionCommManager(protocol, 'log/collection') #iperf_dir, time
        self.proto = protocol
        self.running_time = running_time
        # TODO: handle the params with a config file
        with open('config/train.yml', 'r') as file:
            config = yaml.safe_load(file)

        self.num_fields_kernel = config['num_fields_kernel']
        self.initiated = False
        self._init_communication()

    def setup_communication(self):
        # Set up iperf client-server communication
        # Now a single flow between client and server is running
        # We can now set up the runner and start training the RL model    
        self.cm.init_kernel_communication()
        self.cm.start_communication(client_tag='test', server_log_dir='log/collection')

    def stop_communication(self):
        self.cm.stop_iperf_communication()
        self.cm.close_kernel_communication()
        self.kernel_thread.exit()

    def _init_communication(self):
        # Start thread to communicate with kernel

        if not self.initiated:
            print("Start kernel thread...")

            # Thread for kernel info
            self.kernel_thread = KernelRequest(
                self.cm.netlink_communicator, self.num_fields_kernel)

            self.kernel_thread.start()

            print("Kernel thread started.")
            self.initiated = True

    def _read_data(self):
        kernel_info = self.kernel_thread.queue.get()
        self.kernel_thread.queue.task_done()
        return kernel_info
    
    # def _recv_data(self):
    #     msg = self.cm.netlink_communicator.recv_msg()
    #     data = self.cm.netlink_communicator.read_netlink_msg(msg)
    #     split_data = data.decode(
    #         'utf-8').split(';')[:self.num_fields_kernel]
    #     return list(map(int, split_data))

    def run_collection(self):
        """ 
        TODO: we want to receive network parameters from the kernel side. In order to do that, we run a thread which is in charge of 
        communicating in real time with the kernel module. During the communication, the thread receive the "message" from the kernel 
        module, containing the network information, and store everything locally.
        """

        collected_data = {}
        start = time.time()
        while time.time()-start < self.running_time:
            data = self._read_data()
            collected_data = {
            'now': data[0],
            'cwnd': data[1],
            'rtt': data[2],
            'rtt_dev': data[3],
            'MSS': data[4],
            'delivered': data[5],
            'lost': data[6],
            'in_flight': data[7],
            'retransmitted': data[8]
            }

            print("Collected data:", ", ".join(f"{key}: {value}" for key, value in collected_data.items()))


        

        
    
