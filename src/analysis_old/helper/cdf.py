from copy import deepcopy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *
from astropy.visualization import hist


def plot_cdf(x: np.ndarray, location: int, title: str, xlabel: str, label: str) -> None:

    mu = 200
    sigma = 25
    ax = plt.subplot(location)

    # plot the cumulative histogram
    n, bins, patches = hist(x, bins='scott', density=True,
                            histtype='step', cumulative=True, label=label)

    # Add a line showing the expected distribution.
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    y = y.cumsum()
    y /= y[-1]

    # ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

    # Overlay a reversed cumulative histogram.
    # hist(x, bins='scott', density=True, histtype='step',
    #      cumulative=-1, label='Reversed emp.')

    # tidy up the figure
    ax.legend(loc='right')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Likelihood of occurrence')

def plot_cdf_throughput_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'throughput')

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

    plot_cdf(y_cubic/mb, 321,
             f'{config["trace"]} | Cubic | Throughput CDF', 'Throughput (Mbps)', 'Cubic')

    plot_cdf(y_hybla/mb, 322,
             f'{config["trace"]} | Hybla | Throughput CDF', 'Throughput (Mbps)', 'Hybla')

    plot_cdf(y_vegas/mb, 323,
             f'{config["trace"]} | Vegas | Throughput CDF', 'Throughput (Mbps)', 'Vegas')

    plot_cdf(y_owl/mb, 324,
             f'{config["trace"]} | Owl | Throughput CDF', 'Throughput (Mbps)', 'Owl')

    plot_cdf(y_mimic/mb, 325,
             f'{config["trace"]} | Mimic | Throughput CDF', 'Throughput (Mbps)', 'Mimic')

    plot_cdf(y_basic/mb, 326,
             f'{config["trace"]} | Basic | Throughput CDF', 'Throughput (Mbps)', 'Basic')

    file_name = f'{config["trace"]}.iperf.cdf.throughput.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')

def plot_cdf_latency_multi(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'rtt')

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

    plot_cdf(y_cubic/mb, 321,
             f'{config["trace"]} | Cubic | Latency CDF', 'Latency (s)', 'Cubic')

    plot_cdf(y_hybla/mb, 322,
             f'{config["trace"]} | Hybla | Latency CDF', 'Latency (s)', 'Hybla')

    plot_cdf(y_vegas/mb, 323,
             f'{config["trace"]} | Vegas | Latency CDF', 'Latency (s)', 'Vegas')

    plot_cdf(y_owl/mb, 324,
             f'{config["trace"]} | Owl | Latency CDF', 'Latency (s)', 'Owl')

    plot_cdf(y_mimic/mb, 325,
             f'{config["trace"]} | Mimic | Latency CDF', 'Latency (s)', 'Mimic')

    plot_cdf(y_basic/mb, 326,
             f'{config["trace"]} | Basic | Latency CDF', 'Latency (s)', 'Basic')

    file_name = f'{config["trace"]}.iperf.cdf.latency.multi.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')

def plot_cdf_latency(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'rtt')

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

    hist(y_cubic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Vegas', color='yellow')
    hist(y_basic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Mimic', color='green')

    plt.ylabel('Likelihood of occurrence')
    plt.xlabel('Latency (s)')
    plt.title(f'{config["trace"]} | Latency CDF')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.cdf.latency.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')

def plot_cdf_throughput(config: dict) -> None:

    df_cubic = get_iperf_log(config['cubic_iperf'])
    _, y_cubic = get_iperf_xyz(df_cubic, 'throughput')

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

    hist(y_cubic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Vegas', color='yellow')
    hist(y_basic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Mimic', color='green')

    plt.ylabel('Likelihood of occurrence')
    plt.xlabel('Throughput (Mbps)')
    plt.title(f'{config["trace"]} | Throughput CDF')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.cdf.throughput.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')

def plot_cdf_latency_all(config: dict) -> None:

    _, y_cubic = get_iperf_xyz_all('cubic', config['trace'], 'rtt')

    _, y_hybla = get_iperf_xyz_all('hybla', config['trace'], 'rtt')

    _, y_vegas = get_iperf_xyz_all('vegas', config['trace'], 'rtt')

    _, y_mimic = get_iperf_xyz_all('mimic', config['trace'], 'rtt')

    _, y_owl = get_iperf_xyz_all('owl', config['trace'], 'rtt')

    _, y_basic = get_iperf_xyz_all('bs', config['trace'], 'rtt')

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    hist(y_cubic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Vegas', color='yellow')
    hist(y_basic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Mimic', color='green')

    plt.ylabel('Likelihood of occurrence')
    plt.xlabel('Latency (s)')
    plt.title(f'{config["trace"]} | Latency CDF')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.cdf.latency.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')

def plot_cdf_throughput_all(config: dict) -> None:

    _, y_cubic = get_iperf_xyz_all('cubic', config['trace'], 'throughput')

    _, y_hybla = get_iperf_xyz_all('hybla', config['trace'], 'throughput')

    _, y_vegas = get_iperf_xyz_all('vegas', config['trace'], 'throughput')

    _, y_mimic = get_iperf_xyz_all('mimic', config['trace'], 'throughput')

    _, y_owl = get_iperf_xyz_all('owl', config['trace'], 'throughput')

    _, y_basic = get_iperf_xyz_all('bs', config['trace'], 'throughput')
    
    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    hist(y_cubic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Cubic', color='red')
    hist(y_hybla/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Hybla', color='black')
    hist(y_owl/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Owl', color='blue')
    hist(y_vegas/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Vegas', color='yellow')
    hist(y_basic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Basic', color='magenta')
    hist(y_mimic/mb, bins='scott', density=True, histtype='step', cumulative=True, label='Mimic', color='green')

    plt.ylabel('Likelihood of occurrence')
    plt.xlabel('Throughput (Mbps)')
    plt.title(f'{config["trace"]} | Throughput CDF')
    plt.legend()

    file_name = f'{config["trace"]}.iperf.cdf.throughput.all.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, dpi=300, bbox_inches='tight', pad_inches=0.2)
    plt.close('all')