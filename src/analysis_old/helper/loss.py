import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *


def plot_loss_all_arms_multi(config: dict, ):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'lost', bws)


    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'lost', bws)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'lost', bws)


    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'lost', bws)


    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'lost', bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color = '#ff7f0e')
    ax1.set_ylabel('Packet Lost')
    ax1.set_xlabel('Step')
    ax1.legend()


    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color = '#ff7f0e')
    ax2.set_ylabel('Packet Lost')
    ax2.set_xlabel('Step')
    ax2.legend()


    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color = '#ff7f0e')
    ax3.set_ylabel('Packet Lost')
    ax3.set_xlabel('Step')
    ax3.legend()

    
    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color = '#ff7f0e')
    ax4.set_ylabel('Packet Lost')
    ax4.set_xlabel('Step')
    ax4.legend()

    
    ax5 = plt.subplot(325)
    ax5.plot(x_mab, y_mab, label='Mimic', color = '#ff7f0e')
    ax5.set_ylabel('Packet Lost')
    ax5.set_xlabel('Step')
    ax5.legend()

    plt.xlabel('Step')
    plt.title('')

    file_name = f'{config["trace"]}.multi.arms.linear_lost.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/loss', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')

def plot_loss_all_arms(config: dict, ):
    owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff', 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
    owl_path = 'log/owl/trace'

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'lost', bws)


    df_hybla = to_dataframe(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'lost', bws)

    df_vegas = to_dataframe(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'lost', bws)


    df_mab = to_dataframe(config['mab'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'lost', bws)


    df_owl = to_dataframe(config['owl'], owl_columns, owl_path)
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'lost', bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic, label='Cubic')
    ax.plot(x_hybla, y_hybla, label='Hybla')
    ax.plot(x_vegas, y_vegas, label='Vegas')
    ax.plot(x_owl, y_owl, label='Owl')
    ax.plot(x_mab, y_mab, label='Mimic')

    plt.xlabel('Step')
    plt.ylabel('Packet Loss')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.arms.linear_lost.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/loss', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_prod_loss_all_arms(config: dict, ):
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, _ = get_plot_xyz(df_cubic, 'lost', config, bws)


    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'lost', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'lost', config, bws)


    df_mab = to_dataframe_prod(config['mimic'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'lost', config, bws)


    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'lost', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic, label='Cubic')
    ax.plot(x_hybla, y_hybla, label='Hybla')
    ax.plot(x_vegas, y_vegas, label='Vegas')
    ax.plot(x_owl, y_owl, label='Owl')
    ax.plot(x_mab, y_mab, label='Mimic')

    plt.xlabel('Step')
    plt.ylabel('Packet Loss')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.loss.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
