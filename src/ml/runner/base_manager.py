import threading
from typing import Any

from helper import utils
from network.kernel_feedback import KernelRequest
from network.netlink_communicator import NetlinkCommunicator


class BaseManager(threading.Thread):

    def __init__(self, iperf_logfile: str) -> None:
        threading.Thread.__init__(self)

        self.allow_run = True
        self.log_traces = ''
        self.log_traces_verbose = ''
        self.iperf_logfile = iperf_logfile

        # Thread for kernel info
        self.kernel_thread: KernelRequest = None

    def save_log(self) -> Any:
        raise NotImplementedError()

    def save_log_verbose(self) -> Any:
        raise NotImplementedError()

    def exit(self) -> None:
        self.allow_run = False
        logfile, _ = self.save_log()
        self.save_log_verbose()
        self.log_traces = ''
        self.log_traces_verbose = ''
        self.kernel_thread.exit()

        self.update_iperf_log(logfile)

    def update_iperf_log(self, new_name: str) -> None:

        new_logfilename = new_name.replace("csv", "json")
        iperfList = self.iperf_logfile.split("/")
        iperfList[len(iperfList) - 1] = new_logfilename
        new_logfilepath = "/".join(iperfList)

        utils.change_file_name(self.iperf_logfile, new_logfilepath)
