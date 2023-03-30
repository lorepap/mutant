from copy import deepcopy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *
import random
from random import seed


def plot_prod_throughput_multi(cf: dict):
    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mimic'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    df_basic = to_dataframe_prod(config['basic'], path='log/basic')
    x_basic, y_basic, _ = get_plot_xyz(df_basic, 'throughput', config, bws)

    fig = plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_xlabel('Step')
    ax1.set_title(f'{config["trace"]} | Throughput vs Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Throughput (Mbps)')
    ax2.set_xlabel('Step')
    ax2.set_title(f'{config["trace"]} | Throughput vs Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Step')
    ax3.set_title(f'{config["trace"]} | Throughput vs Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Throughput (Mbps)')
    ax4.set_xlabel('Step')
    ax4.set_title(f'{config["trace"]} | Throughput vs Step')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab, y_mab, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Throughput (Mbps)')
    ax5.set_xlabel('Step')
    ax5.set_title(f'{config["trace"]} | Throughput vs Step')
    ax5.legend()

    ax6 = plt.subplot(326)
    ax6.plot(x_basic, y_basic, label='Basic', color='#ff7f0e')
    ax6.set_ylabel('Throughput (Mbps)')
    ax6.set_xlabel('Step')
    ax6.set_title(f'{config["trace"]} | Throughput vs Step')
    ax6.legend()

    plt.title('')

    file_name = f'{config["trace"]}.throughput.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_prod_throughput_v1(cf: dict):
    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mimic'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic, label='Cubic')
    ax.plot(x_hybla, y_hybla, label='Hybla')
    ax.plot(x_vegas, y_vegas, label='Vegas')
    ax.plot(x_owl, y_owl, label='Owl')
    ax.plot(x_mab, y_mab, label='Mimic')

    plt.xlabel('Step')
    plt.ylabel('Throughput (Mbps)')
    plt.title(f'{config["trace"]} | Throughput vs Step')
    plt.legend()

    file_name = f'{config["trace"]}.v1.throughput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_throughput_loss_scatter(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []
    # bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else [] if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'lost', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'lost', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'lost', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mab'])
    _, x_mab, _ = get_plot_xyz(df_mab, 'lost', config, bws)
    _, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    _, x_owl, _ = get_plot_xyz(df_owl, 'lost', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    x = [np.mean(x_cubic), np.mean(x_hybla), np.mean(x_vegas),
         np.mean(x_owl), np.mean(x_mab[0:y_mab.shape[0]])]
    y = [np.mean(y_cubic), np.mean(y_hybla), np.mean(
        y_vegas), np.mean(y_owl), np.mean(y_mab)]
    x_ticks = ['Cubic', 'Hybla', 'Vegas', 'Owl', 'Mimic']

    N = len(x)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

    ax.scatter(x, y, c=colors)

    for i in range(N):
        plt.text(x[i], y[i], x_ticks[i])

    plt.xlabel('Packet Loss (ln)')
    plt.ylabel('Throughput (Mbps)')

    file_name = f'{config["trace"]}.arms.scatter_throughput_loss.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/throughput', file_name)

    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_throughput_latency_scatter(config: dict):

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mab'])
    _, x_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)
    _, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    _, x_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    x = [np.mean(x_cubic), np.mean(x_hybla), np.mean(x_vegas),
         np.mean(x_owl), np.mean(x_mab[0:y_mab.shape[0]])]
    y = [np.mean(y_cubic), np.mean(y_hybla), np.mean(
        y_vegas), np.mean(y_owl), np.mean(y_mab)]
    x_ticks = ['Cubic', 'Hybla', 'Vegas', 'Owl', 'Mimic']

    N = len(x)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

    ax.scatter(x, y, c=colors)

    for i in range(N):
        plt.text(x[i], y[i], x_ticks[i])

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.xlabel('Latency (s)')
    plt.ylabel('Throughput (Gbps)')

    file_name = f'{config["trace"]}.arms.scatter_throughput_latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots/throughput', file_name)

    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_policies_throughput_latency_scatter(config: dict, error: bool = False):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_x1 = to_dataframe_prod(config['ActiveExplorer'])
    _, x1, _ = get_plot_xyz(df_x1, 'rtt', config, bws)
    _, y1, _ = get_plot_xyz(df_x1, 'throughput', config, bws)
    yerr1 = CI_model(y1)
    xerr1 = CI_model(x1)

    df_x2 = to_dataframe_prod(config['AdaptiveGreedyWithPercentile'])
    _, x2, _ = get_plot_xyz(df_x2, 'rtt', config, bws)
    _, y2, _ = get_plot_xyz(df_x2, 'throughput', config, bws)
    yerr2 = CI_model(y2)
    xerr2 = CI_model(x2)

    df_x3 = to_dataframe_prod(config['AdaptiveGreedyWithThreshold'])
    _, x3, _ = get_plot_xyz(df_x3, 'rtt', config, bws)
    _, y3, _ = get_plot_xyz(df_x3, 'throughput', config, bws)
    yerr3 = CI_model(y3)
    xerr3 = CI_model(x3)

    df_x4 = to_dataframe_prod(config['BootstrappedTS'])
    _, x4, _ = get_plot_xyz(df_x4, 'rtt', config, bws)
    _, y4, _ = get_plot_xyz(df_x4, 'throughput', config, bws)
    yerr4 = CI_model(y4)
    xerr4 = CI_model(x4)

    df_x5 = to_dataframe_prod(config['BootstrappedUCB'])
    _, x5, _ = get_plot_xyz(df_x5, 'rtt', config, bws)
    _, y5, _ = get_plot_xyz(df_x5, 'throughput', config, bws)
    yerr5 = CI_model(y5)
    xerr5 = CI_model(x5)

    df_x6 = to_dataframe_prod(config['EpsilonGreedyWithDecay'])
    _, x6, _ = get_plot_xyz(df_x6, 'rtt', config, bws)
    _, y6, _ = get_plot_xyz(df_x6, 'throughput', config, bws)
    yerr6 = CI_model(y6)
    xerr6 = CI_model(x6)

    df_x7 = to_dataframe_prod(config['EpsilonGreedyWithoutDecay'])
    _, x7, _ = get_plot_xyz(df_x7, 'rtt', config, bws)
    _, y7, _ = get_plot_xyz(df_x7, 'throughput', config, bws)
    yerr7 = CI_model(y7)
    xerr7 = CI_model(x7)

    df_x8 = to_dataframe_prod(config['SeparateClassifiers'])
    _, x8, _ = get_plot_xyz(df_x8, 'rtt', config, bws)
    _, y8, _ = get_plot_xyz(df_x8, 'throughput', config, bws)
    yerr8 = CI_model(y8)
    xerr8 = CI_model(x8)

    df_x9 = to_dataframe_prod(config['cubic'])
    _, x9, _ = get_plot_xyz(df_x9, 'rtt', config, bws)
    _, y9, _ = get_plot_xyz(df_x9, 'throughput', config, bws)
    yerr9 = CI_model(y9)
    xerr9 = CI_model(x9)

    df_x10 = to_dataframe_prod(config['hybla'])
    _, x10, _ = get_plot_xyz(df_x10, 'rtt', config, bws)
    _, y10, _ = get_plot_xyz(df_x10, 'throughput', config, bws)
    yerr10 = CI_model(y10)
    xerr10 = CI_model(x10)

    df_x11 = to_dataframe_prod(config['vegas'])
    _, x11, _ = get_plot_xyz(df_x11, 'rtt', config, bws)
    _, y11, _ = get_plot_xyz(df_x11, 'throughput', config, bws)
    yerr11 = CI_model(y11)
    xerr11 = CI_model(x11)

    df_x12 = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    _, x12, _ = get_plot_xyz(df_x12, 'rtt', config, bws)
    _, y12, _ = get_plot_xyz(df_x12, 'throughput', config, bws)
    yerr12 = CI_model(y12)
    xerr12 = CI_model(x12)

    df_x13 = to_dataframe_prod(config['SoftmaxExplorer'])
    _, x13, _ = get_plot_xyz(df_x13, 'rtt', config, bws)
    _, y13, _ = get_plot_xyz(df_x13, 'throughput', config, bws)
    yerr13 = CI_model(y13)
    xerr13 = CI_model(x13)

    df_x14 = to_dataframe_prod(config['AdaptiveGreedyWeighted'])
    _, x14, _ = get_plot_xyz(df_x14, 'rtt', config, bws)
    _, y14, _ = get_plot_xyz(df_x14, 'throughput', config, bws)
    yerr14 = CI_model(y14)
    xerr14 = CI_model(x14)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    x = [np.mean(x1), np.mean(x2), np.mean(x3), np.mean(x4), np.mean(x5), np.mean(x6), np.mean(
        x7), np.mean(x8), np.mean(x9), np.mean(x10), np.mean(x11), np.mean(x12), np.mean(x13), np.mean(x14)]
    y = [np.mean(y1), np.mean(y2), np.mean(y3), np.mean(y4), np.mean(y5), np.mean(y6), np.mean(
        y7), np.mean(y8), np.mean(y9), np.mean(y10), np.mean(y11), np.mean(y12), np.mean(y13), np.mean(y14)]
    x_ticks = ['ActiveExplorer', 'AdaptiveGreedyWithPercentile', 'AdaptiveGreedyWithThreshold', 'BootstrappedTS', 'BootstrappedUCB',
               'EpsilonGreedyWithDecay', 'EpsilonGreedyWithoutDecay', 'SeparateClassifiers', 'Cubic', 'Hybla', 'Vegas', 'Owl', 'SoftmaxExplorer', 'AdaptiveGreedyWeighted']

    yerr_list = [yerr1, yerr2, yerr3, yerr4, yerr5, yerr6, yerr7,
                 yerr8, yerr9, yerr10, yerr11, yerr12, yerr13, yerr14]
    xerr_list = [xerr1, xerr2, xerr3, xerr4, xerr5, xerr6, xerr7,
                 xerr8, xerr9, xerr10, xerr11, xerr12, xerr13, xerr14]
    N = len(x)
    i = 0

    seed(1)

    color = ['red', 'blue', 'yellow', 'green', 'pink', 'grey', 'gold',
             'cyan', 'skyblue', 'violet', 'magenta', 'brown', 'olive', 'indigo']
    #  ,'black', 'silver', 'violet']

    for a, b in zip(x, y):
        if error:
            ax.errorbar(a, b, c=color[i], label=x_ticks[i],
                        yerr=yerr_list[i], xerr=xerr_list[i], fmt='o')
        else:
            ax.scatter(a, b, c=color[i], label=x_ticks[i])
        i += 1

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 1.25])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 10})

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.xlabel('Latency (s)')
    plt.ylabel('Throughput (Mbps)')

    if error:
        file_name = f'error.{config["trace"]}.arms.scatter_throughput_latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    else:
        file_name = f'{config["trace"]}.arms.scatter_throughput_latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/throughput', file_name)

    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_throughput_latency_multi(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mab'])
    _, x_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)
    _, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    _, x_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_xlabel('Latency (ln s)')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Throughput (Mbps)')
    ax2.set_xlabel('Latency (ln s)')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Latency (ln s)')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Throughput (Mbps)')
    ax4.set_xlabel('Latency (ln s)')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Throughput (Mbps)')
    ax5.set_xlabel('Latency (ln s)')
    ax5.legend()

    file_name = f'{config["trace"]}.multi.arms.throughput_latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/throughput', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_throughput_follow_multi(config: dict):
    config['step'] = 50
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_mab = to_dataframe_prod(config['mab'])
    df_mab_vegas = df_mab[df_mab['action'] == 0]
    df_mab_owl = df_mab[df_mab['action'] == 1]
    df_mab_cubic = df_mab[df_mab['action'] == 2]
    df_mab_hybla = df_mab[df_mab['action'] == 3]

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)
    x_mab_cubic, y_mab_cubic, _ = get_plot_xyz(
        df_mab_cubic, 'throughput', config, bws)
    y_cubic = y_cubic[0:y_mab_cubic.shape[0]]
    cubic_mape = mape(y_cubic, y_mab_cubic)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)
    x_mab_hybla, y_mab_hybla, _ = get_plot_xyz(
        df_mab_hybla, 'throughput', config, bws)
    y_hybla = y_hybla[0:y_mab_hybla.shape[0]]
    hybla_mape = mape(y_hybla, y_mab_hybla)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)
    x_mab_vegas, y_mab_vegas, _ = get_plot_xyz(
        df_mab_vegas, 'throughput', config, bws)
    y_vegas = y_vegas[0:y_mab_vegas.shape[0]]
    vegas_mape = mape(y_vegas, y_mab_vegas)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)
    x_mab_owl, y_mab_owl, _ = get_plot_xyz(
        df_mab_owl, 'throughput', config, bws)
    y_owl = y_owl[0:y_mab_owl.shape[0]]
    owl_mape = mape(y_owl, y_mab_owl)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_mab_cubic, y_cubic/mb, label=f'Cubic')
    ax1.plot(x_mab_cubic, y_mab_cubic/mb, label=f'Mimic (mAPE: {cubic_mape})')
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_mab_hybla, y_hybla/mb, label=f'Hybla')
    ax2.plot(x_mab_hybla, y_mab_hybla/mb, label=f'Mimic (mAPE: {hybla_mape})')
    ax2.set_ylabel('Throughput (Mbps)')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_mab_vegas, y_vegas/mb, label=f'Vegas (mAPE: {vegas_mape})')
    ax3.plot(x_mab_vegas, y_mab_vegas/mb, label=f'Mimic (mAPE: {vegas_mape})')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_mab_owl, y_owl/mb, label=f'Owl')
    ax4.plot(x_mab_owl, y_mab_owl/mb, label=f'Mimic (mAPE: {owl_mape})')
    ax4.set_ylabel('Throughput (Mbps)')
    ax4.set_xlabel('Step')
    ax4.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.multi.follow.linear_throughput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_all_multi(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)
    _, rtt_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, cwnd_cubic, _ = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)
    _, z_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, cwnd_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)
    _, z_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, cwnd_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_mab = to_dataframe_prod(config['mab'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)
    _, z_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)
    _, cwnd_mab, _ = get_plot_xyz(df_mab, 'cwnd', config, bws)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)
    _, z_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, cwnd_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)

    fig = plt.figure(figsize=(20, 15))

    offset = 7

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Throughput (Gbps)')
    ax1.plot(x_cubic, rtt_cubic, label='Latency (s)')
    ax1.plot(x_cubic, cwnd_cubic/mb, label='Congestion Window (MB)')
    ax1.set_ylabel('Cubic')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Throughput (Gbps)')
    ax2.plot(x_hybla, z_hybla, label='Latency (s)')
    ax2.plot(x_hybla, cwnd_hybla/mb, label='Congestion Window (MB)')
    ax2.set_ylabel('Hybla')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Throughput (Gbps)')
    ax3.plot(x_vegas, z_vegas, label='Latency (s)')
    ax3.plot(x_vegas, cwnd_vegas/mb, label='Congestion Window (MB)')
    ax3.set_ylabel('Vegas')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Throughput (Gbps)')
    ax4.plot(x_owl, z_owl, label='Latency (s)')
    ax4.plot(x_owl, cwnd_owl/mb, label='Congestion Window (MB)')
    ax4.set_ylabel('Owl')
    ax4.set_xlabel('Step')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Throughput (Gbps)')
    ax5.plot(x_mab[0:y_mab.shape[0]], z_mab/mb, label='Latency (s)')
    ax5.plot(x_mab[0:y_mab.shape[0]], cwnd_mab /
             mb, label='Congestion Window (MB)')
    ax5.set_ylabel('Mimic')
    ax5.set_xlabel('Step')
    ax5.legend()

    file_name = f'{config["trace"]}.multi.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_all(config: dict, arm: str):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)
    _, rtt_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, cwnd_cubic, _ = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)
    _, z_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, cwnd_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)
    _, z_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, cwnd_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_mab = to_dataframe_prod(config['mab'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)
    _, z_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)
    _, cwnd_mab, _ = get_plot_xyz(df_mab, 'cwnd', config, bws)

    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)
    _, z_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, cwnd_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)

    fig = plt.figure(figsize=(5, 8))

    _, ax = plt.subplots()

    offset = 0

    if arm == 'cubic':
        ax.plot(x_cubic, y_cubic, label='Throughput (Gbps)')
        ax.plot(x_cubic, rtt_cubic, label='Latency (s)')
        ax.plot(x_cubic, cwnd_cubic/mb, label='Congestion Window (MB)')
        ax.set_ylabel('Cubic')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'hybla':
        ax.plot(x_hybla, y_hybla, label='Throughput (Gbps)')
        ax.plot(x_hybla, z_hybla, label='Latency (s)')
        ax.plot(x_hybla, cwnd_hybla/mb, label='Congestion Window (MB)')
        ax.set_ylabel('Hybla')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'vegas':
        ax.plot(x_vegas, y_vegas, label='Throughput (Gbps)')
        ax.plot(x_vegas, z_vegas, label='Latency (s)')
        ax.plot(x_vegas, cwnd_vegas/mb, label='Congestion Window (MB)')
        ax.set_ylabel('Vegas')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'owl':
        ax.plot(x_owl, y_owl, label='Throughput (Gbps)')
        ax.plot(x_owl, z_owl, label='Latency (s)')
        ax.plot(x_owl, cwnd_owl/mb, label='Congestion Window (MB)')
        ax.set_ylabel('Owl')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'mimic':
        ax.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Throughput (Gbps)')
        ax.plot(x_mab[0:y_mab.shape[0]], z_mab, label='Latency (s)')
        ax.plot(x_mab[0:y_mab.shape[0]], cwnd_mab /
                mb, label='Congestion Window (MB)')
        ax.set_ylabel('Mimic')
        ax.set_xlabel('Step')
        ax.legend()

    file_name = f'{config["trace"]}.{arm}.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_prod_throughput_latency(cf: dict):
    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    solution_name = 'Mimic'

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    _, x_mimic, _ = get_plot_xyz(df_mimic, 'rtt', config, bws)
    _, y_mimic, _ = get_plot_xyz(df_mimic, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, x_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    offset = 100

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    # y = [49.48, np.mean(y_mimic)*100, 41.3, 39.54, 38.2, 23.064, 16.87, 5.20,
    #      9.97, 22.16, 20.79, 40.89, 2.22, 14.31, 3.33, 4.20, 26.23]
    # x = [6.4, np.mean(x_mimic)*100, 3.33, 3.01, 3.4, 2.3, 2.93, 2.84, 3.71,
    #      3.85, 3.12, 2.54, 2.88, 4.96, 3.29, 3.92, 2.45]
    # n = ['Sprout', f'{solution_name}', 'Cubic', 'Vegas', 'BBR', 'Copa', 'Aurora', 'FillP-Sheep', 'Indigo', 'LEDBAT', 'PCC-Allegro', 'ABC',
    #      'SCReAM', 'TaoVA-100x', 'Verus', 'PCC-Vivace', 'WebRTC']

    y = [np.mean(y_hybla)*offset, np.mean(y_mimic)*offset, np.mean(y_cubic)*offset, np.mean(y_vegas)*offset, np.mean(y_owl)*offset,
         38.2, 23.064, 16.87, 5.20, 9.97, 22.16, 20.79, 40.89, 2.22, 14.31, 3.33, 4.20, 26.23, 49.48]
    x = [np.mean(x_hybla)*kb, np.mean(x_mimic)*kb, np.mean(x_cubic)*kb, np.mean(x_vegas)*kb, np.mean(x_owl)*kb,
         3.4, 2.3, 2.93, 2.84, 3.71, 3.85, 3.12, 2.54, 2.88, 4.96, 3.29, 3.92, 2.45, 6.4]
    n = ['Hybla', 'Mimic', 'Cubic', 'Vegas', 'Owl', 'BBR', 'Copa', 'Aurora', 'FillP-Sheep', 'Indigo', 'LEDBAT', 'PCC-Allegro', 'ABC',
         'SCReAM', 'TaoVA-100x', 'Verus', 'PCC-Vivace', 'WebRTC', 'Sprout']
    # colors = ['red', 'blue', 'yellow', 'green', 'pink', 'grey', 'gold', 'cyan', 'skyblue', 'violet', 'magenta', 'brown', 'olive', 'indigo',
    #           'black', 'silver', 'violet', 'purple']

    N = len(x)
    colors = np.random.rand(N)

    ax.scatter(x, y, c=colors)

    for i in range(N):
        plt.text(x[i], y[i], n[i])

    ax.set_xlabel('Latency (ms)')
    ax.set_ylabel('Throughput (Mbps)')

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # plt.xlabel('Latency (s)')
    # plt.ylabel('Throughput (Gbps)')

    file_name = f'{config["trace"]}.througput_latency.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_prod_throughput_latency_v2(cf: dict):

    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    _, x_mimic, _ = get_plot_xyz(df_mimic, 'rtt', config, bws)
    _, y_mimic, _ = get_plot_xyz(df_mimic, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, x_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    df_basic = to_dataframe_prod(config['basic'], path='log/basic')
    _, x_basic, _ = get_plot_xyz(df_basic, 'rtt', config, bws)
    _, y_basic, _ = get_plot_xyz(df_basic, 'throughput', config, bws)

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [np.mean(y_hybla), np.mean(y_mimic), np.mean(
        y_cubic), np.mean(y_vegas), np.mean(y_owl), np.mean(y_basic)] + y_pn.tolist()
    x = [np.mean(x_hybla), np.mean(x_mimic), np.mean(
        x_cubic), np.mean(x_vegas), np.mean(x_owl), np.mean(x_basic)] + (x_pn/kb).tolist()
    n = ['Hybla', 'Mimic', 'Cubic', 'Vegas', 'Owl', 'Basic'] + z_pn.tolist()

    for index in range(len(x)):
        ax.scatter(x[index], y[index],
                   label=n[index], clip_on=False, s=None)
        ax.annotate(n[index], (x[index], y[index]))

    ax.set_xlabel('Latency (s)')
    ax.set_ylabel('Throughput (Mbps)')

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # plt.xlabel('Latency (s)')
    # plt.ylabel('Throughput (Gbps)')

    ax.legend(n, scatterpoints=1, bbox_to_anchor=(1, 0.5),
              loc='center left', fontsize=12)

    plt.title(f'{config["trace"]} | Mean Throughput vs Mean Latency')

    file_name = f'{config["trace"]}.v2.througput_latency.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_prod_throughput(config: dict, plot_bandwidth: bool = False):

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x, y_cubic, z = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    x_mimic, y_mimic, _ = get_plot_xyz(df_mimic, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_mimic, y_mimic, label='Mimic', c='blue')
    ax.plot(x, y_cubic, label='Cubic', c='black')
    ax.plot(x, y_vegas, label='Vegas', c='green')
    ax.plot(x, y_hybla, label='Hybla', c='violet')
    ax.plot(x, y_owl, label='Owl', c='indigo')

    if len(z) > 0 and plot_bandwidth:
        ax.plot(x, z/mb, label='Bandwidth', c='red')

    plt.xlabel('Step')
    plt.ylabel('Throughput (Mbps)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.throughput.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_prod_throughput_loss(config: dict):

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'lost', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'lost', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'lost', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mab = to_dataframe_prod(config['mimic'])
    _, x_mab, _ = get_plot_xyz(df_mab, 'lost', config, bws)
    _, y_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, x_owl, _ = get_plot_xyz(df_owl, 'lost', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    x = [np.mean(x_cubic), np.mean(x_hybla), np.mean(x_vegas),
         np.mean(x_owl), np.mean(x_mab[0:y_mab.shape[0]])]
    y = [np.mean(y_cubic), np.mean(y_hybla), np.mean(
        y_vegas), np.mean(y_owl), np.mean(y_mab)]
    x_ticks = ['Cubic', 'Hybla', 'Vegas', 'Owl', 'Mimic']

    N = len(x)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

    ax.scatter(x, y, c=colors)

    for i in range(N):
        plt.text(x[i], y[i], x_ticks[i])

    plt.xlabel('Packet Loss')
    plt.ylabel('Throughput (Mbps)')

    file_name = f'{config["trace"]}.throughput_loss.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_prod_throughput_latency_best(cf: dict):

    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    _, x_mimic, _ = get_plot_xyz(df_mimic, 'rtt', config, bws)
    _, y_mimic, _ = get_plot_xyz(df_mimic, 'throughput', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, x_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, y_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    df_basic = to_dataframe_prod(config['basic'], path='log/basic')
    _, x_basic, _ = get_plot_xyz(df_basic, 'rtt', config, bws)
    _, y_basic, _ = get_plot_xyz(df_basic, 'throughput', config, bws)


    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])
    

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [np.max(y_hybla), np.max(y_mimic), np.max(y_cubic),
         np.max(y_vegas), np.max(y_owl), np.max(y_basic)]+ y_pn.tolist()
    x = [np.min(x_hybla)*kb, np.min(x_mimic)*kb, np.min(x_cubic)*kb,
         np.min(x_vegas)*kb, np.min(x_owl)*kb, np.min(x_basic)*kb]+ (x_pn/kb).tolist()
    n = ['Hybla', 'Mimic', 'Cubic', 'Vegas', 'Owl', 'Basic']+ z_pn.tolist()

    for index in range(len(x)):
        ax.scatter(x[index], y[index],
                   label=n[index], clip_on=False, s=None)
        ax.annotate(n[index], (x[index], y[index]))

    ax.set_xlabel('Latency (ms)')
    ax.set_ylabel('Throughput (Mbps)')

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # plt.xlabel('Latency (s)')
    # plt.ylabel('Throughput (Gbps)')

    ax.legend(n, scatterpoints=1, bbox_to_anchor=(1, 0.5),
              loc='center left', fontsize=12)

    plt.title(f'{config["trace"]} | Max Throughput vs Min Latency')

    file_name = f'{config["trace"]}.best.througput_latency.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')
