#!/usr/bin/env python3

from runner.thesis_runner import ThesisPlotRunner
from helper.utils import *
from helper.arm import *
from helper.cwnd import *
from helper.exp import *
from helper.latency import *
from helper.loss import *
from helper.mape import *
from helper.misc import *
from helper.throughput import *
from helper.protocol import *
from helper.reward import *
from helper.iperf import *
from helper.cdf import *
from helper.thesis import *

import traceback


def get_config(trace: str = 'vz.lte.short') -> dict:

    # experiment = get_verizon_exp()

    experiment = get_tmobile_exp()

    # experiment = get_wifi_exp()

    # experiment = get_less_loss_exp()

    # experiment = get_mininet_exp()

    # experiment = get_policy_exp()

    # experiment = get_prod_exp(trace)

    # experiment = get_prod_exp_verbose(trace)

    return experiment


def prod_plots(experiment: dict) -> None:

    # plot_prod_cwnd(experiment)

    # plot_model_selected(experiment)

    # plot_prod_throughput_latency_v2(experiment)

    # plot_prod_throughput_latency(experiment)

    # plot_protocol_selected(experiment)

    # plot_prod_arms_total_picks(experiment)

    # plot_prod_throughput(experiment)

    # plot_prod_throughput(experiment, True)

    # plot_prod_cwnd_diff(experiment)

    # plot_prod_reward(experiment)

    # plot_prod_cwnd_model(experiment)

    # plot_prod_loss_all_arms(experiment)

    # plot_prod_throughput_loss(experiment)

    # plot_prod_latency_multi(experiment)
    # plot_prod_latency(experiment)

    # plot_prod_throughput_multi(experiment)
    # plot_prod_throughput_v1(experiment)

    # plot_prod_throughput_latency_best(experiment)

    plot_iperf_throughput_latency_mean(experiment)
    # plot_iperf_throughput_latency_min(experiment)
    # plot_iperf_throughput_latency_max(experiment)
    # plot_iperf_cwnd(experiment)
    # plot_iperf_cwnd_multi(experiment)
    # plot_iperf_latency(experiment)
    # plot_iperf_latency_multi(experiment)
    # plot_iperf_throughput(experiment)
    # plot_iperf_throughput_multi(experiment)

    # plot_cdf_throughput_multi(experiment)
    # plot_cdf_latency_multi(experiment)
    # plot_cdf_latency(experiment)
    # plot_cdf_throughput(experiment)

    # plot_cdf_latency_all(experiment)
    # plot_cdf_throughput_all(experiment)

    # ts_throughput(experiment)
    # ts_throughput_orca(experiment)
    # ts_cdf_latency_all(experiment)
    # ts_cdf_throughput_all(experiment)

    # ts_throughput_latency_last(experiment)
    # ts_throughput_latency_mean(experiment)
    # ts_throughput_latency_orca(experiment)

    # ts_protocol_selected(experiment, 'rtt')
    # ts_protocol_selected(experiment, 'bw')
    # ts_protocol_selected(experiment, 'cwnd')
    # ts_protocol_selected(experiment, 'throughput')
    # ts_protocol_selected(experiment)

    # ts_model_selected(experiment)

    # ts_protocol_selected_throughput(experiment)
    # ts_protocol_selected_cwnd(experiment)
    # ts_protocol_selected_metric(experiment)
    # ts_protocol_selected_metric_multi(experiment)

    # ts_protocol_total_picks(experiment)
    # ts_model_total_picks(experiment)

    # ts_reward(experiment)
    # ts_reward_error(experiment)

    ts_reward_error_policies(experiment)
    pass


