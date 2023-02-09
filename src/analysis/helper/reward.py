import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *


def plot_prod_reward(config: dict) -> None:

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x, y_cubic, _ = get_plot_xyz(df_cubic, 'reward', config, bws)

    df_hybla = to_dataframe_prod(config['hybla'])
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'reward', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'reward', config, bws)

    df_mimic = to_dataframe_prod(config['mimic'])
    _, y_mimic, _ = get_plot_xyz(df_mimic, 'reward', config, bws)

    df_owl = to_dataframe_prod(config['owl'])
    _, y_owl, _ = get_plot_xyz(df_owl, 'reward', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x, y_mimic, label='Mimic', c='blue')
    ax.plot(x, y_cubic, label='Cubic', c='black')
    ax.plot(x, y_vegas, label='Vegas', c='green')
    ax.plot(x, y_hybla, label='Hybla', c='violet')
    ax.plot(x, y_owl, label='Owl', c='red')

    plt.xlabel('Step')
    plt.ylabel('Reward')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.reward.linear.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)