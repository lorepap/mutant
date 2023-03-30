import threading
import traceback

from helper.thesis import *
from helper.utils import *


class ThesisPlotRunner(threading.Thread):

    def __init__(self, config: dict) -> None:
        threading.Thread.__init__(self)

        self.__config = config

    def run(self) -> None:

        try:
            self.plot()
        
        except Exception as _:
            print("\n")
            print(traceback.format_exc())


    def plot(self) -> None:
        # ts_throughput_latency_all(self.__config)
        # ts_throughput(self.__config)
        # ts_cdf_latency_all(self.__config)
        # ts_cdf_throughput_all(self.__config)

        # ts_throughput_latency_policies(self.__config)

        # ts_throughput_latency_last(self.__config)
        ts_throughput_latency_mean(self.__config)

        # ts_protocol_selected(self.__config)
        # ts_model_selected(self.__config)

        # ts_protocol_selected_throughput(self.__config)
        # ts_protocol_selected_cwnd(self.__config)
        # ts_protocol_selected_metric(self.__config)
        # ts_protocol_selected_metric_multi(self.__config)

        # ts_arms_total_picks(self.__config)

        # ts_reward(self.__config)
        # ts_reward_error(self.__config)
