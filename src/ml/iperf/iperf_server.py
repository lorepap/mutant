import subprocess

class IperfServer:
    def __init__(self):
        self._server_proc = None
        self._server_log_file = "server.log"

    def start(self):
        if self._server_proc is not None:
            raise Exception("Server already running")

        server_cmd = ["iperf3", "-s", "--logfile", self._server_log_file]
        self._server_proc = subprocess.Popen(server_cmd, shell=False)

        print("Server started with PID:", self._server_proc.pid)

    def stop(self):
        if self._server_proc is not None:
            self._server_proc.terminate()
            self._server_proc.wait()
            self._server_proc = None
            print("Server stopped")
        else:
            print("Server not running")

    def restart(self):
        self.stop()
        self.start()
