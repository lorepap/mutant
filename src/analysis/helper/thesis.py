import math
import random
from copy import deepcopy
from datetime import datetime

import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pandas as pd
from astropy.visualization import hist
from pyparsing import line

from helper.utils import *

matplotlib.rc('font', family='serif', serif='cm10')
plt.rc('text', usetex=True)
plt.rcParams['font.size'] = '16'
# plt.rcParams['font.weight'] = 'bold'
# matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']


def ts_throughput_orca(config: dict) -> None:

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []
    z = np.array(bws)[0:config['max']]

    keys = [*config]

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ignore = ['pantheon']
    colors = ['blue', 'red', 'green', 'brown', 'purple', 'violet', 'black']
    ls_list = ['-', '-.', ':', '--', '--', '-.', ':']
    index = 0

    for key in keys:

        path = config[key]

        key = key.replace('_iperf', '')

        if key in ignore:
            continue

        if not isinstance(path, str):
            continue

        if not path.endswith('.json'):
            continue

        x, ykey = from_iperf(path, 'throughput')

        title = key if key != 'mimic' else 'mimic'

        ax.plot(x[0:10], (ykey/mb)[0:10], label=title.replace('_',
                '\_'), ls=ls_list[index], color=colors[index])
        index += 1

    # ax.plot(np.arange(z.shape[0]), z/mb, label='bandwidth', c='red')

    ax.set_xlabel('Time (s)', fontsize=16)
    ax.set_ylabel('Throughput (Mbit/s)', fontsize=16)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.througput.orca.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_throughput_latency_orca(config: dict) -> None:

    keys = config.keys()
    x = []
    y = []
    n = []

    # ignore = ['cubic', 'pantheon', 'basic', 'hybla', 'vegas', 'owl']
    ignore = ['cubic', 'pantheon']

    for key in keys:

        path = config[key]

        key = key.replace('_iperf', '')

        if key in ignore:
            continue

        if not isinstance(path, str):
            continue

        if not path.endswith('.json'):
            continue

        _, ykey = from_iperf(path, 'throughput')
        _, xkey = from_iperf(path, 'rtt')

        title = key if key != 'mimic' else 'mimic'

        y.append(np.mean(ykey)/mb)
        x.append(np.mean(xkey)/nb)
        n.append(title.replace('_', '\_'))

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'], ['quic'])

    _, ax = plt.subplots()

    y += y_pn.tolist()
    x += (x_pn/kb).tolist()
    n += z_pn.tolist()

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o', 'x']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple', '#A52A2A']

    for index in range(len(x)):
        ax.scatter(x[index], y[index], color=colors[index], marker=markers[index],
                   label=bold(n[index]), clip_on=False, s=300)

    ax.set_xlabel(bold('Latency (s)'), fontsize=16)
    ax.set_ylabel(bold('Throughput (Mbps)'), fontsize=16)

    # confidence_ellipse(np.array(x), np.array(y), ax, facecolor='#F5F5DC',
    #                    edgecolor='brown', linestyle='--', zorder=0, n_std=1)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.througput_latency.orca.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')


