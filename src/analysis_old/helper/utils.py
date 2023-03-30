import json
import os
import subprocess
import sys
import traceback
from types import SimpleNamespace
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np
import pandas as pd
import scipy.stats as st
from matplotlib.patches import Ellipse

src_path = os.path.dirname(os.getcwd())
ml_path = src_path + '/ml'
entry_path = src_path.replace("/src", "")
sys.path.insert(0, entry_path)

print(
    f'src_dir: {src_path} | base_dir: {ml_path} | entry_dir: {entry_path} \n\n')

owl_columns = ['action', 'action_value', 'cwnd', 'rtt', 'rtt_dev', 'delivered',
               'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward', 'model']
owl_path = 'log/owl/trace'

mtu = 1500
max_size = 100
noise = 1e-100
nb = 1e9
mb = 1e6
kb = 1e3
gb = 1e9
bit = 8

TIME_FORMAT = '%Y.%m.%d.%H.%M.%S'


def get_fullpath(file: str) -> str:

    try:

        path = subprocess.check_output(['locate', file])

        return path.strip().decode('utf-8')

    except Exception as _:
        print('\n')
        print(traceback.format_exc())


def get_throughput(cwnds: np.ndarray, rtts: np.ndarray) -> np.ndarray:
    return ((cwnds*bit) / rtts)/mb


def get_average(items: np.ndarray, step: int) -> list:
    """
        Calculates the mean step of values in array
        items: list of items
        step: step value
        result: returns a new list
    """

    _, N = items.reshape(1, -1).shape

    result = []

    lastIndex = 0

    for i in range(step, N+1, step):
        beg = i - step
        end = i
        lastIndex = end

        average = np.mean(items[beg:end])

        result.append(average)

    if N > lastIndex:
        result.append(np.mean(items[lastIndex:]))

    return result


def get_plot_xyz(df: pd.DataFrame, col: str, config, bws: list = []):

    N, _ = df.shape
    steps = config['step']
    max = config['max']

    y = []
    z = np.array([])

    if col is not None:
        if col == 'cwnd':
            y = (np.array(get_average(df[col].values, steps)) * mtu)
        else:
            y = np.array(get_average(df[col].values, steps))

    if max is not None:
        x = np.array([i for i in range(0, max)])

        if col is not None:
            y = y[0:max]

    if bws is not None and len(bws) > 0:
        temp = (np.array(bws))[0:N]
        z = np.array(get_average(temp, steps))

        if max is not None:
            z = temp[0:max]

    x = np.array([i for i in range(0, y.shape[0])])

    print(f'get_plot_xyz: x: ({x.shape}) | y: ({y.shape}) | z: ({z.shape})')
    return x, y, z


def get_iperf_xyz_all(protocol: str, trace: str, col: str, dir_path: str = None):

    print(f'\n\nLoad iperfs for: {protocol} | {trace}')

    dir_path = dir_path if not None else 'log/iperf/protocol'
    allow_zeros = True

    dir = os.path.join(entry_path, dir_path)
    files = sorted(os.listdir(dir))

    xall = []
    yall = []

    for file in files:

        if file.find(protocol) == -1 or file.find(trace) == -1:
            continue

        print(f'Processing: {file}')

        iperf_log = get_iperf_log(file)
        x, y = get_iperf_xyz(iperf_log, col, allow_zeros)

        xall += x.tolist()
        yall += y.tolist()

    return np.array(xall), np.array(yall)


def get_iperf_xyz_all_mean(protocol: str, trace: str, col: str, dir_path: str = None):

    print(f'\n\nLoad iperfs for: {protocol} | {trace}')

    dir_path = dir_path if not None else 'log/iperf/protocol'
    allow_zeros = True

    dir = os.path.join(entry_path, dir_path)
    files = sorted(os.listdir(dir))

    yall = []

    for file in files:

        if file.find(protocol) == -1 or file.find(trace) == -1:
            continue

        print(f'Processing: {file}')

        iperf_log = get_iperf_log(file)
        _, y = get_iperf_xyz(iperf_log, col, allow_zeros)

        yall += [np.mean(y.tolist())]

    xall = np.arange(1, len(yall) + 1)
    return xall, np.array(yall)


def get_iperf_xyz_last(protocol: str, trace: str, col: str, allow_zeros: bool = True):

    print(f'\n\nLoad iperfs for: {protocol} | {trace}')

    selectedFlag = 20
    flag = 1

    dir = os.path.join(entry_path, "log/iperf/protocol")
    files = sorted(os.listdir(dir))

    xall = []
    yall = []

    lastfile = None

    for file in files:

        if file.find(protocol) == -1 or file.find(trace) == -1:
            continue

        lastfile = file

        if flag == selectedFlag:
            break

        flag += 1

    print(f'Processing: {lastfile}')

    iperf_log = get_iperf_log(lastfile)
    x, y = get_iperf_xyz(iperf_log, col, allow_zeros)

    xall += x.tolist()
    yall += y.tolist()

    return np.array(xall), np.array(yall)


