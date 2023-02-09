import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *


def plot_mape_arms(config: dict):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
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

    plt.figure(figsize=(15, 10))

    _, ax = plt.subplots()

    x = ['Cubic', 'Vegas', 'Hybla', 'Owl', 'Mab']
    y = np.array([cubic_mape, vegas_mape, hybla_mape, owl_mape, mab_mape]) * 100

    ax.bar(x, y)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.xlabel('Congestion Control Algorithms')
    plt.ylabel('mAPE (%)')

    bar_widths = [p.get_width() for p in ax.patches]

    for i, v in enumerate(y):
        bw = bar_widths[i] / 4
        ax.text(i - bw, v + 2, str(round(v, 2)), color='black')

    file_name = f'{config["trace"]}.mape.bar_arms.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/mape', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)

def plot_mape_arms_multi(config: dict):
    pass