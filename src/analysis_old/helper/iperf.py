import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *


def plot_iperf_throughput_latency_mean(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x_cubic = df_cubic.end.streams[0].sender.mean_rtt/mb
    y_cubic = df_cubic.end.sum_sent.bits_per_second/mb

    df_hybla = get_iperf_log(config['hybla_iperf'])
    x_hybla = df_hybla.end.streams[0].sender.mean_rtt/mb
    y_hybla = df_hybla.end.sum_sent.bits_per_second/mb

    df_vegas = get_iperf_log(config['vegas_iperf'])
    x_vegas = df_vegas.end.streams[0].sender.mean_rtt/mb
    y_vegas = df_vegas.end.sum_sent.bits_per_second/mb

    df_mimic = get_iperf_log(config['mimic_iperf'])
    x_mimic = df_mimic.end.streams[0].sender.mean_rtt/mb
    y_mimic = df_mimic.end.sum_sent.bits_per_second/mb

    df_owl = get_iperf_log(config['owl_iperf'])
    x_owl = df_owl.end.streams[0].sender.mean_rtt/mb
    y_owl = df_owl.end.sum_sent.bits_per_second/mb

    df_basic = get_iperf_log(config['basic_iperf'])
    x_basic = df_basic.end.streams[0].sender.mean_rtt/mb
    y_basic = df_basic.end.sum_sent.bits_per_second/mb

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [y_hybla, y_mimic, y_cubic, y_vegas, y_owl, y_basic] + y_pn.tolist()
    x = [x_hybla, x_mimic, x_cubic, x_vegas,
         x_owl, x_basic] + (x_pn/kb).tolist()
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

    plt.title(f'{config["trace"]} | Throughput vs Mean Latency')

    file_name = f'{config["trace"]}.iperf.througput_latency_mean.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput_latency_min(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x_cubic = df_cubic.end.streams[0].sender.min_rtt/mb
    y_cubic = df_cubic.end.sum_sent.bits_per_second/mb

    df_hybla = get_iperf_log(config['hybla_iperf'])
    x_hybla = df_hybla.end.streams[0].sender.min_rtt/mb
    y_hybla = df_hybla.end.sum_sent.bits_per_second/mb

    df_vegas = get_iperf_log(config['vegas_iperf'])
    x_vegas = df_vegas.end.streams[0].sender.min_rtt/mb
    y_vegas = df_vegas.end.sum_sent.bits_per_second/mb

    df_mimic = get_iperf_log(config['mimic_iperf'])
    x_mimic = df_mimic.end.streams[0].sender.min_rtt/mb
    y_mimic = df_mimic.end.sum_sent.bits_per_second/mb

    df_owl = get_iperf_log(config['owl_iperf'])
    x_owl = df_owl.end.streams[0].sender.min_rtt/mb
    y_owl = df_owl.end.sum_sent.bits_per_second/mb

    df_basic = get_iperf_log(config['basic_iperf'])
    x_basic = df_basic.end.streams[0].sender.min_rtt/mb
    y_basic = df_basic.end.sum_sent.bits_per_second/mb

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [y_hybla, y_mimic, y_cubic, y_vegas, y_owl, y_basic] + y_pn.tolist()
    x = [x_hybla, x_mimic, x_cubic, x_vegas,
         x_owl, x_basic] + (x_pn/kb).tolist()
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

    plt.title(f'{config["trace"]} | Throughput vs Min Latency')

    file_name = f'{config["trace"]}.iperf.througput_latency_min.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput_latency_max(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x_cubic = df_cubic.end.streams[0].sender.max_rtt/mb
    y_cubic = df_cubic.end.sum_sent.bits_per_second/mb

    df_hybla = get_iperf_log(config['hybla_iperf'])
    x_hybla = df_hybla.end.streams[0].sender.max_rtt/mb
    y_hybla = df_hybla.end.sum_sent.bits_per_second/mb

    df_vegas = get_iperf_log(config['vegas_iperf'])
    x_vegas = df_vegas.end.streams[0].sender.max_rtt/mb
    y_vegas = df_vegas.end.sum_sent.bits_per_second/mb

    df_mimic = get_iperf_log(config['mimic_iperf'])
    x_mimic = df_mimic.end.streams[0].sender.max_rtt/mb
    y_mimic = df_mimic.end.sum_sent.bits_per_second/mb

    df_owl = get_iperf_log(config['owl_iperf'])
    x_owl = df_owl.end.streams[0].sender.max_rtt/mb
    y_owl = df_owl.end.sum_sent.bits_per_second/mb

    df_basic = get_iperf_log(config['basic_iperf'])
    x_basic = df_basic.end.streams[0].sender.max_rtt/mb
    y_basic = df_basic.end.sum_sent.bits_per_second/mb

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [y_hybla, y_mimic, y_cubic, y_vegas, y_owl, y_basic] + y_pn.tolist()
    x = [x_hybla, x_mimic, x_cubic, x_vegas,
         x_owl, x_basic] + (x_pn/kb).tolist()
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

    plt.title(f'{config["trace"]} | Throughput vs Max Latency')

    file_name = f'{config["trace"]}.iperf.througput_latency_max.scatter.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_cwnd_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'cwnd')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'cwnd')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'cwnd')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'cwnd')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'cwnd')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'cwnd')

    fig = plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x, y_cubic/kb, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Congestion Window (KB)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x, y_hybla/kb, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Congestion Window (KB)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x, y_vegas/kb, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Congestion Window (KB)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x, y_owl/kb, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Congestion Window (KB)')
    ax4.set_xlabel('Time (s)')
    ax4.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x, y_mimic/kb, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Congestion Window (KB)')
    ax5.set_xlabel('Time (s)')
    ax5.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax5.legend()

    ax6 = plt.subplot(326)
    ax6.plot(x, y_basic/mb, label='Basic', color='#ff7f0e')
    ax6.set_ylabel('Throughput (Mbps)')
    ax6.set_xlabel('Time (s)')
    ax6.set_title(f'{config["trace"]} | Congestion Window vs Time')
    ax6.legend()

    file_name = f'{config["trace"]}.iperf.cwnd.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_cwnd(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'cwnd')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'cwnd')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'cwnd')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'cwnd')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'cwnd')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'cwnd')

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x, y_cubic/kb, label='Cubic')
    ax.plot(x, y_hybla/kb, label='Hybla')
    ax.plot(x, y_vegas/kb, label='Vegas')
    ax.plot(x, y_owl/kb, label='Owl')
    ax.plot(x, y_mimic/kb, label='Mimic')
    ax.plot(x, y_basic/kb, label='Basic')

    plt.xlabel('Time (s)')
    plt.ylabel('Congestion Window (KB)')
    plt.title(f'{config["trace"]} | Congestion Window vs Time')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_latency_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'rtt')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'rtt')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'rtt')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'rtt')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'rtt')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'rtt')

    fig = plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x, y_cubic/mb, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Latency (s)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title(f'{config["trace"]} | Latency vs Time')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x, y_hybla/mb, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Latency (s)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title(f'{config["trace"]} | Latency vs Time')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x, y_vegas/mb, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Latency (s)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title(f'{config["trace"]} | Latency vs Time')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x, y_owl/mb, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Latency (s)')
    ax4.set_xlabel('Time (s)')
    ax4.set_title(f'{config["trace"]} | Latency vs Time')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x, y_mimic/mb, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Latency (s)')
    ax5.set_xlabel('Time (s)')
    ax5.set_title(f'{config["trace"]} | Latency vs Time')
    ax5.legend()

    ax6 = plt.subplot(326)
    ax6.plot(x, y_basic/mb, label='Basic', color='#ff7f0e')
    ax6.set_ylabel('Throughput (Mbps)')
    ax6.set_xlabel('Time (s)')
    ax6.set_title(f'{config["trace"]} | Latency vs Time')
    ax6.legend()

    file_name = f'{config["trace"]}.iperf.latency.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_latency(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'rtt')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'rtt')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'rtt')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'rtt')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'rtt')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'rtt')

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x, y_cubic/mb, label='Cubic')
    ax.plot(x, y_hybla/mb, label='Hybla')
    ax.plot(x, y_vegas/mb, label='Vegas')
    ax.plot(x, y_owl/mb, label='Owl')
    ax.plot(x, y_mimic/mb, label='Mimic')
    ax.plot(x, y_basic/mb, label='Basic')

    plt.xlabel('Time (s)')
    plt.ylabel('Latency (s)')
    plt.title(f'{config["trace"]} | Latency vs Time')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'throughput')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'throughput')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'throughput')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'throughput')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'throughput')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'throughput')

    fig = plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x, y_cubic/mb, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x, y_hybla/mb, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Throughput (Mbps)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x, y_vegas/mb, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x, y_owl/mb, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Throughput (Mbps)')
    ax4.set_xlabel('Time (s)')
    ax4.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x, y_mimic/mb, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Throughput (Mbps)')
    ax5.set_xlabel('Time (s)')
    ax5.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax5.legend()

    ax6 = plt.subplot(326)
    ax6.plot(x, y_basic/mb, label='Basic', color='#ff7f0e')
    ax6.set_ylabel('Throughput (Mbps)')
    ax6.set_xlabel('Time (s)')
    ax6.set_title(f'{config["trace"]} | Instant Throughput vs Time')
    ax6.legend()

    file_name = f'{config["trace"]}.iperf.throughput.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    x, y_cubic = get_iperf_xyz(df_cubic, 'throughput')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'throughput')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'throughput')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'throughput')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'throughput')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'throughput')

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x, y_cubic/mb, label='Cubic')
    ax.plot(x, y_hybla/mb, label='Hybla')
    ax.plot(x, y_vegas/mb, label='Vegas')
    ax.plot(x, y_owl/mb, label='Owl')
    ax.plot(x, y_mimic/mb, label='Mimic')
    ax.plot(x, y_basic/mb, label='Basic')

    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (Mbps)')
    plt.title(f'{config["trace"]} | Instant Throughput vs Time')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.throughput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput_rtt_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'throughput')
    _, x_cubic = get_iperf_xyz(df_cubic, 'rtt')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'throughput')
    _, x_hybla = get_iperf_xyz(df_hybla, 'rtt')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'throughput')
    _, x_vegas = get_iperf_xyz(df_vegas, 'rtt')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'throughput')
    _, x_mimic = get_iperf_xyz(df_mimic, 'rtt')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'throughput')
    _, x_owl = get_iperf_xyz(df_owl, 'rtt')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'throughput')
    _, x_basic = get_iperf_xyz(df_basic, 'rtt')

    fig = plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic/mb, y_cubic/mb, label='Cubic', color='#ff7f0e')
    ax1.set_ylabel('Throughput (Mbps)')
    ax1.set_xlabel('Latency (s)')
    ax1.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla/mb, y_hybla/mb, label='Hybla', color='#ff7f0e')
    ax2.set_ylabel('Throughput (Mbps)')
    ax2.set_xlabel('Latency (s)')
    ax2.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas/mb, y_vegas/mb, label='Vegas', color='#ff7f0e')
    ax3.set_ylabel('Throughput (Mbps)')
    ax3.set_xlabel('Latency (s)')
    ax3.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl/mb, y_owl/mb, label='Owl', color='#ff7f0e')
    ax4.set_ylabel('Throughput (Mbps)')
    ax4.set_xlabel('Latency (s)')
    ax4.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mimic/mb, y_mimic/mb, label='Mimic', color='#ff7f0e')
    ax5.set_ylabel('Throughput (Mbps)')
    ax5.set_xlabel('Latency (s)')
    ax5.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax5.legend()

    ax6 = plt.subplot(326)
    ax6.plot(x_basic/mb, y_basic/mb, label='Basic', color='#ff7f0e')
    ax6.set_ylabel('Throughput (Mbps)')
    ax6.set_xlabel('Latency (s)')
    ax6.set_title(f'{config["trace"]} | Instant Throughput vs Latency')
    ax6.legend()

    file_name = f'{config["trace"]}.iperf.throughput_rtt.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')