def ts_throughput_latency_mean(config: dict) -> None:

    if 'dir_path' not in config:
        config['dir_path'] = 'log/iperf/protocol'

    x_cubic, y_cubic = iperf_dir_lastfile_tput_latency_mean(
        'cubic', config['trace'], config['dir_path'])

    x_hybla, y_hybla = iperf_dir_lastfile_tput_latency_mean(
        'hybla', config['trace'], config['dir_path'])

    x_vegas, y_vegas = iperf_dir_lastfile_tput_latency_mean(
        'vegas', config['trace'], config['dir_path'])

    x_mimic, y_mimic = iperf_dir_lastfile_tput_latency_mean(
        'mimic', config['trace'], config['dir_path'])

    x_owl, y_owl = iperf_dir_lastfile_tput_latency_mean(
        'owl', config['trace'], config['dir_path'])

    x_basic, y_basic = iperf_dir_lastfile_tput_latency_mean(
        'bs', config['trace'], config['dir_path'])

    if 'pantheon' in config:
        x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'], ['quic'])
    else:
        x_pn, y_pn, z_pn = (np.array([]), np.array([]), np.array([]))

    # plt.figure(figsize=(20, 15))

    plt.ioff()
    _, ax = plt.subplots()

    y = [
        y_hybla/mb,
        y_mimic/mb,
        y_vegas/mb,
        y_owl/mb,
        y_basic/mb,
        # y_cubic/mb
    ] + y_pn.tolist()
    x = [
        x_hybla/nb,
        x_mimic/nb,
        x_vegas/nb,
        x_owl/nb,
        x_basic/nb,
        # x_cubic/nb
    ] + (x_pn/kb).tolist()
    n = bold_ls(['hybla', 'mimic', 'vegas', 'owl',
                'basic'] + z_pn.tolist())

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    for index in range(len(x)):
        ax.scatter(x[index], y[index], color=colors[index], marker=markers[index],
                   label=n[index], clip_on=False, s=300)

    ax.set_xlabel(bold('Latency (s)'), fontsize=16)
    ax.set_ylabel(bold('Throughput (Mbps)'), fontsize=16)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.througput_latency.mean.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_throughput_latency_all(config: dict) -> None:

    if 'dir_path' not in config:
        config['dir_path'] = 'log/iperf/protocol'

    _, y_cubic = get_iperf_xyz_all_mean(
        'cubic', config['trace'], 'throughput', config['dir_path'])
    _, x_cubic = get_iperf_xyz_all_mean(
        'cubic', config['trace'], 'rtt', config['dir_path'])

    _, y_hybla = get_iperf_xyz_all_mean(
        'hybla', config['trace'], 'throughput', config['dir_path'])
    _, x_hybla = get_iperf_xyz_all_mean(
        'hybla', config['trace'], 'rtt', config['dir_path'])

    _, y_vegas = get_iperf_xyz_all_mean(
        'vegas', config['trace'], 'throughput', config['dir_path'])
    _, x_vegas = get_iperf_xyz_all_mean(
        'vegas', config['trace'], 'rtt', config['dir_path'])

    _, y_mimic = get_iperf_xyz_all_mean(
        'mimic', config['trace'], 'throughput', config['dir_path'])
    _, x_mimic = get_iperf_xyz_all_mean(
        'mimic', config['trace'], 'rtt', config['dir_path'])

    _, y_owl = get_iperf_xyz_all_mean(
        'owl', config['trace'], 'throughput', config['dir_path'])
    _, x_owl = get_iperf_xyz_all_mean(
        'owl', config['trace'], 'rtt', config['dir_path'])

    _, y_basic = get_iperf_xyz_all_mean(
        'bs', config['trace'], 'throughput', config['dir_path'])
    _, x_basic = get_iperf_xyz_all_mean(
        'bs', config['trace'], 'rtt', config['dir_path'])

    config_ls = config['dir_path'].split('/')
    tag = 'ps' if len(config_ls) != 4 else config_ls[3]

    if 'pantheon' in config:
        delay_pn, tp_pn, z_pn = get_pantheon_all_xyz(config['pantheon'])

        x_pn = []
        y_pn = []

        for p in z_pn:
            xall = delay_pn[p].tolist()
            yall = tp_pn[p].tolist()
            x_pn.append(np.mean(xall)/kb)
            y_pn.append(np.mean(yall))

        x_pn = np.array(x_pn)
        y_pn = np.array(y_pn)
    else:
        x_pn, y_pn, z_pn = (np.array([]), np.array([]), np.array([]))

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [
        np.mean(y_hybla)/mb,
        np.mean(y_mimic)/mb,
        np.mean(y_vegas)/mb,
        np.mean(y_owl)/mb,
        np.mean(y_basic)/mb,
        np.mean(y_cubic)/mb
    ] + y_pn.tolist()
    x = [
        np.mean(x_hybla)/mb,
        np.mean(x_mimic)/mb,
        np.mean(x_vegas)/mb,
        np.mean(x_owl)/mb,
        np.mean(x_basic)/mb,
        np.mean(x_cubic)/mb
    ] + x_pn.tolist()
    n = ['hybla', 'mimic', 'vegas', 'owl', 'basic', 'cubic'] + z_pn.tolist()
    # n = ['mimic', 'basic'] + z_pn.tolist()

    y_error = [
        CI_model(y_hybla)/mb,
        CI_model(y_mimic)/mb,
        CI_model(y_vegas)/mb,
        CI_model(y_owl)/mb,
        CI_model(y_basic)/mb,
        CI_model(y_cubic)/mb
    ]

    x_error = [
        CI_model(x_hybla)/mb,
        CI_model(x_mimic)/mb,
        CI_model(x_vegas)/mb,
        CI_model(x_owl)/mb,
        CI_model(x_basic)/mb,
        CI_model(x_cubic)/mb
    ]

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    for index in range(len(x)):
        ax.scatter(x[index], y[index], color=colors[index], marker=markers[index], label=bold(n[index]), clip_on=False, s=300)
        # ax.errorbar(x[index], y[index], color=colors[index],
                #    marker='o', label=bold(n[index]), yerr=y_error[index], xerr=x_error[index], markersize=10)
        # ax.annotate(n[index], (x[index], y[index]))

    ax.set_xlabel(bold('Latency  (ms)'), fontsize=16)
    ax.set_ylabel(bold('Throughput (Mbps)'), fontsize=16)

    # ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['right'].set_visible(False)

    # plt.xlabel('Latency (s)')
    # plt.ylabel('Throughput (Gbps)')

    # ax.legend(n, scatterpoints=1, bbox_to_anchor=(1, 0.5),
    #           loc='center left', fontsize=12)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 16})
    # ax.legend(n, loc='lower right', ncol=2)

    file_name = f'ts.{tag}.iperf.througput_latency.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_throughput_latency_last(config: dict) -> None:

    _, y_cubic = get_iperf_xyz_last('cubic', config['trace'], 'throughput')
    _, x_cubic = get_iperf_xyz_last('cubic', config['trace'], 'rtt')

    _, y_hybla = get_iperf_xyz_last('hybla', config['trace'], 'throughput')
    _, x_hybla = get_iperf_xyz_last('hybla', config['trace'], 'rtt')

    _, y_vegas = get_iperf_xyz_last('vegas', config['trace'], 'throughput')
    _, x_vegas = get_iperf_xyz_last('vegas', config['trace'], 'rtt')

    _, y_mimic = get_iperf_xyz_last('mimic', config['trace'], 'throughput')
    _, x_mimic = get_iperf_xyz_last('mimic', config['trace'], 'rtt')

    _, y_owl = get_iperf_xyz_last('owl', config['trace'], 'throughput')
    _, x_owl = get_iperf_xyz_last('owl', config['trace'], 'rtt')

    _, y_basic = get_iperf_xyz_last('bs', config['trace'], 'throughput')
    _, x_basic = get_iperf_xyz_last('bs', config['trace'], 'rtt')

    x_pn, y_pn, z_pn = get_pantheon_xyz(config['pantheon'])

    # plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = [
        round(np.mean(y_hybla)/mb, 4),
        round(np.mean(y_mimic)/mb, 4),
        round(np.mean(y_vegas)/mb, 4),
        round(np.mean(y_owl)/mb, 4),
        round(np.mean(y_basic)/mb, 4),
        # round(np.mean(y_cubic)/mb, 4)
    ] + y_pn.tolist()
    x = [
        round(np.mean(x_hybla)/nb, 4),
        round(np.mean(x_mimic)/nb, 4),
        round(np.mean(x_vegas)/nb, 4),
        round(np.mean(x_owl)/nb, 4),
        round(np.mean(x_basic)/nb, 4),
        # round(np.mean(x_cubic)/nb, 4)
    ] + (x_pn/kb).tolist()
    n = ['hybla', 'mimic', 'vegas', 'owl', 'basic'] + z_pn.tolist()
    # n = ['mimic', 'basic'] + z_pn.tolist()

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    for index in range(len(x)):
        ax.scatter(x[index], y[index], color=colors[index], marker=markers[index],
                   label=bold(n[index]), clip_on=False, s=300)

    ax.set_xlabel(bold('Latency (s)'), fontsize=16)
    ax.set_ylabel(bold('Throughput (Mbps)'), fontsize=16)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=4, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.througput_latency.last.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')


