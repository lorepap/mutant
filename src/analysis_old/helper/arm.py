import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *

def plot_arms_total_picks(config: dict):

    df = to_dataframe(config['mab'])
    offset = 4900

    x0 = df[df['action'] == 0].shape[0]
    x1 = df[df['action'] == 1].shape[0]
    x2 = df[df['action'] == 2].shape[0]
    x3 = df[df['action'] == 3].shape[0]
    x = ['vegas', 'owl', 'cubic', 'hybla']
    y = np.array([x0, x1, x2, x3]) - offset

    df = pd.DataFrame({'x' : x , 'y' : y})
    df = df.sort_values('y', ascending=True)

    _, ax = plt.subplots()

    ax.barh(df['x'], df['y'])
    plt.ylabel('Arm')
    plt.xlabel('Total times chosen')

    ax.set_xticks([])
    ax.set_xticklabels([])

    for i in range(len(y)):
        # ax.text(i - .15, v + 10, str(v), color='blue', fontweight='bold')
        # plt.annotate(y[i], (-0.1 + i, y[i] + 10))
        plt.annotate(y[i] + offset, (y[i] + 5, -0.1 + i))

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)

    plot_file_name = f'{config["trace"]}.chosen.bar_arms.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_prod_arms_total_picks(config: dict):

    df = to_dataframe_prod(config['mimic'])
    offset = 300

    x0 = df[df['action'] == 0].shape[0]
    x1 = df[df['action'] == 1].shape[0]
    x2 = df[df['action'] == 2].shape[0]
    x3 = df[df['action'] == 3].shape[0]
    x = ['cubic', 'hybla', 'owl', 'vegas']
    y = np.array([x0, x1, x2, x3]) - offset

    df = pd.DataFrame({'x' : x , 'y' : y})
    df = df.sort_values('y', ascending=True).reset_index()

    _, ax = plt.subplots()

    ax.barh(df['x'], df['y'])
    plt.ylabel('Arm')
    plt.xlabel('Total times chosen')

    y = df['y']

    ax.set_xticks([])
    ax.set_xticklabels([])

    for i in range(len(y)):
        # ax.text(i - .15, v + 10, str(v), color='blue', fontweight='bold')
        # plt.annotate(y[i], (-0.1 + i, y[i] + 10))
        plt.annotate(y[i] + offset, (y[i], i))

    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # frame1 = plt.gca()
    # frame1.axes.get_xaxis().set_visible(False)

    plot_file_name = f'{config["trace"]}.protocol.chosen.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'images/prod', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)