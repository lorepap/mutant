from copy import deepcopy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *
import matplotlib.ticker as ticker


def plot_model_selected(config: dict) -> None:

    cf = deepcopy(config)
    cf['step'] = 1

    df = to_dataframe_prod(cf['mimic'])
    x = np.arange(1, df.shape[0] + 1)
    y = df['model']

    _, ax = plt.subplots()

    ax.scatter(x, y, label='Model', c='blue')


    plt.xlabel('Step')
    plt.ylabel('Model')
    plt.title('')

    file_name = f'{config["trace"]}.model.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')

def plot_protocol_selected(config: dict) -> None:

    cf = deepcopy(config)
    cf['step'] = 1

    df = to_dataframe_prod(cf['mimic'])
    x = np.arange(1, df.shape[0] + 1)
    y = df['protocol']

    _, ax = plt.subplots()

    ax.scatter(x, y, label='Protocol', c='blue')


    plt.xlabel('Step')
    plt.ylabel('Protocol')
    plt.title('')

    file_name = f'{config["trace"]}.protocol.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_protocol_selected_dir(path: str, max: int = 10) -> None:

    files = sorted(os.listdir(path))

    axcolor = 'red'
    ax1color = '#1f77b4'

    index = 0


    for file in files:

        plt.figure(figsize=(20, 15))

        if not file.endswith('.json') or '.mimic' not in file:
            continue

        if index == max:
            break

        xtput, ytput = from_iperf(file, 'throughput')
        xrtt, yrtt = from_iperf(file, 'rtt')
        xcwnd, ycwnd = from_iperf(file, 'cwnd')

        df = to_dataframe_prod(file.replace('.json', '.csv'))
        y = df['action'][0:60]
        x = np.arange(1, y.shape[0] + 1)

        ax1 = plt.subplot(221)
        ax1.plot(xtput, ytput/mb, color=ax1color)
        ax1.fill_between(xtput, 0, ytput/mb, color=ax1color)
        ax1.set_ylabel('Throughput (Mbps)', color=ax1color)
        ax1.set_xlabel('Time (s)')
        ax1.tick_params(axis ='y', labelcolor = ax1color)
        ax11 = ax1.twinx()
        ax11.tick_params(axis ='y', labelcolor = axcolor)
        ax11.set_ylabel('Protocol Selected', color = axcolor)
        ax11.plot(x, y, label='Protocol', c='black',
            markerfacecolor = axcolor, marker='o', linestyle='-.')
        ax11.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
        ax11.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])
        ax11.set_xlabel('Time (s)')

        ax2 = plt.subplot(222)
        ax2.plot(xrtt, yrtt/nb, color=ax1color)
        ax2.fill_between(xrtt, 0, yrtt/nb, color=ax1color)
        ax2.set_ylabel('Latency (s)', color=ax1color)
        ax2.set_xlabel('Time (s)')
        ax2.tick_params(axis ='y', labelcolor = ax1color)
        ax21 = ax2.twinx()
        ax21.tick_params(axis ='y', labelcolor = axcolor)
        ax21.set_ylabel('Protocol Selected', color = axcolor)
        ax21.plot(x, y, label='Protocol', c='black',
            markerfacecolor = axcolor, marker='o', linestyle='-.')
        ax21.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
        ax21.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])
        ax21.set_xlabel('Time (s)')

        ax3 = plt.subplot(223)
        ax3.plot(xcwnd, ycwnd/mb, color=ax1color)
        ax3.fill_between(xcwnd, 0, ycwnd/mb, color=ax1color)
        ax3.set_ylabel('Cwnd (MB)')
        ax3.set_xlabel('Time (s)')
        ax3.tick_params(axis ='y', labelcolor = ax1color)
        ax31 = ax3.twinx()
        ax31.tick_params(axis ='y', labelcolor = axcolor)
        ax31.set_ylabel('Protocol Selected', color = axcolor)
        ax31.plot(x, y, label='Protocol', c='black',
            markerfacecolor = axcolor, marker='o', linestyle='-.')
        ax31.yaxis.set_major_locator(ticker.FixedLocator([0, 1, 2, 3]))
        ax31.set_yticklabels(['cubic', 'hybla', 'owl', 'vegas'])
        ax31.set_xlabel('Time (s)')


        file_name = f'protocol.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
        plot_file_name = os.path.join(entry_path, 'images/protocol', file_name)

        plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
        plt.close('all')

        index += 1