def ts_throughput(config: dict) -> None:

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []
    z = np.array(bws)[0:config['max']]

    x_cubic, y_cubic = get_iperf_xyz_last(
        'cubic', config['trace'], 'throughput', True)

    x_hybla, y_hybla = get_iperf_xyz_last(
        'hybla', config['trace'], 'throughput', True)

    x_vegas, y_vegas = get_iperf_xyz_last(
        'vegas', config['trace'], 'throughput', True)

    x_mimic, y_mimic = get_iperf_xyz_last(
        'mimic', config['trace'], 'throughput', True)

    x_owl, y_owl = get_iperf_xyz_last(
        'owl', config['trace'], 'throughput', True)

    x_basic, y_basic = get_iperf_xyz_last(
        'bs', config['trace'], 'throughput', True)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic/mb, label='cubic', ls='--', color='black')
    ax.plot(x_hybla, y_hybla/mb, label='hybla', ls='--', color='violet')
    ax.plot(x_vegas, y_vegas/mb, label='vegas', ls='--', color='green')
    ax.plot(x_owl, y_owl/mb, label='owl', ls='--', color='brown')
    ax.plot(x_mimic, y_mimic/mb, label='mimic', ls='--', color='blue')
    ax.plot(x_basic, y_basic/mb, label='basic', ls='--', color='purple')
    ax.plot(x_cubic, z/mb, label='bandwidth', c='red')

    ax.set_xlabel('Time (s)', fontsize=16)
    ax.set_ylabel('Throughput (Mbit/s)', fontsize=16)

    # ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['right'].set_visible(False)

    # plt.legend()

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    # plt.title(f'{config["trace"]} | Throughput vs Mean Latency')

    file_name = f'ts.{config["trace"]}.iperf.througput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_cdf_latency_all(config: dict) -> None:

    _, y_cubic = get_iperf_xyz_all('cubic', config['trace'], 'rtt', False)

    _, y_hybla = get_iperf_xyz_all('hybla', config['trace'], 'rtt', False)

    _, y_vegas = get_iperf_xyz_all('vegas', config['trace'], 'rtt', False)

    _, y_mimic = get_iperf_xyz_all('mimic', config['trace'], 'rtt', False)

    _, y_owl = get_iperf_xyz_all('owl', config['trace'], 'rtt', False)

    _, y_basic = get_iperf_xyz_all('bs', config['trace'], 'rtt', False)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    hist(y_cubic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='vegas', color='turquoise')
    hist(y_basic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='mimic', color='green')

    plt.ylabel('CDF')
    plt.xlabel('Latency (ms)')
    # plt.title(f'{config["trace"]} | Latency CDF')
    # plt.legend(loc='upper left')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.cdf.latency.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_cdf_throughput_all(config: dict) -> None:

    _, y_cubic = get_iperf_xyz_all(
        'cubic', config['trace'], 'throughput', False)

    _, y_hybla = get_iperf_xyz_all(
        'hybla', config['trace'], 'throughput', False)

    _, y_vegas = get_iperf_xyz_all(
        'vegas', config['trace'], 'throughput', False)

    _, y_mimic = get_iperf_xyz_all(
        'mimic', config['trace'], 'throughput', False)

    _, y_owl = get_iperf_xyz_all('owl', config['trace'], 'throughput', False)

    _, y_basic = get_iperf_xyz_all('bs', config['trace'], 'throughput', False)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    hist(y_cubic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='vegas', color='turquoise')
    hist(y_basic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step',
         cumulative=True, label='mimic', color='green')

    plt.ylabel('CDF')
    plt.xlabel('Throughput (Mbps)')
    # plt.title(f'{config["trace"]} | Throughput CDF')
    # plt.legend(loc='upper left')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.cdf.throughput.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_throughput_latency_policies(config: dict) -> None:

    keys = config.keys()
    x = []
    xerror = []
    y = []
    yerror = []
    n = []

    for key in keys:

        path = config[key]

        if not isinstance(path, str):
            continue

        if not path.endswith('.json'):
            continue

        _, ykey = from_iperf(path, 'throughput')
        _, xkey = from_iperf(path, 'rtt')

        y.append(np.mean(ykey)/mb)
        yerror.append(CI_model(ykey)/mb)
        xerror.append(CI_model(xkey)/mb)
        x.append(np.mean(xkey)/mb)

        n.append(key.replace('_', '\_'))

    # plt.figure(figsize=(30, 15))

    _, ax = plt.subplots()

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    for index in range(len(x)):
        ax.scatter(x[index], y[index], color=colors[index], marker=markers[index], label=bold(n[index]), clip_on=False, s=300)
        # ax.errorbar(x[index], y[index], color=colors[index],
                #    marker='o', label=bold(n[index]), yerr=yerror[index], xerr=xerror[index], markersize=10)

    ax.set_xlabel(bold('Latency (ms)'), fontsize=16)
    ax.set_ylabel(bold('Throughput (Mbps)'), fontsize=16)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=2, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.policies.througput_latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_protocol_selected(config: dict, wt: str = '') -> None:

    df = to_dataframe_prod(config['mimic'])
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    xtput, ytput = from_iperf(config['mimic_iperf'], 'throughput')
    _, _, bw_list = get_plot_xyz(df, 'throughput', config, bws)
    xrtt, yrtt = from_iperf(config['mimic_iperf'], 'rtt')
    xcwnd, ycwnd = from_iperf(config['mimic_iperf'], 'cwnd')

    y = df['action'][0:config['max']]
    x = np.arange(1, y.shape[0] + 1)

    _, ax1 = plt.subplots(sharex=True)
    ax = None

    axcolor = 'red'
    ax1color = '#1f77b4'

    if wt == 'throughput':
        ax1.plot(xtput, ytput/mb, color=ax1color)
        ax1.fill_between(xtput, 0, ytput/mb, color=ax1color)
        ax1.set_ylabel('Throughput (Mbps)', color=ax1color)
        ax1.set_xlabel('Time (s)')
        ax1.tick_params(axis='y', labelcolor=ax1color)
        ax = ax1.twinx()
        ax.tick_params(axis='y', labelcolor=axcolor)
        ax.set_ylabel('Protocol Selected', color=axcolor)

    elif wt == 'rtt':
        ax1.plot(xrtt, yrtt/nb, color=ax1color)
        ax1.fill_between(xrtt, 0, yrtt/nb, color=ax1color)
        ax1.set_ylabel('Latency (s)', color=ax1color)
        ax1.set_xlabel('Time (s)')
        ax1.tick_params(axis='y', labelcolor=ax1color)
        ax = ax1.twinx()
        ax.tick_params(axis='y', labelcolor=axcolor)
        ax.set_ylabel('Protocol Selected', color=axcolor)

    elif wt == 'cwnd':
        ax1.plot(xcwnd, ycwnd/mb, color=ax1color)
        ax1.fill_between(xcwnd, 0, ycwnd/mb, color=ax1color)
        ax1.set_ylabel('Cwnd (MB)')
        ax1.set_xlabel('Time (s)')
        ax1.tick_params(axis='y', labelcolor=ax1color)
        ax = ax1.twinx()
        ax.tick_params(axis='y', labelcolor=axcolor)
        ax.set_ylabel('Protocol Selected', color=axcolor)

    elif wt == 'bw':
        ax1.plot(x, bw_list/mb, color=ax1color)
        ax1.fill_between(x, 0, bw_list/mb, color=ax1color)
        ax1.set_ylabel('Bandwidth (Mbps)', color=ax1color)
        ax1.set_xlabel('Time (s)')
        ax1.tick_params(axis='y', labelcolor=ax1color)
        ax = ax1.twinx()
        ax.tick_params(axis='y', labelcolor=axcolor)
        ax.set_ylabel('Protocol Selected', color=axcolor)

    else:
        ax = ax1
        ax.set_ylabel('Protocol Selected')

    ax.plot(x, y, label='Protocol', c='black',
            markerfacecolor=axcolor, marker='o', linestyle='-.')

    ax.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
    ax.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])
    ax.set_xlabel('Time (s)')

    file_name = f'ts.{config["trace"]}.protocol.linear.{wt}.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def ts_model_selected(config: dict) -> None:

    df = to_dataframe_prod(config['mimic'])
    y = df['model'][0:config['max']].tolist()
    x = np.arange(1, len(y) + 1)

    y = list(map(lambda x: x.replace('_', '\_'), y))

    _, ax = plt.subplots()

    ax.plot(x, y, label='Model', c='black',
            markerfacecolor='red', marker='o', linestyle='-.')

    plt.xlabel('Time (s)')
    plt.ylabel('ML Model Selected')
    plt.title('')

    file_name = f'ts.{config["trace"]}.model.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def ts_protocol_selected_throughput(config: dict) -> None:

    df = to_dataframe_prod(config['mimic'])

    protocols = np.unique(df['protocol'])

    x = {}
    y = {}

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    for ps in protocols:
        y = df[df['protocol'] == ps]['throughput'].values[0:config['max']]
        N = y.shape[0]
        x = np.arange(N)

        ax.plot(x, y, label=ps, ls='-', marker='o')

    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Throughput (Mbit/s)', fontsize=11)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.througput.protocol.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_protocol_selected_cwnd(config: dict) -> None:

    df = to_dataframe_prod(config['mimic'])

    protocols = np.unique(df['protocol'])

    x = {}
    y = {}

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    for ps in protocols:
        y = df[df['protocol'] == ps]['cwnd'].values[0:config['max']]
        N = y.shape[0]
        x = np.arange(N)

        ax.plot(x, y/kb, label=ps, ls='-', marker='o')

    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Congestion Window (KB)', fontsize=11)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.cwnd.protocol.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_protocol_selected_metric(cf: dict) -> None:

    config = deepcopy(cf)
    config['max'] = 5
    st = 0
    end = 10

    df = to_dataframe_prod(config['mimic'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    y = df['action'][st:end].values
    cwnd = df['cwnd'][st:end].values/kb
    tput = df['throughput'][st:end].values
    dd = df['delivered'][st:end].values
    x = np.arange(1, y.shape[0] + 1)

    ax.plot(x, y, label='Protocol', c='black',
            markerfacecolor='red', marker='o', linestyle='-.')

    for i in range(cwnd.shape[0]):
        # label = f'({round(cwnd[i], 3)}, {round(tput[i], 3)})'
        # label = f'({round(tput[i], 3)})'
        label = f'({math.floor(dd[i])})'
        # label = f'({round(cwnd[i], 3)})'
        ax.annotate(label, (x[i]-0.1, y[i]-0.1), fontsize=5)

    ax.set_xlabel('Time (s)', fontsize=11)
    ax.set_ylabel('Protocol Selected', fontsize=11)
    ax.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
    ax.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
    #            fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.metric.protocol.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_protocol_selected_metric_multi(cf: dict) -> None:

    config = deepcopy(cf)
    config['max'] = 5
    st = 0
    end = 60

    df = to_dataframe_prod(config['mimic'])

    fig, ax = plt.subplots()

    # plt.figure(figsize=(30, 10))

    y = df['action'][st:end].values
    cwnd = df['cwnd'][st:end].values/kb
    tput = df['throughput'][st:end].values
    dd = df['delivered'][st:end].values
    md = df['model'][st:end].values
    md_abbrv = abbreviate_ls(md)
    x = np.arange(1, y.shape[0] + 1)

    n = []
    for i in range(len(md)):
        n.append(f"{to_latex_txt(md[i])} ({md_abbrv[i]})")

    # print(np.unique(n))

    # return

    markers = ['+', 'x', 'o', '*', '^', '+', '<',
               '>', 'H', 'p', '1', 'd', 'D', '^', '+', 'o']
    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    md_color = {}
    md_marker = {}
    for index, i in enumerate(np.unique(md_abbrv)):
        md_color[i] = colors[index]
        md_marker[i] = markers[index]

    ax = None

    div = 10

    for index in range(6):
        yindex = y[index*div:(index*div + div)]
        cwndindex = cwnd[index*div:(index*div + div)]
        tputindex = tput[index*div:(index*div + div)]
        ddindex = dd[index*div:(index*div + div)]
        md_abbrvindex = md_abbrv[index*div:(index*div + div)]
        md_index = md[index*div:(index*div + div)]
        xindex = x[index*div:(index*div + div)]

        ax = plt.subplot(320 + index + 1)

        for i in range(xindex.shape[0]):
            ll = f"{to_latex_txt(md_index[i])} ({md_abbrvindex[i]})"
            ax.scatter(xindex[i], yindex[i], label=ll, c=md_color[md_abbrvindex[i]],
                       marker=md_marker[md_abbrvindex[i]], linestyle='-.', s=200)

        ax.set_xlabel('Time (s)', fontsize=11)
        ax.set_ylabel('Protocol Selected', fontsize=11)
        ax.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
        ax.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])

        for i in range(cwndindex.shape[0]):
            # label = f'({round(cwnd[i], 3)}, {round(tput[i], 3)})'
            # label = f'({round(tputindex[i], 3)})'
            label = f'({md_abbrvindex[i]})'
            # label = f'({math.floor(ddindex[i])})'
            # label = f'({round(cwnd[i], 3)})'
            # ax.annotate(label, (xindex[i]-0.1, yindex[i]-0.1), fontsize=16)

    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 + box.height *
    #                 0.1, box.width, box.height * 1.25])

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=2, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.iperf.metric.protocol.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=600, bbox_inches='tight')
    plt.close('all')


