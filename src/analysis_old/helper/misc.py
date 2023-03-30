import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from helper.utils import *

def plot_arm_all_policies(config: dict, max: int = None) -> None:

    N = 5000
    steps = 1
    x = np.array([i for i in range(0, N, steps)])

    if max is not None:
        x = np.array([i for i in range(0, max, steps)])

    df1 = to_dataframe('2021.06.30.09.59.25.csv')
    y1 = df1['action']
    y1 = y1[int(df1.shape[0]/2):].values

    df2 = to_dataframe('2021.06.30.10.31.57.csv')
    y2 = df2['action']
    y2 = y2[int(df2.shape[0]/2):].values

    df3 = to_dataframe('2021.06.30.10.57.09.csv')
    y3 = df3['action']
    y3 = y3[int(df3.shape[0]/2):].values

    df4 = to_dataframe('2021.06.30.11.16.43.csv')
    y4 = df4['action']
    y4 = y4[int(df4.shape[0]/2):].values

    df5 = to_dataframe('2021.06.30.11.37.02.csv')
    y5 = df5['action']
    y5 = y5[int(df5.shape[0]/2):].values

    df6 = to_dataframe('2021.07.05.22.02.53.csv')
    y6 = df6['action']
    y6 = y6[int(df6.shape[0]/2):].values

    df7 = to_dataframe('2021.07.05.22.49.26.csv')
    y7 = df7['action']
    y7 = y7[int(df7.shape[0]/2):].values

    df8 = to_dataframe('2021.07.05.23.57.15.csv')
    y8 = df8['action']
    y8 = y8[int(df8.shape[0]/2):].values

    df9 = to_dataframe('2021.07.06.18.04.37.csv')
    y9 = df9['action']
    y9 = y9[int(df9.shape[0]/2):].values

    df10 = to_dataframe('2021.07.06.19.13.35.csv')
    y10 = df10['action']
    y10 = y10[int(df10.shape[0]/2):].values

    df11 = to_dataframe('2021.07.06.19.39.02.csv')
    y11 = df11['action']
    y11 = y11[int(df11.shape[0]/2):].values

    if max is not None:
        y1 = y1[0:max]
        y2 = y2[0:max]
        y3 = y3[0:max]
        y4 = y4[0:max]
        y5 = y5[0:max]
        y6 = y6[0:max]
        y7 = y7[0:max]
        y8 = y8[0:max]
        y9 = y9[0:max]
        y10 = y10[0:max]
        y11 = y11[0:max]

    plt.figure(figsize=(20, 15))

    _, ax = plt.subplots()

    ax.plot(x,    y1,  '.',    label='Bootstrapped Upper-Confidence Bound')
    ax.plot(x,    y2,  '.',    label='Bootstrapped Thompson Sampling')
    ax.plot(x,    y3,  '.',    label='Separate Classifiers + Beta Prior')
    ax.plot(x,    y4,  '.',    label='Epsilon-Greedy with decay')
    ax.plot(x,    y5,  '.',    label='Epsilon-Greedy without decay')
    ax.plot(x,    y6,  '.',    label='Adaptive Greedy with decaying threshold')
    ax.plot(x,    y7,  '.',    label='Adaptive Greedy with decaying percentile')
    ax.plot(x,    y8,  '.',    label='Explore First with 1,500 explore rounds')
    ax.plot(x,    y9,  '.',    label='Active Explorer')
    ax.plot(x,   y10,  '.',    label='Adaptive Active Greedy')
    ax.plot(x,   y11,  '.',    label='Softmax Explorer')

    plt.xlabel('Step')
    plt.ylabel('Congestion Protocols Chosen')
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['vegas', 'owl', 'cubic', 'hybla'])
    plt.title('')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 1.25])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 10})

    file_name = f'arms.linear_policies.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots/arm', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_arm_all_policies_multi(config: dict, max: int = None) -> None:

    N = 5000
    steps = 1
    x = np.array([i for i in range(0, N, steps)])

    if max is not None:
        x = np.array([i for i in range(0, max, steps)])

    df1 = to_dataframe('2021.06.30.09.59.25.csv')
    y1 = df1['action']
    y1 = y1[int(df1.shape[0]/2):].values

    df2 = to_dataframe('2021.06.30.10.31.57.csv')
    y2 = df2['action']
    y2 = y2[int(df2.shape[0]/2):].values

    df3 = to_dataframe('2021.06.30.10.57.09.csv')
    y3 = df3['action']
    y3 = y3[int(df3.shape[0]/2):].values

    df4 = to_dataframe('2021.06.30.11.16.43.csv')
    y4 = df4['action']
    y4 = y4[int(df4.shape[0]/2):].values

    df5 = to_dataframe('2021.06.30.11.37.02.csv')
    y5 = df5['action']
    y5 = y5[int(df5.shape[0]/2):].values

    df6 = to_dataframe('2021.07.05.22.02.53.csv')
    y6 = df6['action']
    y6 = y6[int(df6.shape[0]/2):].values

    df7 = to_dataframe('2021.07.05.22.49.26.csv')
    y7 = df7['action']
    y7 = y7[int(df7.shape[0]/2):].values

    df8 = to_dataframe('2021.07.05.23.57.15.csv')
    y8 = df8['action']
    y8 = y8[int(df8.shape[0]/2):].values

    df9 = to_dataframe('2021.07.06.18.04.37.csv')
    y9 = df9['action']
    y9 = y9[int(df9.shape[0]/2):].values

    df10 = to_dataframe('2021.07.06.19.13.35.csv')
    y10 = df10['action']
    y10 = y10[int(df10.shape[0]/2):].values

    df11 = to_dataframe('2021.07.06.19.39.02.csv')
    y11 = df11['action']
    y11 = y11[int(df11.shape[0]/2):].values

    if max is not None:
        y1 = y1[0:max]
        y2 = y2[0:max]
        y3 = y3[0:max]
        y4 = y4[0:max]
        y5 = y5[0:max]
        y6 = y6[0:max]
        y7 = y7[0:max]
        y8 = y8[0:max]
        y9 = y9[0:max]
        y10 = y10[0:max]
        y11 = y11[0:max]

    plt.figure(figsize=(20, 15))

    plot_matrix(x, y1, 'Bootstrapped Upper-Confidence Bound', 1)
    plot_matrix(x, y2,   'Bootstrapped Thompson Sampling', 2)
    plot_matrix(x, y3,   'Separate Classifiers + Beta Prior', 3)
    plot_matrix(x, y4,   'Epsilon-Greedy with decay', 4)
    plot_matrix(x, y5,   'Epsilon-Greedy without decay', 5)
    plot_matrix(x, y6,   'Adaptive Greedy with decaying threshold', 6)
    plot_matrix(x, y7,   'Adaptive Greedy with decaying percentile', 7)
    plot_matrix(x, y8,   'Explore First with 1,500 explore rounds', 8)
    plot_matrix(x, y9,   'Active Explorer', 9)
    plot_matrix(x, y10,   'Adaptive Active Greedy', 10)
    plot_matrix(x, y11,  'Softmax Explorer', 11)

    file_name = f'multi.arms.linear_policies.{max}.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots/arm', file_name)

    plt.tight_layout()
    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_arm_scatter(df: pd.DataFrame, title: str) -> None:

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    N = df.shape[0]
    x = df['step']
    y = df['action']
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

    plt.scatter(x, y,  c=colors)
    plt.xlabel('Step')
    plt.ylabel('Arm')
    plt.title(title)

    plot_file_name = f'{title.replace(" ", "_")}.scatter_arm.{datetime.now().strftime("%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_reward_evolution(df: pd.DataFrame, title: str) -> None:

    N = df.shape[0]
    x = [df['step'].values[i] for i in range(0, N, 100)]
    y = [df['reward_fl'].values[i] for i in range(0, N, 100)]

    _, ax = plt.subplots()

    ax.plot(x, y, 'r.')
    plt.xlabel('Step')
    plt.ylabel('Reward')
    plt.title(title)

    plot_file_name = f'{title.replace(" ", "_")}.linear_reward' + \
        datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")
    plot_file_name = os.path.join(entry_path, 'plots/reward', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_all_reward(csv_files: list, csv_file_names: list):

    _, ax = plt.subplots()

    for i in range(len(csv_files)):
        policy = csv_file_names[i]
        run_file = csv_files[i]
        csv_file = os.path.join(entry_path, 'log/mab/trace', run_file)

        columns = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
                   'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']
        df = pd.read_csv(csv_file, names=columns)

        N = df.shape[0]
        x = [i for i in range(0, int(N/2))]
        y = df['reward_fl'][int(N/2):].values

        ax.plot(x, y, '.', label=policy)

    plt.xlabel('Step')
    plt.ylabel('Reward')
    plt.title('Reward Evolution of all policies')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
               fancybox=True, ncol=3, prop={'size': 10})

    plot_file_name = f'all_reward {datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots/reward', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')


