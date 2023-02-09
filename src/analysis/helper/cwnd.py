import os
from datetime import datetime
from re import M

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from helper.utils import *


def plot_cwnd(df: pd.DataFrame, title: str, bandwidths: list = [], max: int = None) -> None:

    _, ax = plt.subplots()

    x, y, bws = get_plot_xyz(df, 'cwnd', bandwidths, max)

    ax.plot(x[0:y.shape[0]], y, label='Congestion Window')

    if len(bandwidths) > 0:
        ax.plot(x[0:y.shape[0]], bws, label='Bandwidth')

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (Bytes)')
    plt.title(title)
    plt.legend()

    file_name = f'{title.replace(" ", "_")}.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_arm_cwnd(result_file: str, bw_file: str, title: str, colns: list = None, path: str = None):

    df = to_dataframe(result_file, colns, path)

    if title != "Mimic":
        N, _ = df.shape
        df = df[int(N/2):].reset_index()

    bandwidths = to_bandwidth_array_v2(bw_file)

    print(
        f'Arm: {title} \t Input: {df.shape[0]} \t BWs: {bandwidths.shape[0]}')

    plot_cwnd(df, title, bandwidths)


def plot_cwnd_all_arms_diff(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)
    cubic_mape = mape(y_cubic, z)
    y_cubic = np.subtract(y_cubic, z)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, z_hybla = get_plot_xyz(df_hybla, 'cwnd', config, bws)
    hybla_mape = mape(y_hybla, z_hybla)
    y_hybla = np.subtract(y_hybla, z_hybla)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, z_vegas = get_plot_xyz(df_vegas, 'cwnd', config, bws)
    vegas_mape = mape(y_vegas, z_vegas)
    y_vegas = np.subtract(y_vegas, z_vegas)

    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, z_mab = get_plot_xyz(df_mab, 'cwnd', config, bws)
    mab_mape = mape(y_mab, z_mab[0:y_mab.shape[0]])
    y_mab = np.subtract(y_mab, z_mab[0:y_mab.shape[0]])

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, z_owl = get_plot_xyz(df_owl, 'cwnd', config, bws)
    owl_mape = mape(y_owl, z_owl)
    y_owl = np.subtract(y_owl, z_owl)

    plt.figure(figsize=(15, 12))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic/kb, label=f'Cubic (mAPE: {cubic_mape})')
    ax.plot(x_hybla, y_hybla/kb, label=f'Hybla (mAPE: {hybla_mape})')
    ax.plot(x_vegas, y_vegas/kb, label=f'Vegas (mAPE: {vegas_mape})')
    ax.plot(x_owl, y_owl/kb, label=f'Owl (mAPE: {owl_mape})')
    ax.plot(x_mab[0:y_mab.shape[0]], y_mab/kb,
            label=f'Mimic (mAPE: {mab_mape})')

    plt.xlabel('Step')
    plt.ylabel('Bandwidth - Congestion Window (KB)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.diff.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_cwnd_all_arms(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, z_hybla = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, z_vegas = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, z_mab = get_plot_xyz(df_mab, 'cwnd', config, bws)

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, z_owl = get_plot_xyz(df_owl, 'cwnd', config, bws)

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic, label='Cubic')
    ax.plot(x_hybla, y_hybla, label='Hybla')
    ax.plot(x_vegas, y_vegas, label='Vegas')
    ax.plot(x_owl, y_owl, label='Owl')
    ax.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic')

    if len(z) > 0:
        ax.plot(x_cubic, z, label='Bandwidth')

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (Bytes)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_all_arms_multi(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, z_hybla = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, z_vegas = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, z_mab = get_plot_xyz(df_mab, 'cwnd', config, bws)

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, z_owl = get_plot_xyz(df_owl, 'cwnd', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic')

    if len(z) > 0:
        ax1.plot(x_cubic, z, label='Bandwidth')

    ax1.set_ylabel('Congestion Window Size (Bytes)')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla')

    if len(z_hybla) > 0:
        ax2.plot(x_hybla, z_hybla, label='Bandwidth')

    ax2.set_ylabel('Congestion Window Size (Bytes)')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas')

    if len(z_vegas) > 0:
        ax3.plot(x_vegas, z_vegas, label='Bandwidth')

    ax3.set_ylabel('Congestion Window Size (Bytes)')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl')

    if len(z_owl) > 0:
        ax4.plot(x_owl, z_owl, label='Bandwidth')

    ax4.set_ylabel('Congestion Window Size (Bytes)')
    ax4.set_xlabel('Step')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic')

    if len(z_mab) > 0:
        ax5.plot(x_mab[0:y_mab.shape[0]],
                 z_mab[0:y_mab.shape[0]], label='Bandwidth')

    ax5.set_ylabel('Congestion Window Size (Bytes)')
    ax5.set_xlabel('Step')
    ax5.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.multi.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_all_arms_multi_diff(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)
    cubic_mape = mape(y_cubic, z)
    y_cubic = np.subtract(y_cubic, z)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, z_hybla = get_plot_xyz(df_hybla, 'cwnd', config, bws)
    hybla_mape = mape(y_hybla, z_hybla)
    y_hybla = np.subtract(y_hybla, z_hybla)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, z_vegas = get_plot_xyz(df_vegas, 'cwnd', config, bws)
    vegas_mape = mape(y_vegas, z_vegas)
    y_vegas = np.subtract(y_vegas, z_vegas)

    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, z_mab = get_plot_xyz(df_mab, 'cwnd', config, bws)
    mab_mape = mape(y_mab, z_mab[0:y_mab.shape[0]])
    y_mab = np.subtract(y_mab, z_mab[0:y_mab.shape[0]])

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, z_owl = get_plot_xyz(df_owl, 'cwnd', config, bws)
    owl_mape = mape(y_owl, z_owl)
    y_owl = np.subtract(y_owl, z_owl)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label=f'Cubic (mAPE: {cubic_mape})')
    ax1.set_ylabel('Difference (Bandwidth - Congestion Window)')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label=f'Hybla (mAPE: {hybla_mape})')
    ax2.set_ylabel('Difference (Bandwidth - Congestion Window)')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label=f'Vegas (mAPE: {vegas_mape})')
    ax3.set_ylabel('Difference (Bandwidth - Congestion Window)')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label=f'Owl (mAPE: {owl_mape})')
    ax4.set_ylabel('Difference (Bandwidth - Congestion Window)')
    ax4.set_xlabel('Step')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab,
             label=f'Mimic: (mAPE: {mab_mape})')
    ax5.set_ylabel('Difference (Bandwidth - Congestion Window)')
    ax5.set_xlabel('Step')
    ax5.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.multi.diff.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_all_arms_multi_aoc(config: dict, show_bws: bool = True):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, z_hybla = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, z_vegas = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, z_mab = get_plot_xyz(df_mab, 'cwnd', config, bws)

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, z_owl = get_plot_xyz(df_owl, 'cwnd', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color='#ff7f0e')
    ax1.fill_between(x_cubic, y_cubic, alpha=0.2, color='#ff7f0e')

    if show_bws:
        ax1.plot(x_cubic, z, label='Bandwidth', color='#1f77b4')
        ax1.fill_between(x_cubic, z, alpha=0.5, color='#1f77b4')

    ax1.set_ylabel('Congestion Window (Bytes)')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color='#ff7f0e')
    ax2.fill_between(x_hybla, y_hybla, alpha=0.2, color='#ff7f0e')

    if show_bws:
        ax2.plot(x_cubic, z_hybla, label='Bandwidth', color='#1f77b4')
        ax2.fill_between(x_hybla, z_hybla, alpha=0.5, color='#1f77b4')

    ax2.set_ylabel('Congestion Window (Bytes)')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color='#ff7f0e')
    ax3.fill_between(x_vegas, y_vegas, alpha=0.2, color='#ff7f0e')

    if show_bws:
        ax3.plot(x_vegas, z_vegas, label='Bandwidth', color='#1f77b4')
        ax3.fill_between(x_vegas, z_vegas, alpha=0.5, color='#1f77b4')

    ax3.set_ylabel('Congestion Window (Bytes)')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color='#ff7f0e')
    ax4.fill_between(x_owl, y_owl, alpha=0.2, color='#ff7f0e')

    if show_bws:
        ax4.plot(x_owl, z_owl, label='Bandwidth', color='#1f77b4')
        ax4.fill_between(x_owl, z_owl, alpha=0.5, color='#1f77b4')

    ax4.set_ylabel('Congestion Window (Bytes)')
    ax4.set_xlabel('Step')
    ax4.legend()

    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic', color='#ff7f0e')
    ax5.fill_between(x_mab[0:y_mab.shape[0]], y_mab,
                     alpha=0.2, color='#ff7f0e')

    if show_bws:
        ax5.plot(x_mab[0:y_mab.shape[0]], z_mab[0:y_mab.shape[0]],
                 label='Bandwidth', color='#1f77b4')
        ax5.fill_between(
            x_mab[0:y_mab.shape[0]], z_mab[0:y_mab.shape[0]], alpha=0.5, color='#1f77b4')

    ax5.set_ylabel('Congestion Window (Bytes)')
    ax5.set_xlabel('Step')
    ax5.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.aoc.multi.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_all_policies(csv_files: list, csv_file_names: list):

    _, ax = plt.subplots()

    for i in range(len(csv_files)):
        policy = csv_file_names[i]
        run_file = csv_files[i]
        csv_file = os.path.join(entry_path, 'log/mab/trace', run_file)

        columns = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
        df = pd.read_csv(csv_file, names=columns)

        N = df.shape[0]
        x = [df['step'].values[i] for i in range(0, N, 100)]
        y = [df['cwnd'].values[i] for i in range(0, N, 100)]

        ax.plot(x, y, '.', label=policy)

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (Bytes)')
    plt.title('Congestion Window Evolution of all policies')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 10})

    plot_file_name = f'all_cwnd.{datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_cwnd_follow_multi(config: dict):
    config['step'] = 50
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_mab = to_dataframe(config['mab'])
    df_mab_vegas = df_mab[df_mab['action'] == 0]
    df_mab_owl = df_mab[df_mab['action'] == 1]
    df_mab_cubic = df_mab[df_mab['action'] == 2]
    df_mab_hybla = df_mab[df_mab['action'] == 3]

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'cwnd', config, bws)
    x_mab_cubic, y_mab_cubic, _ = get_plot_xyz(
        df_mab_cubic, 'cwnd', config, bws)
    y_cubic = y_cubic[0:y_mab_cubic.shape[0]]
    cubic_mape = mape(y_cubic, y_mab_cubic)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)
    x_mab_hybla, y_mab_hybla, _ = get_plot_xyz(
        df_mab_hybla, 'cwnd', config, bws)
    y_hybla = y_hybla[0:y_mab_hybla.shape[0]]
    hybla_mape = mape(y_hybla, y_mab_hybla)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)
    x_mab_vegas, y_mab_vegas, _ = get_plot_xyz(
        df_mab_vegas, 'cwnd', config, bws)
    y_vegas = y_vegas[0:y_mab_vegas.shape[0]]
    vegas_mape = mape(y_vegas, y_mab_vegas)

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)
    x_mab_owl, y_mab_owl, _ = get_plot_xyz(df_mab_owl, 'cwnd', config, bws)
    y_owl = y_owl[0:y_mab_owl.shape[0]]
    owl_mape = mape(y_owl, y_mab_owl)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(221)
    ax1.plot(x_mab_cubic, y_cubic/mb, label=f'Cubic')
    ax1.plot(x_mab_cubic, y_mab_cubic/mb, label=f'Mimic (mAPE: {cubic_mape})')
    ax1.set_ylabel('Congestion Window Size (KB)')
    ax1.set_xlabel('Step')
    ax1.legend()

    ax2 = plt.subplot(222)
    ax2.plot(x_mab_hybla, y_hybla/mb, label=f'Hybla')
    ax2.plot(x_mab_hybla, y_mab_hybla/mb, label=f'Mimic (mAPE: {hybla_mape})')
    ax2.set_ylabel('Congestion Window Size (KB)')
    ax2.set_xlabel('Step')
    ax2.legend()

    ax3 = plt.subplot(223)
    ax3.plot(x_mab_vegas, y_vegas/mb, label=f'Vegas (mAPE: {vegas_mape})')
    ax3.plot(x_mab_vegas, y_mab_vegas/mb, label=f'Mimic (mAPE: {vegas_mape})')
    ax3.set_ylabel('Congestion Window Size (KB)')
    ax3.set_xlabel('Step')
    ax3.legend()

    ax4 = plt.subplot(224)
    ax4.plot(x_mab_owl, y_owl/mb, label=f'Owl')
    ax4.plot(x_mab_owl, y_mab_owl/mb, label=f'Mimic (mAPE: {owl_mape})')
    ax4.set_ylabel('Congestion Window Size (KB)')
    ax4.set_xlabel('Step')
    ax4.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.multi.follow.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_follow(config: dict, arm: str) -> None:
    config['step'] = 50
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_mab = to_dataframe(config['mab'])
    df_mab_vegas = df_mab[df_mab['action'] == 0]
    df_mab_owl = df_mab[df_mab['action'] == 1]
    df_mab_cubic = df_mab[df_mab['action'] == 2]
    df_mab_hybla = df_mab[df_mab['action'] == 3]

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'cwnd', config, bws)
    x_mab_cubic, y_mab_cubic, _ = get_plot_xyz(
        df_mab_cubic, 'cwnd', config, bws)
    y_cubic = y_cubic[0:y_mab_cubic.shape[0]]
    cubic_mape = mape(y_cubic, y_mab_cubic)

    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)
    x_mab_hybla, y_mab_hybla, _ = get_plot_xyz(
        df_mab_hybla, 'cwnd', config, bws)
    y_hybla = y_hybla[0:y_mab_hybla.shape[0]]
    hybla_mape = mape(y_hybla, y_mab_hybla)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)
    x_mab_vegas, y_mab_vegas, _ = get_plot_xyz(
        df_mab_vegas, 'cwnd', config, bws)
    y_vegas = y_vegas[0:y_mab_vegas.shape[0]]
    vegas_mape = mape(y_vegas, y_mab_vegas)

    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)
    x_mab_owl, y_mab_owl, _ = get_plot_xyz(df_mab_owl, 'cwnd', config, bws)
    y_owl = y_owl[0:y_mab_owl.shape[0]]
    owl_mape = mape(y_owl, y_mab_owl)

    plt.figure(figsize=(5, 8))

    _, ax = plt.subplots()

    if arm == 'cubic':
        ax.plot(x_mab_cubic, y_cubic/mb, label=f'Cubic')
        ax.plot(x_mab_cubic, y_mab_cubic/mb,
                label=f'Mimic (mAPE: {cubic_mape})')
        ax.set_ylabel('Congestion Window Size (KB)')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'hybla':
        ax.plot(x_mab_hybla, y_hybla/mb, label=f'Hybla')
        ax.plot(x_mab_hybla, y_mab_hybla/mb,
                label=f'Mimic (mAPE: {hybla_mape})')
        ax.set_ylabel('Congestion Window Size (KB)')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'vegas':
        ax.plot(x_mab_vegas, y_vegas/mb, label=f'Vegas (mAPE: {vegas_mape})')
        ax.plot(x_mab_vegas, y_mab_vegas/mb,
                label=f'Mimic (mAPE: {vegas_mape})')
        ax.set_ylabel('Congestion Window Size (KB)')
        ax.set_xlabel('Step')
        ax.legend()

    if arm == 'owl':
        ax.plot(x_mab_owl, y_owl/mb, label=f'Owl')
        ax.plot(x_mab_owl, y_mab_owl/mb, label=f'Mimic (mAPE: {owl_mape})')
        ax.set_ylabel('Congestion Window Size (KB)')
        ax.set_xlabel('Step')
        ax.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.{arm}.follow.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_cwnd_all_policies(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_x1 = to_dataframe(config['ActiveExplorer'])
    x1, y1, z = get_plot_xyz(df_x1, 'cwnd', config, bws)

    df_x2 = to_dataframe(config['AdaptiveGreedyWithPercentile'])
    x2, y2, _ = get_plot_xyz(df_x2, 'cwnd', config, bws)

    df_x3 = to_dataframe(config['AdaptiveGreedyWithThreshold'])
    x3, y3, _ = get_plot_xyz(df_x3, 'cwnd', config, bws)

    df_x4 = to_dataframe(config['BootstrappedTS'])
    x4, y4, _ = get_plot_xyz(df_x4, 'cwnd', config, bws)

    df_x5 = to_dataframe(config['BootstrappedUCB'])
    x5, y5, _ = get_plot_xyz(df_x5, 'cwnd', config, bws)

    df_x6 = to_dataframe(config['EpsilonGreedyWithDecay'])
    x6, y6, _ = get_plot_xyz(df_x6, 'cwnd', config, bws)

    df_x7 = to_dataframe(config['EpsilonGreedyWithoutDecay'])
    x7, y7, _ = get_plot_xyz(df_x7, 'cwnd', config, bws)

    df_x8 = to_dataframe(config['SeparateClassifiers'])
    x8, y8, _ = get_plot_xyz(df_x8, 'cwnd', config, bws)

    df_x9 = to_dataframe(config['cubic'])
    x9, y9, _ = get_plot_xyz(df_x9, 'cwnd', config, bws)

    df_x10 = to_dataframe(config['hybla'])
    x10, y10, _ = get_plot_xyz(df_x10, 'cwnd', config, bws)

    df_x11 = to_dataframe(config['vegas'])
    x11, y11, _ = get_plot_xyz(df_x11, 'cwnd', config, bws)

    df_x12 = to_dataframe(config['owl'], owl_columns, owl_path)
    x12, y12, _ = get_plot_xyz(df_x12, 'cwnd', config, bws)

    df_x13 = to_dataframe(config['SoftmaxExplorer'])
    x13, y13, _ = get_plot_xyz(df_x13, 'cwnd', config, bws)

    df_x14 = to_dataframe(config['AdaptiveGreedyWeighted'])
    x14, y14, _ = get_plot_xyz(df_x14, 'cwnd', config, bws)

    _, ax = plt.subplots()

    x = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
    y = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14]
    x_ticks = ['ActiveExplorer', 'AdaptiveGreedyWithPercentile', 'AdaptiveGreedyWithThreshold', 'BootstrappedTS', 'BootstrappedUCB',
               'EpsilonGreedyWithDecay', 'EpsilonGreedyWithoutDecay', 'SeparateClassifiers', 'Cubic', 'Hybla', 'Vegas', 'Owl', 'SoftmaxExplorer', 'AdaptiveGreedyWeighted']

    color = ['red', 'blue', 'yellow', 'green', 'pink', 'grey', 'gold',
             'cyan', 'skyblue', 'violet', 'magenta', 'brown', 'olive', 'indigo']

    i = 0

    for a, b in zip(x, y):
        ax.plot(a, b, label=x_ticks[i], c=color[i])
        i += 1

    if len(z) > 0:
        ax.plot(x1, z, label='Bandwidth')

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (Bytes)')
    plt.title('')
    # plt.legend()

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 1.25])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 10})

    file_name = f'{config["trace"]}.arms.linear_cwnd.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/cwnd', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_prod_cwnd(config: dict):
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_mimic = to_dataframe_prod(config['mimic'])
    x, y_mimic, z = get_plot_xyz(df_mimic, 'cwnd', config, bws)

    df_cubic = to_dataframe_prod(config['cubic'])
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'cwnd', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    x, y_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    x, y_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)

    _, ax = plt.subplots()

    ax.plot(x, y_mimic/mb, label='Mimic', c='blue')
    ax.plot(x, y_cubic/mb, label='Cubic', c='black')
    ax.plot(x, y_vegas/mb, label='Vegas', c='green')
    ax.plot(x, y_hybla/mb, label='Hybla', c='violet')
    ax.plot(x, y_owl/mb, label='Owl', c='red')

    if len(z) > 0:
        ax.plot(x, z/mb, label='Bandwidth', c='red')

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (MB)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.cwnd.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_prod_cwnd_diff(config: dict):
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x, y_cubic, z = get_plot_xyz(df_cubic, 'cwnd', config, bws)
    cubic_mape = mape(y_cubic/mb, z/mb)
    y_cubic = np.subtract(y_cubic/mb, z/mb)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'cwnd', config, bws)
    hybla_mape = mape(y_hybla/mb, z/mb)
    y_hybla = np.subtract(y_hybla/mb, z/mb)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'cwnd', config, bws)
    vegas_mape = mape(y_vegas/mb, z/mb)
    y_vegas = np.subtract(y_vegas/mb, z/mb)

    df_mimic = to_dataframe_prod(config['mimic'])
    _, y_mimic, _ = get_plot_xyz(df_mimic, 'cwnd', config, bws)
    mab_mape = mape(y_mimic/mb, z/mb)
    y_mimic = np.subtract(y_mimic/mb, z/mb)

    df_owl = to_dataframe_prod(config['owl'])
    _, y_owl, _ = get_plot_xyz(df_owl, 'cwnd', config, bws)
    owl_mape = mape(y_owl/mb, z/mb)
    y_owl = np.subtract(y_owl/mb, z/mb)


    plt.figure(figsize=(15, 12))

    _, ax = plt.subplots()

    ax.plot(x, y_cubic, label=f'Cubic (mAPE: {cubic_mape})')
    ax.plot(x, y_hybla, label=f'Hybla (mAPE: {hybla_mape})')
    ax.plot(x, y_vegas, label=f'Vegas (mAPE: {vegas_mape})')
    ax.plot(x, y_mimic, label=f'Mimic (mAPE: {mab_mape})')
    ax.plot(x, y_owl, label=f'Owl (mAPE: {owl_mape})')

    plt.xlabel('Step')
    plt.ylabel('Bandwidth - Congestion Window (MB)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.bw.minux.cwnd.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_prod_cwnd_model(config: dict) -> None:
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df = to_dataframe_prod(config['mimic'])

    models = np.unique(df['model'])

    x = {}
    y = {}

    for model in models:
        y[model] = df[df['model'] == model]['cwnd'].values
        N = y[model].shape[0]
        x[model] = np.arange(N)

    _, ax = plt.subplots()

    for model in models:
        ax.plot(x[model], y[model]/kb, label=model)

    plt.xlabel('Step')
    plt.ylabel('Congestion Window (KB)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.cwnd.model.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')