def ts_protocol_total_picks(config: dict):

    df = to_dataframe_prod(config['mimic'])[0:config['max']]

    x0 = df[df['action'] == 0].shape[0]
    x1 = df[df['action'] == 1].shape[0]
    x2 = df[df['action'] == 2].shape[0]
    x3 = df[df['action'] == 3].shape[0]
    offset = np.min([x0, x1, x2, x3]) - 5

    x = ['cubic', 'hybla', 'owl', 'vegas']
    y = np.array([x0, x1, x2, x3]) - offset

    df = pd.DataFrame({'x': x, 'y': y})
    df = df.sort_values('y', ascending=True).reset_index()

    _, ax = plt.subplots()

    ax.barh(df['x'], df['y'])
    plt.ylabel('Protocol Selected')
    plt.xlabel('Total times chosen')

    y = df['y']

    ax.set_xticks([])
    ax.set_xticklabels([])

    for i in range(len(y)):
        # ax.text(i - .15, v + 10, str(v), color='blue', fontweight='bold')
        # plt.annotate(y[i], (-0.1 + i, y[i] + 10))
        plt.annotate(y[i] + offset, (y[i] + 0.25, i-0.1))

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)

    plot_file_name = f'ts.{config["trace"]}.protocol.chosen.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def ts_model_total_picks(config: dict):

    df = to_dataframe_prod(config['mimic'])[0:config['max']]
    x = []
    y = []
    models = np.unique(df['model'])

    for m in models:
        m_count = df[df['model'] == m].shape[0]
        x.append(to_latex_txt(m))
        y.append(m_count)

    offset = np.min(y) - 5

    y = np.array(y) - offset

    df = pd.DataFrame({'x': x, 'y': y})
    df = df.sort_values('y', ascending=True).reset_index()

    _, ax = plt.subplots()

    ax.barh(df['x'], df['y'])
    plt.ylabel('ML Model Selected')
    plt.xlabel('Total times chosen')

    y = df['y']

    ax.set_xticks([])
    ax.set_xticklabels([])

    for i in range(len(y)):
        # ax.text(i - .15, v + 10, str(v), color='blue', fontweight='bold')
        # plt.annotate(y[i], (-0.1 + i, y[i] + 10))
        plt.annotate(y[i] + offset, (y[i] + 0.25, i-0.1))

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)

    plot_file_name = f'ts.{config["trace"]}.model.chosen.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def ts_reward(config: dict) -> None:

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'reward', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'reward', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'reward', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    x_mimic, y_mimic, _ = get_plot_xyz(df_mimic, 'reward', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'reward', config, bws)

    df_basic = to_dataframe_prod(config['basic'])
    x_basic, y_basic, _ = get_plot_xyz(df_basic, 'reward', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_mimic, y_mimic, label='mimic', c='blue', ls='--')
    ax.plot(x_cubic, y_cubic, label='cubic', c='black', ls='-.')
    ax.plot(x_vegas, y_vegas, label='vegas', c='green', ls='-')
    ax.plot(x_hybla, y_hybla, label='hybla', c='violet', ls=':')
    ax.plot(x_owl, y_owl, label='owl', c='red', ls='-')
    ax.plot(x_basic, y_basic, label='basic', c='purple', ls='--')

    plt.xlabel('Step')
    plt.ylabel('Reward')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.reward.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def ts_reward_error(config: dict) -> None:

    h_cubic, x_cubic, y_cubic = prepare_error_ds_prod(config['cubic'])

    h_hybla, x_hybla, y_hybla = prepare_error_ds_prod(config['hybla'])

    h_vegas, x_vegas, y_vegas = prepare_error_ds_prod(config['vegas'])

    h_mimic, x_mimic, y_mimic = prepare_error_ds_prod(config['mimic'])

    h_owl, x_owl, y_owl = prepare_error_ds_prod(config['owl'])

    h_basic, x_basic, y_basic = prepare_error_ds_prod(config['basic'])

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.errorbar(x_mimic, y_mimic, yerr=h_mimic,
                label='mimic', c='blue', ls='-')
    ax.errorbar(x_cubic, y_cubic, yerr=h_cubic,
                label='cubic', c='black', ls='-.')
    ax.errorbar(x_vegas, y_vegas, yerr=h_vegas,
                label='vegas', c='green', ls='--')
    ax.errorbar(x_hybla, y_hybla, yerr=h_hybla,
                label='hybla', c='violet', ls='-')
    ax.errorbar(x_owl, y_owl, yerr=h_owl, label='owl', c='red', ls='--')
    ax.errorbar(x_basic, y_basic, yerr=h_basic,
                label='basic', c='purple', ls=':')

    plt.xlabel('Rounds')
    plt.ylabel('Cummulative Mean Reward')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.reward.errorbar.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def ts_reward_error_policies(config: dict) -> None:

    keys = config.keys()
    x = []
    y = []
    n = []

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    colors = ['red', 'blue', 'green', 'turquoise', 'black', 'violet', 'gold',
              'cyan', 'skyblue', 'pink', 'brown', 'olive', 'gray', 'violet', 'indigo', 'purple']

    index = 0

    for key in keys:

        path = config[key]

        if not isinstance(path, str):
            continue

        if not path.endswith('.csv'):
            continue

        h, x, y = prepare_error_ds_prod(path)

        ax.errorbar(x, y, yerr=h, label=to_latex_txt(key), c=colors[index])

        index += 1

    plt.xlabel('Rounds')
    plt.ylabel('Cummulative Mean Reward')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=2, prop={'size': 16})

    file_name = f'ts.{config["trace"]}.reward.policies.errorbar.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def ts_harm_throughput(att_config: dict, tm_config: dict, vz_config: dict) -> None:

    _, att_tput_solo = from_iperf(att_config['solo'], 'throughput')
    _, att_tput_against = from_iperf(att_config['against'], 'throughput')

    _, tm_tput_solo = from_iperf(tm_config['solo'], 'throughput')
    _, tm_tput_against = from_iperf(tm_config['against'], 'throughput')

    _, vz_tput_solo = from_iperf(vz_config['solo'], 'throughput')
    _, vz_tput_against = from_iperf(vz_config['against'], 'throughput')

    width = 0.20

    labels = ['AT\&T', 'T-Mobile', 'Verizon']
    x = np.arange(len(labels))

    y_solo = [
        round(np.mean(att_tput_solo)/mb, 4),
        round(np.mean(tm_tput_solo)/mb, 4),
        round(np.mean(vz_tput_solo)/mb, 4)
    ]

    y_against = [
        round(np.mean(att_tput_against)/mb, 4),
        round(np.mean(tm_tput_against)/mb, 4),
        round(np.mean(vz_tput_against)/mb, 4)
    ]

    harm_ls = '\n'.join([
        f'AT\&T (h): {harm_tput(y_solo[0], y_against[0])}',
        f'T-Mobile (h): {harm_tput(y_solo[1], y_against[1])}',
        f'Verizon (h): {harm_tput(y_solo[2], y_against[2])}'
    ])

    plt.figure(figsize=(8, 6))

    _, ax = plt.subplots()

    ax.bar(x-width, y_solo, width, label='Cubic', align='edge', capsize=5)
    ax.bar(x, y_against, width, label='Cubic + Mimic', align='edge', capsize=5)
    ax.set_ylabel('Throughput (Mbps)')
    # ax.set_xlabel('Throughput analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc="lower center", ncol=3)
    ax.add_artist(AnchoredText(harm_ls, loc='upper left', frameon=True))

    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)

    file_name = f'ts.harm.tput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def ts_harm_delay(att_config: dict, tm_config: dict, vz_config: dict) -> None:

    _, att_solo = from_iperf(att_config['solo'], 'rtt')
    _, att_against = from_iperf(att_config['against'], 'rtt')

    _, tm_solo = from_iperf(tm_config['solo'], 'rtt')
    _, tm_against = from_iperf(tm_config['against'], 'rtt')

    _, vz_solo = from_iperf(vz_config['solo'], 'rtt')
    _, vz_against = from_iperf(vz_config['against'], 'rtt')

    width = 0.20

    labels = ['AT\&T', 'T-Mobile', 'Verizon']
    x = np.arange(len(labels))

    y_solo = [
        round(np.mean(att_solo)/mb, 4),
        round(np.mean(tm_solo)/mb, 4),
        round(np.mean(vz_solo)/mb, 4)
    ]

    y_against = [
        round(np.mean(att_against)/mb, 4),
        round(np.mean(tm_against)/mb, 4),
        round(np.mean(vz_against)/mb, 4)
    ]

    harm_ls = '\n'.join([
        f'AT\&T (h): {harm_delay(y_solo[0], y_against[0])}',
        f'T-Mobile (h): {harm_delay(y_solo[1], y_against[1])}',
        f'Verizon (h): {harm_delay(y_solo[2], y_against[2])}'
    ])

    plt.figure(figsize=(8, 6))

    _, ax = plt.subplots()

    ax.bar(x-width, y_solo, width, label='Cubic', align='edge', capsize=5)
    ax.bar(x, y_against, width, label='Cubic + Mimic', align='edge', capsize=5)
    ax.set_ylabel('Latency  (ms)')
    # ax.set_xlabel('Time (s)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc="lower center", ncol=3)
    ax.add_artist(AnchoredText(harm_ls, loc='upper right', frameon=True))

    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)

    file_name = f'ts.harm.delay.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.pdf")}'
    plot_file_name = os.path.join(entry_path, 'images/thesis', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')