def main() -> None:

    utils.check_output(['sudo', 'updatedb'])

    experiment = get_config()

    csv_files = ['2021.06.30.09.59.25.csv',
                 '2021.06.30.10.31.57.csv',
                 '2021.06.30.10.57.09.csv',
                 '2021.06.30.11.16.43.csv',
                 '2021.06.30.11.37.02.csv',
                 '2021.07.05.22.02.53.csv',
                 '2021.07.05.22.49.26.csv',
                 '2021.07.05.23.57.15.csv',
                 '2021.07.06.18.04.37.csv',
                 '2021.07.06.19.13.35.csv',
                 '2021.07.06.19.39.02.csv']

    csv_file_names = ['Bootstrapped Upper-Confidence Bound',
                      'Bootstrapped Thompson Sampling',
                      'Separate Classifiers with Beta Prior',
                      'Epsilon-Greedy with decay',
                      'Epsilon-Greedy without decay',
                      'Adaptive Greedy with decaying threshold',
                      'Adaptive Greedy with decaying percentile',
                      'Explore First with explore rounds',
                      'Active Explorer',
                      'Adaptive Active Greedy',
                      'Softmax Explorer']

    # for i in range(len(csv_files)):
    #     policy = csv_file_names[i]
    #     run_file = csv_files[i]
    #     csv_file = os.path.join(base_path, 'log/mab/trace', run_file)

    #     columns = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
    #             'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    #     df = pd.read_csv(csv_file, names=columns)

    #     # plot_scatter(df, policy)

    #     plot_cwnd(df, policy)

    #     plot_reward(df, policy)

    #     plot_reward_evolution(df, policy)

    #     plot_arms(df, policy)

    # plot_all_cwnd(csv_files, csv_file_names)

    # plot_all_reward(csv_files, csv_file_names)

    # plot_error()

    # Plot arms
    # plot_arm_cwnd('cubic.2021.07.26.00.59.01.csv', 'Verizon-LTE-short.up', 'Cubic')
    # plot_arm_cwnd('hybla.2021.07.27.23.14.10.csv', 'Verizon-LTE-short.up', 'Hybla')
    # plot_arm_cwnd('vegas.2021.07.27.01.13.53.csv', 'Verizon-LTE-short.up', 'Vegas')
    # plot_arm_cwnd('AdaptiveGreedy.2021.08.25.02.25.56.csv', 'Verizon-LTE-short.up', 'Mab')
    # plot_arm_cwnd('owl.2021.08.04.09.45.09.csv', 'Verizon-LTE-short.up', 'Owl', owl_columns, owl_path)
    # plot_cwnd_all_arms(experiment)
    # plot_cwnd_all_arms_diff(experiment)
    # plot_cwnd_all_arms_multi(experiment)
    # plot_cwnd_all_arms_multi_diff(experiment)
    # plot_cwnd_all_arms_multi_aoc(experiment, False)
    # plot_cwnd_all_arms_multi_aoc(experiment, True)
    # plot_cwnd_follow_multi(experiment)
    # plot_cwnd_follow(experiment, 'hybla')
    # plot_cwnd_all_policies(experiment)

    # Plot bandwidths
    # plot_arm_bandwidth('Verizon-LTE-short.up', 'Verizon-LTE-short.up')

    # Plot throughput
    # plot_throughput_multi(experiment, False)
    # plot_throughput(experiment)
    # plot_throughput_latency_multi(experiment)
    # plot_throughput_loss_scatter(experiment)
    # plot_throughput_latency_scatter(experiment)
    # plot_throughput_follow_multi(experiment)
    # plot_policies_throughput_latency_scatter(experiment)
    # plot_policies_throughput_latency_scatter(experiment, True)

    # Plot latency
    # plot_latency(experiment)
    # plot_latency_multi(experiment)
    # plot_latency_throughput_multi(experiment)

    # Plot packet lost
    # plot_loss_all_arms_multi(experiment)
    # plot_loss_all_arms(experiment)

    # Plot policies
    # plot_arm_all_policies(experiment, 10)
    # plot_arm_all_policies_multi(experiment, 10)
    # plot_arm_all_policies_multi(experiment, 50)
    # plot_arm_all_policies_multi(experiment, 100)
    # plot_arm_all_policies_multi(experiment, 500)
    # plot_arms_total_picks(experiment)

    # Plot mAPE
    # plot_mape_arms(experiment)

    # plot_all_multi(experiment)
    # plot_all(experiment, 'mimic')

    # Plot PROD
    # prod_plots(get_prod_exp('att.lte.driving'))
    # prod_plots(get_prod_exp('att.lte.driving.2016'))
    # prod_plots(get_prod_exp('tm.umts.driving'))
    # prod_plots(get_prod_exp('tm.lte.short'))
    # prod_plots(get_prod_exp('vz.lte.short'))
    # prod_plots(get_prod_exp('vz.evdo.driving'))
    # prod_plots(get_prod_exp('vz.lte.driving'))

    # prod_plots(get_prod_exp_verbose('vz.lte.short'))
    # prod_plots(get_prod_exp_verbose('att.lte.driving'))
    # prod_plots(get_prod_exp_verbose('tm.lte.short'))

    # prod_plots(get_prod_musketeers('vz.lte.short'))
    # prod_plots(get_prod_musketeers('att.lte.driving'))
    # prod_plots(get_prod_musketeers('tm.lte.short'))

    # ts_protocol_total_picks(get_prod_musketeers('vz.lte.short'))
    # ts_protocol_total_picks(get_prod_musketeers('att.lte.driving'))
    # ts_protocol_total_picks(get_prod_musketeers('tm.lte.short'))

    # ts_model_total_picks(get_prod_musketeers('vz.lte.short'))
    # ts_model_total_picks(get_prod_musketeers('att.lte.driving'))
    # ts_model_total_picks(get_prod_musketeers('tm.lte.short'))

    # ts_protocol_selected(get_prod_musketeers('vz.lte.short'), 'bw')
    # ts_protocol_selected(get_prod_musketeers('att.lte.driving'), 'bw')
    # ts_protocol_selected(get_prod_musketeers('tm.lte.short'), 'bw')
    

    # ts_throughput_latency_mean(get_prod_musketeers('att.lte.driving'))
    # ts_throughput_latency_mean(get_prod_musketeers('tm.lte.short'))
    # ts_throughput_latency_mean(get_prod_musketeers('vz.lte.short'))

    # ts_throughput_latency_all(get_prod_musketeers('vz.lte.short'))
    # ts_throughput_latency_all(get_prod_musketeers('att.lte.driving'))
    # ts_throughput_latency_all(get_prod_musketeers('tm.lte.short'))

    # ts_throughput_latency_orca(get_orca('bus'))
    # ts_throughput_latency_orca(get_orca('timessquare'))
    # ts_throughput_latency_orca(get_orca('wired'))

    # ts_reward_error_policies(get_policy_exp('vz.lte.short'))
    # ts_reward_error_policies(get_policy_exp('att.lte.driving'))
    ts_reward_error_policies(get_policy_exp('tm.lte.short'))

    # ts_throughput_latency_policies(get_policy_iperf('vz.lte.short'))
    # ts_throughput_latency_policies(get_policy_iperf('att.lte.driving'))
    # ts_throughput_latency_policies(get_policy_iperf('tm.lte.short'))

    # plot_protocol_selected_dir(os.path.join(utils.entry_path, 'log/iperf/protocol'))

    # ts_harm_throughput(
    #     get_harm_iperf('att.lte.driving'), 
    #     get_harm_iperf('tm.lte.short'), 
    #     get_harm_iperf('vz.lte.short'))
    
    # ts_harm_delay(
    #     get_harm_iperf('att.lte.driving'), 
    #     get_harm_iperf('tm.lte.short'), 
    #     get_harm_iperf('vz.lte.short'))


    # ts_throughput_latency_all(get_geni_illinois_iperf())
    # ts_throughput_latency_all(get_geni_stanford_iperf())
    # ts_throughput_latency_all(get_geni_washington_iperf())


if __name__ == '__main__':

    try:
        main()

    except Exception as err:
        print('\n')
        print(traceback.format_exc())