def iperf_dir_lastfile_tput_latency_mean(protocol: str, trace: str, dir_path: str):

    print(f'\n\nLoad iperfs for: {protocol} | {trace}')

    dir_path = dir_path if not None else 'log/iperf/protocol'

    dir = os.path.join(entry_path, dir_path)
    files = sorted(os.listdir(dir))

    lastfile = None

    for index, file in enumerate(files):

        if file.find(protocol) == -1 or file.find(trace) == -1:
            continue

        lastfile = file

        # if index == 10:
        #     break

    print(f'Processing: {lastfile}')

    iperf_log = get_iperf_log(lastfile)
    x = iperf_log.end.streams[0].sender.mean_rtt
    y = iperf_log.end.sum_sent.bits_per_second

    return x, y


def get_iperf_xyz(log: object, col: str, allow_zeros: bool = True):

    y = []
    last_tput = 0

    for item in log.intervals:

        if col == 'cwnd':
            y.append(item.streams[0].snd_cwnd)

        elif col == 'rtt':
            y.append(item.streams[0].rtt)

        elif col == 'throughput':
            tput = item.streams[0].bits_per_second

            if not allow_zeros:
                tput = last_tput if tput == 0 else tput

            y.append(tput)
            last_tput = tput

    y = np.array(y)

    x = np.arange(1, y.shape[0]+1)

    return np.array(x), y


def get_iperf_log(filename: str) -> dict:

    path = get_fullpath(filename)

    print(f'Loading: {path} -> JSON object')

    with open(path) as file:
        config = json.load(file, object_hook=lambda d: SimpleNamespace(**d))

    return config


def from_iperf(filename: str, col: str, allow_zeros: bool = True):

    log = get_iperf_log(filename)

    return get_iperf_xyz(log, col, allow_zeros)


def get_pantheon_all_xyz(path: str) -> Any:

    with open(path) as file:
        config: dict = json.load(file)

    keys = config.keys()

    delay_list = []
    tput_list = []
    z = []

    tp_df = pd.DataFrame()
    delay_df = pd.DataFrame()

    for key in keys:
        protocol = config[key]

        if not "1" in protocol:
            # if not "1" in protocol or key == 'pcc_experimental':
            # if not "1" in protocol or key == 'pcc_experimental' or key == 'pcc' or key == 'vivace' or key == 'cubic':
            continue

        runs = protocol.keys()
        print(f'Processing: {key}')

        for run in runs:

            tput = protocol[run]["all"]["tput"]
            delay = protocol[run]["all"]["delay"]

            tput_list.append(tput)
            delay_list.append(delay)

        key = key.replace('_', '\_')
        delay_df[key] = delay_list
        tp_df[key] = tput_list
        delay_list = []
        tput_list = []
        z.append(key)

    return delay_df, tp_df, np.array(z)


def get_pantheon_xyz(path: str, exclude: list = []) -> Any:

    with open(path) as file:
        config: dict = json.load(file)

    keys = config.keys()

    x = []
    y = []
    z = []

    for key in keys:
        data = config[key]

        if not "1" in data or key in exclude:
            # if not "1" in data or key == 'pcc_experimental':
            # if not "1" in data or key == 'indigo' or key == 'webrtc' or key == 'scream' or key == 'sprout' or key == 'ledbat' or key == 'fillp_sheep' or key == 'vivace' or key == 'pcc':
            continue

        tp = data["1"]["all"]["tput"]
        latency = data["1"]["all"]["delay"]

        title = key.replace('_', '\_')
        x.append(round(latency, 4))
        y.append(round(tp, 4))
        z.append(title)

    return np.array(x), np.array(y), np.array(z)


def to_dataframe(result_file: str, colns: list = None, path: str = None) -> pd.DataFrame:

    if colns is None:
        colns = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff',
                 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward_fl', 'reward']

    if path is None:
        path = 'log/mab/trace'

    protocol_labels = {
        0: 'cubic',
        1: 'hybla',
        2: 'vegas',
    }

    path = get_fullpath(result_file)

    df = pd.read_csv(path, names=colns)
    df['rtt'] = df['rtt']/nb
    df['throughput'] = get_throughput(df['cwnd'].values, df['rtt'].values)
    df['protocol'] = np.array([protocol_labels[i] for i in df['action']])

    print(f'file: {result_file} | shape: {df.shape}')

    return df


