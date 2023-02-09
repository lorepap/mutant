from analysis.models.protocol import Protocol
from models.trace import MiTrace
from datetime import datetime
from helper import utils


class Experiment():

    def __init__(self, trace: MiTrace, protocol: Protocol) -> None:
        self._trace = trace
        self._protocol = protocol
        self.format = utils.TIME_FORMAT


    def get_tag(self) -> str:

        return f'{self._trace}.{self._protocol}'

    def get_configuration(self, date: datetime) -> dict:
        config = {}

        iperf_log = f'{self._protocol}_iperf'
        log = f'{self._protocol}'

        iperf_logs = []
        logs = []

        config[iperf_log] = iperf_logs
        config[log] = logs

        return config
