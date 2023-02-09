from copy import deepcopy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *

def plot_prod_latency_multi(cf: dict):
    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'rtt', config, bws)


    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)


    df_mab = to_dataframe_prod(config['mimic'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)


    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color = '#ff7f0e')
    ax1.set_ylabel('Latency (s)')
    ax1.set_xlabel('Step')
    ax1.legend()


    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color = '#ff7f0e')
    ax2.set_ylabel('Latency (s)')
    ax2.set_xlabel('Step')
    ax2.legend()


    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color = '#ff7f0e')
    ax3.set_ylabel('Latency (s)')
    ax3.set_xlabel('Step')
    ax3.legend()

    
    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color = '#ff7f0e')
    ax4.set_ylabel('Latency (s)')
    ax4.set_xlabel('Step')
    ax4.legend()

    
    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic', color = '#ff7f0e')
    ax5.set_ylabel('Latency (s)')
    ax5.set_xlabel('Step')
    ax5.legend()

    file_name = f'{config["trace"]}.latency.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')

def plot_prod_latency(cf: dict):
    config = deepcopy(cf)
    config['step'] = 1

    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []

    df_cubic = to_dataframe_prod(config['cubic'])
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic, 'rtt', config, bws)


    df_hybla = to_dataframe_prod(config['hybla'])
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)


    df_mab = to_dataframe_prod(config['mimic'])
    x_mab, y_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)


    df_owl = to_dataframe_prod(config['owl'])
    x_owl, y_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x_cubic, y_cubic, label='Cubic')
    ax.plot(x_hybla, y_hybla, label='Hybla')
    ax.plot(x_vegas, y_vegas, label='Vegas')
    ax.plot(x_owl, y_owl, label='Owl')
    ax.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic')

    plt.xlabel('Step')
    plt.ylabel('Latency (s)')
    plt.title('')
    plt.legend()

    file_name = f'{config["trace"]}.latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)

def plot_latency_throughput_multi(config: dict):
    bws = to_bandwidth_array_v2(config['bw']) if config['bw'] != None else []   

    df_cubic = to_dataframe_prod(config['cubic'])
    df_cubic['throughput'] = get_throughput(df_cubic['cwnd'].values, df_cubic['rtt'].values)
    _, y_cubic, _ = get_plot_xyz(df_cubic, 'rtt', config, bws)
    _, x_cubic, _ = get_plot_xyz(df_cubic, 'throughput', config, bws)


    df_hybla = to_dataframe_prod(config['hybla'])
    df_hybla['throughput'] = get_throughput(df_hybla['cwnd'].values, df_hybla['rtt'].values)
    _, y_hybla, _ = get_plot_xyz(df_hybla, 'rtt', config, bws)
    _, x_hybla, _ = get_plot_xyz(df_hybla, 'throughput', config, bws)

    df_vegas = to_dataframe_prod(config['vegas'])
    df_vegas['throughput'] = get_throughput(df_vegas['cwnd'].values, df_vegas['rtt'].values)
    _, y_vegas, _ = get_plot_xyz(df_vegas, 'rtt', config, bws)
    _, x_vegas, _ = get_plot_xyz(df_vegas, 'throughput', config, bws)


    df_mab = to_dataframe_prod(config['mab'])
    df_mab['throughput'] = get_throughput(df_mab['cwnd'].values, df_mab['rtt'].values)
    _, y_mab, _ = get_plot_xyz(df_mab, 'rtt', config, bws)
    _, x_mab, _ = get_plot_xyz(df_mab, 'throughput', config, bws)


    df_owl = to_dataframe_prod(config['owl'], owl_columns, owl_path)
    df_owl['throughput'] = get_throughput(df_owl['cwnd'].values, df_owl['rtt'].values)
    _, y_owl, _ = get_plot_xyz(df_owl, 'rtt', config, bws)
    _, x_owl, _ = get_plot_xyz(df_owl, 'throughput', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color = '#ff7f0e')
    ax1.set_xlabel('Throughput (Gbps)')
    ax1.set_ylabel('Latency (s)')
    ax1.legend()


    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color = '#ff7f0e')
    ax2.set_xlabel('Throughput (Gbps)')
    ax2.set_ylabel('Latency (s)')
    ax2.legend()


    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color = '#ff7f0e')
    ax3.set_xlabel('Throughput (Gbps)')
    ax3.set_ylabel('Latency (s)')
    ax3.legend()

    
    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color = '#ff7f0e')
    ax4.set_xlabel('Throughput (Gbps)')
    ax4.set_ylabel('Latency (s)')
    ax4.legend()

    
    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic', color = '#ff7f0e')
    ax5.set_xlabel('Throughput (Gbps)')
    ax5.set_ylabel('Latency (s)')
    ax5.legend()

    file_name = f'{config["trace"]}.multi.arms.latency_throughput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/latency', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_prod_latency_evolution(config: dict, step: int) -> None:

    cf = deepcopy(config)
    cf['step'] = 1
    bws = to_bandwidth_array_v2(cf['bw']) if cf['bw'] != None else []        

    df_cubic = to_dataframe_prod(cf['cubic'])
    df_cubic_new = df_cubic[df_cubic["step"] == step]
    x_cubic, y_cubic, z = get_plot_xyz(df_cubic_new, 'rtt', config, bws)



    df_hybla = to_dataframe_prod(cf['hybla'])
    df_hybla_new = df_hybla[df_hybla["step"] == step]
    x_hybla, y_hybla, _ = get_plot_xyz(df_hybla_new, 'rtt', config, bws)

    df_vegas = to_dataframe_prod(cf['vegas'])
    df_vegas_new = df_vegas[df_vegas["step"] == step]
    x_vegas, y_vegas, _ = get_plot_xyz(df_vegas_new, 'rtt', config, bws)

    df_mab = to_dataframe_prod(cf['mimic'])
    df_mab_new = df_mab[df_mab["step"] == step]
    x_mab, y_mab, _ = get_plot_xyz(df_mab_new, 'rtt', config, bws)

    df_owl = to_dataframe_prod(cf['owl'])
    df_owl_new = df_owl[df_owl["step"] == step]
    x_owl, y_owl, _ = get_plot_xyz(df_owl_new, 'rtt', config, bws)

    plt.figure(figsize=(20, 15))

    ax1 = plt.subplot(321)
    ax1.plot(x_cubic, y_cubic, label='Cubic', color = '#ff7f0e')
    ax1.set_ylabel('Latency (s)')
    ax1.set_xlabel('Step')
    ax1.legend()


    ax2 = plt.subplot(322)
    ax2.plot(x_hybla, y_hybla, label='Hybla', color = '#ff7f0e')
    ax2.set_ylabel('Latency (s)')
    ax2.set_xlabel('Step')
    ax2.legend()


    ax3 = plt.subplot(323)
    ax3.plot(x_vegas, y_vegas, label='Vegas', color = '#ff7f0e')
    ax3.set_ylabel('Latency (s)')
    ax3.set_xlabel('Step')
    ax3.legend()

    
    ax4 = plt.subplot(324)
    ax4.plot(x_owl, y_owl, label='Owl', color = '#ff7f0e')
    ax4.set_ylabel('Latency (s)')
    ax4.set_xlabel('Step')
    ax4.legend()

    
    ax5 = plt.subplot(325)
    ax5.plot(x_mab[0:y_mab.shape[0]], y_mab, label='Mimic', color = '#ff7f0e')
    ax5.set_ylabel('Latency (s)')
    ax5.set_xlabel('Step')
    ax5.legend()

    file_name = f'{config["trace"]}.step.latency.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