def plot_arm_bandwidth(bw_file: str, title: str, max: int = None):

    bws = to_bandwidth_array_v2(bw_file)

    N = len(bws)
    steps = 100
    x = np.array([i for i in range(steps, N, steps)])

    if max is not None:
        x = np.array([i for i in range(0, max_size)])

    y = np.array(get_average(bws, steps))

    if max is not None:
        y = bws[0:max_size]

    _, ax = plt.subplots()

    ax.plot(x, y, label='Bandwidth')

    plt.xlabel('Step')
    plt.ylabel('Bandwidth')
    plt.title(title)
    plt.legend()

    file_name = f'{title.replace(" ", "_")}.bandwidth.{datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")}'
    plot_file_name = os.path.join(entry_path, 'plots/bandwidth', file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def plot_arms_reward(df: pd.DataFrame, title: str):

    x0 = np.sum(df[df['action'] == 0]['reward'].values)
    x1 = np.sum(df[df['action'] == 1]['reward'].values)
    x2 = np.sum(df[df['action'] == 2]['reward'].values)
    x3 = np.sum(df[df['action'] == 3]['reward'].values)
    x = ['vegas', 'owl', 'cubic', 'hybla']
    y = np.array([x0, x1, x2, x3])

    _, ax = plt.subplots()

    ax.bar(x, y)
    plt.xlabel('Arm')
    plt.ylabel('Total reward obtained')
    plt.title(title)

    # ax.set_xticklabels

    for i, v in enumerate(y):
        ax.text(i - .15, v + 10, str(v), color='blue', fontweight='bold')

    plot_file_name = f'{title.replace(" ", "_")}.bar_arm_reward' + \
        datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")
    plot_file_name = os.path.join(entry_path, 'plots/reward', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)


def get_mean_reward(reward_lst, batch_size):
    mean_rew = list()
    for r in range(len(reward_lst)):
        mean_rew.append(sum(reward_lst[:r+1]) * 1.0 / ((r+1)*batch_size))
    return mean_rew


def prepare_error_ds(filename: str):

    df = to_dataframe(filename, None, None)
    x = [index for index in range(int(df.shape[0]/2))]
    y = get_mean_reward(df['reward'][int(df.shape[0]/2):].values, 1)

    hy = CI_model(y)

    return hy, x, y


def plot_error():

    plt.figure(figsize=(5, 15))

    _, ax = plt.subplots()

    h_y1, x1, y1 = prepare_error_ds('2021.06.30.09.59.25.csv')

    h_y2, x2, y2 = prepare_error_ds('2021.06.30.10.31.57.csv')

    h_y3, x3, y3 = prepare_error_ds('2021.06.30.10.57.09.csv')

    h_y4, x4, y4 = prepare_error_ds('2021.06.30.11.16.43.csv')

    h_y5, x5, y5 = prepare_error_ds('2021.06.30.11.37.02.csv')

    h_y6, x6, y6 = prepare_error_ds('2021.07.05.22.02.53.csv')

    h_y7, x7, y7 = prepare_error_ds('2021.07.05.22.49.26.csv')

    h_y8, x8, y8 = prepare_error_ds('2021.07.05.23.57.15.csv')

    h_y9, x9, y9 = prepare_error_ds('2021.07.06.18.04.37.csv')

    h_y10, x10, y10 = prepare_error_ds('2021.07.06.19.13.35.csv')

    h_y11, x11, y11 = prepare_error_ds('2021.07.06.19.39.02.csv')

    ax.errorbar(x1,    y1,     yerr=h_y1,
                label='Bootstrapped Upper-Confidence Bound')
    ax.errorbar(x2,    y2,     yerr=h_y2,
                label='Bootstrapped Thompson Sampling')
    ax.errorbar(x3,    y3,     yerr=h_y3,
                label='Separate Classifiers + Beta Prior')
    ax.errorbar(x4,    y4,     yerr=h_y4,  label='Epsilon-Greedy with decay')
    ax.errorbar(x5,    y5,     yerr=h_y5,
                label='Epsilon-Greedy without decay')
    ax.errorbar(x6,    y6,     yerr=h_y6,
                label='Adaptive Greedy with decaying threshold')
    ax.errorbar(x7,    y7,     yerr=h_y7,
                label='Adaptive Greedy with decaying percentile')
    ax.errorbar(x8,    y8,     yerr=h_y8,
                label='Explore First with 1,500 explore rounds')
    ax.errorbar(x9,    y9,     yerr=h_y9,  label='Active Explorer')
    ax.errorbar(x10,   y10,    yerr=h_y10, label='Adaptive Active Greedy')
    ax.errorbar(x11,   y11,    yerr=h_y11, label='Softmax Explorer')
    # plt.plot(np.repeat(y.mean(axis=0).max(),len(rewards_sft)),linewidth=4,ls='dashed', label='Overall Best Arm (no context)')

    plt.xlabel('Rounds', size=10)
    plt.ylabel('Cummulative Mean Reward', size=10)
    #plt.title('Comparison of Online Contextual Bandit Policies in location 7\n(Base Algorithm is Logistic Regression with data fit in streams)\n\nDataset\n(159 categories, 1836 attributes)',size=30)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 1.25])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              fancybox=True, ncol=3, prop={'size': 16})

    plot_file_name = 'all_policies' + datetime.now().strftime(".%Y.%m.%d.%H.%M.%S.png")
    plot_file_name = os.path.join(entry_path, 'plots/reward', plot_file_name)

    plt.savefig(plot_file_name, bbox_inches='tight', dpi=600)
    plt.close('all')