def to_dataframe_prod(result_file: str, colns: list = None, path: str = None) -> pd.DataFrame:

    tf = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff',
          'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward', 'model', 'timestamp']

    if colns is None:
        colns = ['action', 'cwnd', 'rtt', 'rtt_dev', 'delivered', 'delivered_diff',
                 'lost', 'in_flight', 'retrans', 'cwnd_diff', 'step', 'reward', 'model']

    protocol_labels = {
        0: 'cubic',
        1: 'hybla',
        2: 'owl',
        3: 'vegas'
    }

    path = get_fullpath(result_file)
    df: pd.DataFrame = pd.read_csv(path)

    if df.shape[1] == len(colns):
        df.columns = colns

    if df.shape[1] == len(tf):
        df.columns = tf

    df['rtt'] = df['rtt']/nb
    df['throughput'] = get_throughput(df['cwnd'].values, df['rtt'].values)
    df['protocol'] = np.array([protocol_labels[i] for i in df['action']])

    print(f'file: {result_file} | shape: {df.shape}')

    return df


def to_bandwidth_array(file: str) -> np.ndarray:
    """
        Get bandwidth data frame
        file: Name of the file where the bandwidth values are stored
    """

    bws = []

    path = os.path.join(entry_path, 'traces', file)

    with open(path, 'rt') as f:
        while True:
            line = f.readline()

            if not line:
                break

            if "1504" in line and "#" in line:
                items = line.strip().split('#')
                bws.append(int(items[0]))

    # _, indices = np.unique(bws, return_index=True)

    # final_bws = [bws[i] for i in indices]

    # return np.array(final_bws)
    return np.array(bws)


def to_bandwidth_array_v2(file: str) -> np.ndarray:
    """
        Get bandwidth values \n
        Input:
        \t file: \t Name of the file where the bandwidth values are stored
        Returns: \t An np array containing the bandwidth values
    """

    bws = []
    mtu = 1500
    traces = []

    path = os.path.join(entry_path, 'traces', file)

    with open(path, 'rt') as f:
        traces = [int(i) for i in f]

    mtu_count = 0
    last_time_ms = -1

    for time_ms in traces:

        if last_time_ms == -1:
            last_time_ms = time_ms

        if last_time_ms != time_ms:
            interval_ms = time_ms - last_time_ms
            bw = (mtu_count * mtu * bit)/(interval_ms/1000)
            bws.append(bw)

            # reset
            mtu_count = 0
            last_time_ms = time_ms

        mtu_count += 1

    return np.array(bws)


def mape(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """
        Mean absolute percentage error
    """

    return round((np.absolute(predictions - actuals) / actuals).mean(), 4)


def plot_matrix(x: np.ndarray, y: np.ndarray, label: str, position: int) -> None:

    ax = plt.subplot(4, 3, position)
    ax.plot(x, y, '.')
    ax.set_ylabel('Congestion Protocols Chosen')
    ax.set_xlabel('Step')
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['vegas', 'owl', 'cubic', 'hybla'])
    plt.title(label)

    return ax


def CI_model(y, confidence=0.9):
    std_err_y = st.sem(y)
    n_y = len(y)
    h_y = std_err_y * st.t.ppf((1 + confidence) / 2, n_y - 1)
    return h_y


def get_mean_reward(reward_lst, batch_size):
    mean_rew = list()
    for r in range(len(reward_lst)):
        mean_rew.append(sum(reward_lst[:r+1]) * 1.0 / ((r+1)*batch_size))
    return mean_rew


def prepare_error_ds_prod(filename: str):

    df = to_dataframe_prod(filename)
    x = np.arange(df.shape[0])
    y = get_mean_reward(df['reward'].values, 1)

    hy = CI_model(y)

    return hy, x, y


def bold(txt: str) -> str:
    return txt  # '\\textbf{' + f'{txt}' + '}'


def bold_ls(ls: list) -> list:

    result = list()

    for item in ls:
        result.append(bold(item))

    return result


def to_latex_txt(txt: str) -> str:
    return txt.replace('_', '\_')


def abbreviate(txt: str) -> str:
    pts = txt.strip().split('_')
    res = ""

    for i in pts:
        res += i[0]

    return res


def abbreviate_ls(ls: list) -> list:

    res = list()

    for i in ls:
        res.append(abbreviate(i))

    return res


def check_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def change_file_name(old_name: str, new_name: str) -> None:
    try:
        os.rename(old_name, new_name)
    except Exception as _:
        print('\n')
        print(traceback.print_exc())


def print_cmd(cmd):
    if isinstance(cmd, list):
        cmd_to_print = ' '.join(cmd).strip()
    elif isinstance(cmd, str):
        cmd_to_print = cmd.strip()
    else:
        cmd_to_print = ''

    if cmd_to_print:
        sys.stderr.write('\n$ %s\n\n' % cmd_to_print)


def check_output(cmd, **kwargs):
    print_cmd(cmd)
    return subprocess.check_output(cmd, **kwargs)


def harm_tput(x, y) -> float:
    return round((x-y)/x, 4)


def harm_delay(x, y) -> float:
    return round((y-x)/y, 4)


def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