def plot_iperf_throughput_rtt(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'throughput')
    _, x_cubic = get_iperf_xyz(df_cubic, 'rtt')

    df_hybla = get_iperf_log(config['hybla_iperf'])
    _, y_hybla = get_iperf_xyz(df_hybla, 'throughput')
    _, x_hybla = get_iperf_xyz(df_hybla, 'rtt')

    df_vegas = get_iperf_log(config['vegas_iperf'])
    _, y_vegas = get_iperf_xyz(df_vegas, 'throughput')
    _, x_vegas = get_iperf_xyz(df_vegas, 'rtt')

    df_mimic = get_iperf_log(config['mimic_iperf'])
    _, y_mimic = get_iperf_xyz(df_mimic, 'throughput')
    _, x_mimic = get_iperf_xyz(df_mimic, 'rtt')

    df_owl = get_iperf_log(config['owl_iperf'])
    _, y_owl = get_iperf_xyz(df_owl, 'throughput')
    _, x_owl = get_iperf_xyz(df_owl, 'rtt')

    df_basic = get_iperf_log(config['basic_iperf'])
    _, y_basic = get_iperf_xyz(df_basic, 'throughput')
    _, x_basic = get_iperf_xyz(df_basic, 'rtt')

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic/mb, y_cubic/mb, label='Cubic')
    ax.plot(x_hybla/mb, y_hybla/mb, label='Hybla')
    ax.plot(x_vegas/mb, y_vegas/mb, label='Vegas')
    ax.plot(x_owl/mb, y_owl/mb, label='Owl')
    ax.plot(x_mimic/mb, y_mimic/mb, label='Mimic')
    ax.plot(x_basic/mb, y_basic/mb, label='Basic')

    plt.xlabel('Latency (s)')
    plt.ylabel('Throughput (Mbps)')
    plt.title(f'{config["trace"]}| Instant Throughput vs Latency')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.throughput_rtt.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')
