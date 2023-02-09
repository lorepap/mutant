import os
from helper import utils


def get_verizon_exp() -> dict:
    experiment = {}

    # experiment = {
    #     'cubic': 'cubic.2021.07.26.00.59.01.csv',
    #     'hybla': 'hybla.2021.07.27.23.14.10.csv',
    #     'vegas': 'vegas.2021.07.27.01.13.53.csv',
    #     'owl':   'owl.2021.08.04.09.45.09.csv',
    #     'mab':   'mab.AdaptiveGreedy.2021.08.25.02.25.56.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'step': 10,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.30.2021.08.30.22.20.16.csv',
    #     'hybla': 'verizon/hybla.30.2021.08.30.23.07.40.csv',
    #     'vegas': 'verizon/vegas.30.2021.08.30.21.41.50.csv',
    #     'mab':   'verizon/mab.30.2021.08.30.23.47.36.csv',
    #     'owl':   'verizon/owl.30.2021.08.31.23.24.47.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '30.verizon',
    #     'step': 10,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.60.2021.08.30.22.22.19.csv',
    #     'hybla': 'verizon/hybla.60.2021.08.30.23.12.55.csv',
    #     'vegas': 'verizon/vegas.60.2021.08.30.21.44.07.csv',
    #     'mab':   'verizon/mab.60.2021.08.30.23.49.24.csv',
    #     'owl':   'verizon/owl.60.2021.08.31.23.32.00.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '60.verizon',
    #     'step': 10,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'mab':   'verizon/mab.300.2021.08.30.23.54.11.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '300.verizon',
    #     'step': 50,
    #     'max': None
    # }

    experiment = {
        'cubic': 'verizon/cubic.600.2021.08.30.22.48.55.csv',
        'hybla': 'verizon/hybla.600.2021.08.30.23.38.22.csv',
        'vegas': 'verizon/vegas.600.2021.08.30.22.14.03.csv',
        'mab':   'verizon/mab.600.2021.08.31.00.05.01.csv',
        'owl':   'verizon/owl.600.2021.09.01.00.22.39.csv',
        'bw': 'Verizon-LTE-short.up',
        'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
        'training': 'train: \t 5 episodes (1000 steps per episode)',
        'testing': 'test: \t 5 episodes (1000 steps per episode)',
        'trace': '600.verizon',
        'step': 100,
        'max': None
    }

    return experiment


def get_tmobile_exp() -> dict:
    experiment = {}

    # experiment = {
    #     'cubic': 'tmobile/cubic.30.2021.09.14.11.42.58.csv',
    #     'hybla': 'tmobile/hybla.30.2021.09.14.13.22.42.csv',
    #     'vegas': 'tmobile/vegas.30.2021.09.01.01.52.57.csv',
    #     'mab':   'tmobile/mab.30.2021.09.01.01.00.26.csv',
    #     'owl':   'tmobile/owl.30.2021.09.01.00.27.27.csv',
    #     'bw': 'TMobile-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '30.tmobile',
    #     'step': 10,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'tmobile/cubic.60.2021.09.14.11.45.51.csv',
    #     'hybla': 'tmobile/hybla.60.2021.09.14.13.25.10.csv',
    #     'vegas': 'tmobile/vegas.60.2021.09.01.01.55.59.csv',
    #     'mab':   'tmobile/mab.60.2021.09.01.01.02.16.csv',
    #     'owl':   'tmobile/owl.60.2021.09.01.00.28.28.csv',
    #     'bw': 'TMobile-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '60.tmobile',
    #     'step': 20,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'tmobile/cubic.300.2021.09.14.12.00.04.csv',
    #     'hybla': 'tmobile/hybla.300.2021.09.14.13.53.20.csv',
    #     'vegas': 'tmobile/vegas.300.2021.09.01.02.00.48.csv',
    #     'mab':   'tmobile/mab.300.2021.09.01.01.05.36.csv',
    #     'owl':   'tmobile/owl.300.2021.09.01.00.34.06.csv',
    #     'bw': 'TMobile-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '300.tmobile',
    #     'step': 50,
    #     'max': None
    # }

    experiment = {
        'cubic': 'tmobile/cubic.600.2021.09.14.12.25.08.csv',
        'hybla': 'tmobile/hybla.600.2021.09.14.14.11.29.csv',
        'vegas': 'tmobile/vegas.600.2021.09.01.02.12.12.csv',
        'mab':   'tmobile/mab.600.2021.09.01.01.27.07.csv',
        'owl':   'tmobile/owl.600.2021.09.01.00.46.42.csv',
        'bw': 'TMobile-LTE-short.up',
        'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
        'training': 'train: \t 5 episodes (1000 steps per episode)',
        'testing': 'test: \t 5 episodes (1000 steps per episode)',
        'trace': '600.tmobile',
        'step': 100,
        'max': None
    }

    return experiment


def get_wifi_exp() -> dict:
    experiment = {}

    # experiment = {
    #     'cubic': 'wifi/cubic.30.2021.09.14.12.30.50.csv',
    #     'hybla': 'wifi/hybla.30.2021.09.14.14.55.57.csv',
    #     'vegas': 'wifi/vegas.30.2021.09.14.20.43.30.csv',
    #     'mab':   'wifi/mab.30.2021.09.14.22.04.48.csv',
    #     'owl':   'wifi/owl.30.2021.09.14.17.23.43.csv',
    #     'bw': None,
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '30.wifi',
    #     'step': 50,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'wifi/cubic.60.2021.09.14.12.32.22.csv',
    #     'hybla': 'wifi/hybla.60.2021.09.14.14.56.52.csv',
    #     'vegas': 'wifi/vegas.60.2021.09.14.20.44.38.csv',
    #     'mab':   'wifi/mab.60.2021.09.14.22.09.14.csv',
    #     'owl':   'wifi/owl.60.2021.09.14.17.26.36.csv',
    #     'bw': None,
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '60.wifi',
    #     'step': 100,
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'wifi/cubic.300.2021.09.14.12.38.46.csv',
    #     'hybla': 'wifi/hybla.300.2021.09.14.15.05.01.csv',
    #     'vegas': 'wifi/vegas.300.2021.09.14.21.12.14.csv',
    #     'mab':   'wifi/mab.300.2021.09.14.22.14.50.csv',
    #     'owl':   'wifi/owl.300.2021.09.14.17.41.07.csv',
    #     'bw': None,
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': '300.wifi',
    #     'step': 100,
    #     'max': None
    # }

    experiment = {
        'cubic': 'wifi/cubic.600.2021.09.14.12.52.17.csv',
        'hybla': 'wifi/hybla.600.2021.09.14.15.56.22.csv',
        'vegas': 'wifi/vegas.600.2021.09.14.21.22.45.csv',
        'mab':   'wifi/mab.600.2021.09.14.22.25.55.csv',
        'owl':   'wifi/owl.600.2021.09.14.18.28.55.csv',
        'bw': None,
        'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
        'training': 'train: \t 5 episodes (1000 steps per episode)',
        'testing': 'test: \t 5 episodes (1000 steps per episode)',
        'trace': '600.wifi',
        'step': 200,
        'max': None
    }

    return experiment


def get_less_loss_exp() -> dict:
    experiment = None

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'mab':   'AdaptiveGreedyWithPercentile.2021.09.20.18.45.06.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': 'verizon',
    #     'step': 100,
    #     'info': 'Mab experiment where delta was decreased to 0.01',
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'mab':   'AdaptiveGreedyWithPercentile.2021.09.21.17.56.00.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': 'verizon',
    #     'step': 100,
    #     'info': 'Mab experiment where the jiffy was increased to 5 and history was not used in training',
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'mab':   'AdaptiveGreedyWithPercentile.2021.09.27.21.27.24.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': 'verizon',
    #     'step': 100,
    #     'info': 'Mab experiment where the jiffy was increased to 5 and history was used in training',
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'mab':   'AdaptiveGreedyWithPercentile.2021.10.03.14.42.25.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': 'verizon',
    #     'step': 100,
    #     'info': 'Mab experiment where samples were collected every 5 seconds',
    #     'max': None
    # }

    # experiment = {
    #     'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
    #     'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
    #     'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
    #     'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
    #     'mab':   'AdaptiveGreedyWithPercentile.2021.10.18.20.48.51.csv',
    #     'bw': 'Verizon-LTE-short.up',
    #     'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
    #     'training': 'train: \t 5 episodes (1000 steps per episode)',
    #     'testing': 'test: \t 5 episodes (1000 steps per episode)',
    #     'trace': 'verizon',
    #     'step': 100,
    #     'info': 'Mab experiment where delta was increased to 1.0',
    #     'max': None
    # }

    experiment = {
        'cubic': 'verizon/cubic.300.2021.08.30.22.27.43.csv',
        'hybla': 'verizon/hybla.300.2021.08.30.23.26.40.csv',
        'vegas': 'verizon/vegas.300.2021.08.30.22.02.55.csv',
        'owl':   'verizon/owl.300.2021.08.31.23.50.07.csv',
        'mab':   'AdaptiveGreedyWithPercentile.2021.10.20.12.13.12.csv',
        'bw': 'Verizon-LTE-short.up',
        'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
        'training': 'train: \t 5 episodes (1000 steps per episode)',
        'testing': 'test: \t 5 episodes (1000 steps per episode)',
        'trace': 'verizon',
        'step': 100,
        'info': 'Mab experiment where delta was increased to 1.0',
        'max': None
    }

    return experiment


def get_mininet_exp() -> dict:
    experiment = {
        'cubic': 'cubic.2021.10.21.12.57.47.csv',
        'hybla': 'hybla.2021.10.24.00.58.25.csv',
        'vegas': 'vegas.2021.10.24.15.33.01.csv',
        'owl':   'owl.2021.10.25.00.21.41.csv',
        'mab':   'AdaptiveGreedyWithPercentile.2021.10.20.12.13.12.csv',
        'bw': 'Verizon-LTE-short.up',
        'mab_policy': 'mab_policy: \t Adaptive Greedy with weighted percentile',
        'training': 'train: \t 10 episodes (1000 steps per episode)',
        'testing': 'test: \t 1 episode (1000 steps per episode)',
        'trace': 'mn',
        'step': 100,
        'info': 'Mab experiments with all arms using mininet',
        'max': None
    }

    return experiment


def get_policy_exp(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':

        return {
            'active_explorer': 'att.lte.driving.active_explorer.2022.03.17.23.34.24.csv',
            'active_greedy_percentile': 'att.lte.driving.adaptive_greedy_percentile.2022.03.17.23.34.24.csv',
            'active_greedy_threshold': 'att.lte.driving.adaptive_greedy_threshold.2022.03.17.23.34.24.csv',
            'active_greedy_weighted': 'att.lte.driving.adaptive_greedy_weighted.2022.03.17.23.34.24.csv',
            'bootstrapped_ts': 'att.lte.driving.bootstrapped_ts.2022.03.17.23.34.24.csv',
            'bootstrapped_ucb': 'att.lte.driving.bootstrapped_ucb.2022.03.17.23.34.24.csv',
            'epsilon_greedy_decay': 'att.lte.driving.epsilon_greedy_decay.2022.03.17.23.34.24.csv',
            'epsilon_greedy': 'att.lte.driving.epsilon_greedy.2022.03.17.23.34.24.csv',
            'explore_first': 'att.lte.driving.explore_first.2022.03.17.23.34.24.csv',
            'separate_classifiers': 'att.lte.driving.separate_classifiers.2022.03.17.23.34.24.csv',
            'softmax_explorer': 'att.lte.driving.softmax_explorer.2022.03.17.23.34.24.csv',
            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving',
            'step': 10,
        }

    if trace == 'tm.lte.short':
        return {
            'active_explorer': 'tm.lte.short.active_explorer.2022.03.18.00.42.14.csv',
            'active_greedy_percentile': 'tm.lte.short.adaptive_greedy_percentile.2022.05.12.12.42.05.csv',
            'active_greedy_threshold': 'tm.lte.short.adaptive_greedy_threshold.2022.03.18.00.42.14.csv',
            'active_greedy_weighted': 'tm.lte.short.adaptive_greedy_weighted.2022.05.12.12.42.05.csv',
            'bootstrapped_ts': 'tm.lte.short.bootstrapped_ts.2022.03.18.00.42.14.csv',
            'bootstrapped_ucb': 'tm.lte.short.bootstrapped_ucb.2022.03.18.00.42.14.csv',
            'epsilon_greedy_decay': 'tm.lte.short.epsilon_greedy_decay.2022.03.18.00.42.14.csv',
            'epsilon_greedy': 'tm.lte.short.epsilon_greedy.2022.03.18.00.42.14.csv',
            'explore_first': 'tm.lte.short.explore_first.2022.03.18.00.42.14.csv',
            'separate_classifiers': 'tm.lte.short.separate_classifiers.2022.05.12.12.42.06.csv',
            'softmax_explorer': 'tm.lte.short.softmax_explorer.2022.05.12.12.42.06.csv',
            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short',
            'step': 10,
        }

    return {
        'active_explorer': 'vz.lte.short.active_explorer.2022.03.18.02.01.07.csv',
        'active_greedy_percentile': 'vz.lte.short.adaptive_greedy_percentile.2022.03.18.02.01.07.csv',
        'active_greedy_threshold': 'vz.lte.short.adaptive_greedy_threshold.2022.03.18.12.35.24.csv',
        'active_greedy_weighted': 'vz.lte.short.adaptive_greedy_weighted.2022.03.18.12.35.24.csv',
        'bootstrapped_ts': 'vz.lte.short.bootstrapped_ts.2022.03.18.12.35.24.csv',
        'bootstrapped_ucb': 'vz.lte.short.bootstrapped_ucb.2022.03.18.12.35.24.csv',
        'epsilon_greedy_decay': 'vz.lte.short.epsilon_greedy_decay.2022.03.18.12.35.24.csv',
        'epsilon_greedy': 'vz.lte.short.epsilon_greedy.2022.03.18.02.01.07.csv',
        'explore_first': 'vz.lte.short.explore_first.2022.03.18.12.35.24.csv',
        'separate_classifiers': 'vz.lte.short.separate_classifiers.2022.03.18.12.35.24.csv',
        'softmax_explorer': 'vz.lte.short.softmax_explorer.2022.03.18.14.55.50.csv',
        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short',
        'step': 10,
    }



def get_prod_exp(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':
        return {
            'mimic': 'att.lte.driving.2022.02.22.16.39.38.csv',
            'cubic': 'att.lte.driving.cubic.2022.02.22.16.55.51.csv',
            'hybla': 'att.lte.driving.hybla.2022.02.22.17.21.39.csv',
            'vegas': 'att.lte.driving.vegas.2022.02.22.17.09.03.csv',
            'owl': 'att.lte.driving.owl.2022.02.22.17.45.27.csv',
            'basic': 'bs.att.lte.driving.2022.02.24.19.09.15.csv',

            'mimic_iperf': 'att.lte.driving.2022.02.22.16.39.38.json',
            'cubic_iperf': 'att.lte.driving.cubic.2022.02.22.16.55.51.json',
            'hybla_iperf': 'att.lte.driving.hybla.2022.02.22.17.21.39.json',
            'vegas_iperf': 'att.lte.driving.vegas.2022.02.22.17.09.03.json',
            'owl_iperf': 'att.lte.driving.owl.2022.02.22.17.45.27.json',
            'basic_iperf': 'bs.att.lte.driving.2022.02.24.19.09.15.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/att.lte.driving/v1/pantheon_perf.v1.json'),

            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'att.lte.driving.2016':
        return {
            'mimic': 'prod_trace.2022.01.31.22.12.40.csv',
            'cubic': 'cubic.2022.01.31.12.30.55.csv',
            'hybla': 'hybla.2022.01.31.21.42.59.csv',
            'vegas': 'vegas.2022.01.31.12.11.22.csv',
            'owl': 'owl.2022.01.31.12.56.40.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/att.lte.driving.2016/v1/pantheon_perf.v1.json'),

            'bw': 'ATT-LTE-driving-2016.up',
            'trace': 'att.lte.driving.2016',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'tm.umts.driving':
        return {
            'mimic': 'prod_trace.2022.02.01.13.53.49.csv',
            'cubic': 'cubic.2022.02.01.13.07.40.csv',
            'hybla': 'hybla.2022.02.01.12.41.54.csv',
            'vegas': 'vegas.2022.02.01.13.27.35.csv',
            'owl': 'owl.2022.02.01.12.22.45.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/tm.umts.driving/v1/pantheon_perf.v1.json'),

            'bw': 'TMobile-UMTS-driving.up',
            'trace': 'tm.umts.driving',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'tm.lte.short':
        return {
            'mimic': 'tm.lte.short.2022.02.22.18.46.06.csv',
            'cubic': 'tm.lte.short.cubic.2022.02.22.18.34.31.csv',
            'hybla': 'tm.lte.short.hybla.2022.02.22.18.12.00.csv',
            'vegas': 'tm.lte.short.vegas.2022.02.22.18.23.06.csv',
            'owl': 'tm.lte.short.owl.2022.02.22.18.00.41.csv',
            'basic': 'bs.tm.lte.short.2022.02.24.20.00.24.csv',

            'mimic_iperf': 'tm.lte.short.2022.02.22.18.46.06.json',
            'cubic_iperf': 'tm.lte.short.cubic.2022.02.22.18.34.31.json',
            'hybla_iperf': 'tm.lte.short.hybla.2022.02.22.18.12.00.json',
            'vegas_iperf': 'tm.lte.short.vegas.2022.02.22.18.23.06.json',
            'owl_iperf': 'tm.lte.short.owl.2022.02.22.18.00.41.json',
            'basic_iperf': 'bs.tm.lte.short.2022.02.24.20.00.24.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/tm.lte.short/v1/pantheon_perf.v1.json'),

            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'vz.evdo.driving':
        return {
            'mimic': 'prod_trace.2022.02.01.03.13.28.csv',
            'cubic': 'cubic.2022.02.01.01.41.03.csv',
            'hybla': 'hybla.2022.02.01.02.49.25.csv',
            'vegas': 'vegas.2022.02.01.02.01.32.csv',
            'owl': 'owl.2022.02.01.02.28.11.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.evdo.driving/v1/pantheon_perf.v1.json'),

            'bw': 'Verizon-EVDO-driving.up',
            'trace': 'vz.evdo.driving',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'vz.lte.driving':
        return {
            'mimic': 'prod_trace.2022.01.31.22.46.26.csv',
            'mimic': 'prod_trace.2022.01.31.22.46.26.csv',
            'cubic': 'cubic.2022.02.01.00.53.11.csv',
            'hybla': 'hybla.2022.01.31.23.14.32.csv',
            'vegas': 'vegas.2022.02.01.01.11.22.csv',
            'owl': 'owl.2022.01.31.23.36.34.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.lte.driving/v1/pantheon_perf.v1.json'),

            'bw': 'Verizon-LTE-driving.up',
            'trace': 'vz.lte.driving',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    return {
        'mimic': 'vz.lte.short.2022.02.22.18.57.31.csv',
        'cubic': 'vz.lte.short.cubic.2022.02.22.19.09.14.csv',
        'hybla': 'vz.lte.short.hybla.2022.02.22.19.33.19.csv',
        'vegas': 'vz.lte.short.vegas.2022.02.22.19.20.36.csv',
        'owl': 'vz.lte.short.owl.2022.02.22.19.45.52.csv',
        'basic': 'bs.vz.lte.short.2022.02.24.20.26.48.csv',

        'mimic_iperf': 'vz.lte.short.2022.02.22.18.57.31.json',
        'cubic_iperf': 'vz.lte.short.cubic.2022.02.22.19.09.14.json',
        'hybla_iperf': 'vz.lte.short.hybla.2022.02.22.19.33.19.json',
        'vegas_iperf': 'vz.lte.short.vegas.2022.02.22.19.20.36.json',
        'owl_iperf': 'vz.lte.short.owl.2022.02.22.19.45.52.json',
        'basic_iperf': 'bs.vz.lte.short.2022.02.24.20.26.48.json',

        'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.lte.short/v1/pantheon_perf.v1.json'),

        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short',
        'step': 10,
        'info': 'Mimic experiment with verizon lte short up for 1000 steps',
        'max': None
    }


def get_prod_exp_verbose(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':
        return {
            'mimic': 'att.lte.driving.verbose.2022.02.22.16.39.38.csv',
            'cubic': 'att.lte.driving.verbose.cubic.2022.02.22.16.55.51.csv',
            'hybla': 'att.lte.driving.verbose.hybla.2022.02.22.17.21.39.csv',
            'vegas': 'att.lte.driving.verbose.vegas.2022.02.22.17.09.03.csv',
            'owl': 'att.lte.driving.verbose.owl.2022.02.22.17.45.27.csv',
            'basic': 'bs.att.lte.driving.verbose.2022.02.24.19.09.15.csv',

            'mimic_iperf': 'att.lte.driving.2022.02.22.16.39.38.json',
            'cubic_iperf': 'att.lte.driving.cubic.2022.02.22.16.55.51.json',
            'hybla_iperf': 'att.lte.driving.hybla.2022.02.22.17.21.39.json',
            'vegas_iperf': 'att.lte.driving.vegas.2022.02.22.17.09.03.json',
            'owl_iperf': 'att.lte.driving.owl.2022.02.22.17.45.27.json',
            'basic_iperf': 'bs.att.lte.driving.2022.02.24.19.09.15.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/att.lte.driving/v1/pantheon_perf.v1.json'),

            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'att.lte.driving.2016':
        return {
            'mimic': 'att.lte.driving.2016.verbose.2022.02.18.11.36.53.csv',
            'cubic': 'cubic.2022.01.31.12.30.55.csv',
            'hybla': 'hybla.2022.01.31.21.42.59.csv',
            'vegas': 'vegas.2022.01.31.12.11.22.csv',
            'owl': 'owl.2022.01.31.12.56.40.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/att.lte.driving.2016/v1/pantheon_perf.v1.json'),

            'bw': 'ATT-LTE-driving-2016.up',
            'trace': 'att.lte.driving.2016.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'tm.umts.driving':
        return {
            'mimic': 'prod_trace.2022.02.01.13.53.49.csv',
            'cubic': 'cubic.2022.02.01.13.07.40.csv',
            'hybla': 'hybla.2022.02.01.12.41.54.csv',
            'vegas': 'vegas.2022.02.01.13.27.35.csv',
            'owl': 'owl.2022.02.01.12.22.45.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/tm.umts.driving/v1/pantheon_perf.v1.json'),

            'bw': 'TMobile-UMTS-driving.up',
            'trace': 'tm.umts.driving.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'tm.lte.short':
        return {
            'mimic': 'tm.lte.short.verbose.2022.02.22.18.46.06.csv',
            'cubic': 'tm.lte.short.verbose.cubic.2022.02.22.18.34.31.csv',
            'hybla': 'tm.lte.short.verbose.hybla.2022.02.22.18.12.00.csv',
            'vegas': 'tm.lte.short.verbose.vegas.2022.02.22.18.23.06.csv',
            'owl': 'tm.lte.short.verbose.owl.2022.02.22.18.00.41.csv',
            'basic': 'bs.tm.lte.short.verbose.2022.02.24.20.00.24.csv',

            'mimic_iperf': 'tm.lte.short.2022.02.22.18.46.06.json',
            'cubic_iperf': 'tm.lte.short.cubic.2022.02.22.18.34.31.json',
            'hybla_iperf': 'tm.lte.short.hybla.2022.02.22.18.12.00.json',
            'vegas_iperf': 'tm.lte.short.vegas.2022.02.22.18.23.06.json',
            'owl_iperf': 'tm.lte.short.owl.2022.02.22.18.00.41.json',
            'basic_iperf': 'bs.tm.lte.short.2022.02.24.20.00.24.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/tm.lte.short/v1/pantheon_perf.v1.json'),

            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'vz.evdo.driving':
        return {
            'mimic': 'prod_trace.2022.02.01.03.13.28.csv',
            'cubic': 'cubic.2022.02.01.01.41.03.csv',
            'hybla': 'hybla.2022.02.01.02.49.25.csv',
            'vegas': 'vegas.2022.02.01.02.01.32.csv',
            'owl': 'owl.2022.02.01.02.28.11.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.evdo.driving/v1/pantheon_perf.v1.json'),

            'bw': 'Verizon-EVDO-driving.up',
            'trace': 'vz.evdo.driving.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    if trace == 'vz.lte.driving':
        return {
            # 'mimic': 'prod_trace.2022.01.31.22.46.26.csv',
            'mimic': 'prod_trace.2022.01.31.22.46.26.csv',
            'cubic': 'cubic.2022.02.01.00.53.11.csv',
            'hybla': 'hybla.2022.01.31.23.14.32.csv',
            'vegas': 'vegas.2022.02.01.01.11.22.csv',
            'owl': 'owl.2022.01.31.23.36.34.csv',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.lte.driving/v1/pantheon_perf.v1.json'),

            'bw': 'Verizon-LTE-driving.up',
            'trace': 'vz.lte.driving.vb',
            'step': 10,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': None
        }

    return {
        'mimic': 'vz.lte.short.verbose.2022.02.22.18.57.31.csv',
        'cubic': 'vz.lte.short.verbose.cubic.2022.02.22.19.09.14.csv',
        'hybla': 'vz.lte.short.verbose.hybla.2022.02.22.19.33.19.csv',
        'vegas': 'vz.lte.short.verbose.vegas.2022.02.22.19.20.36.csv',
        'owl': 'vz.lte.short.verbose.owl.2022.02.22.19.45.52.csv',
        'basic': 'bs.vz.lte.short.verbose.2022.02.24.20.26.48.csv',

        'mimic_iperf': 'vz.lte.short.2022.02.22.18.57.31.json',
        'cubic_iperf': 'vz.lte.short.cubic.2022.02.22.19.09.14.json',
        'hybla_iperf': 'vz.lte.short.hybla.2022.02.22.19.33.19.json',
        'vegas_iperf': 'vz.lte.short.vegas.2022.02.22.19.20.36.json',
        'owl_iperf': 'vz.lte.short.owl.2022.02.22.19.45.52.json',
        'basic_iperf': 'bs.vz.lte.short.2022.02.24.20.26.48.json',

        'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.lte.short/v1/pantheon_perf.v1.json'),

        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short.vb',
        'step': 10,
        'info': 'Mimic experiment with verizon lte short up for 1000 steps',
        'max': None
    }


def get_orca(trace: str = 'bus') -> dict:

    if trace == 'bus':
        return {
            'mimic': 'bus.mimic.2022.04.05.13.59.14.csv',
            'cubic': 'bus.cubic.2022.04.05.15.04.47.csv',
            'hybla': 'bus.hybla.2022.04.05.15.05.50.csv',
            'owl': 'bus.owl.2022.04.05.15.06.53.csv',
            'vegas': 'bus.vegas.2022.04.05.15.07.55.csv',
            'basic': 'bus.bs.2022.04.05.14.20.09.csv',

            'mimic_iperf': 'bus.mimic.2022.04.05.13.59.14.json',
            'cubic_iperf': 'bus.cubic.2022.04.05.15.04.47.json',
            'hybla_iperf': 'bus.hybla.2022.04.05.15.05.50.json',
            'owl_iperf': 'bus.owl.2022.04.05.15.06.53.json',
            'vegas_iperf': 'bus.vegas.2022.04.05.15.07.55.json',
            'basic_iperf': 'bus.bs.2022.04.05.14.20.09.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/bus/pantheon_perf.json'),

            'bw': 'trace-3109898-bus',
            'trace': 'bus',
            'step': 1,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': 60
        }

    if trace == 'timessquare':
        return {
            'mimic': 'timessquare.mimic.2022.04.05.14.09.49.csv',
            'cubic': 'timessquare.cubic.2022.04.05.14.58.25.csv',
            'hybla': 'timessquare.hybla.2022.04.05.14.59.28.csv',
            'owl': 'timessquare.owl.2022.04.05.15.00.31.csv',
            'vegas': 'timessquare.vegas.2022.04.05.15.01.33.csv',
            'basic': 'timessquare.bs.2022.04.05.14.29.18.csv',

            'mimic_iperf': 'timessquare.mimic.2022.04.05.14.09.49.json',
            'cubic_iperf': 'timessquare.cubic.2022.04.05.14.58.25.json',
            'hybla_iperf': 'timessquare.hybla.2022.04.05.14.59.28.json',
            'owl_iperf': 'timessquare.owl.2022.04.05.15.00.31.json',
            'vegas_iperf': 'timessquare.vegas.2022.04.05.15.01.33.json',
            'basic_iperf': 'timessquare.bs.2022.04.05.14.29.18.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/timessquare/pantheon_perf.json'),

            'bw': 'trace-3189663-timessquare',
            'trace': 'timessquare',
            'step': 1,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': 60
        }

    
    if trace == 'wired':
        return {
            'mimic': 'wired.mimic.2022.04.05.16.38.10.csv',
            'cubic': 'wired.cubic.2022.04.05.16.33.36.csv',
            'hybla': 'wired.hybla.2022.04.05.16.34.40.csv',
            'owl': 'wired.owl.2022.04.05.16.35.43.csv',
            'vegas': 'wired.vegas.2022.04.05.16.36.45.csv',
            'basic': 'wired.bs.2022.04.05.16.45.27.csv',

            'mimic_iperf': 'wired.mimic.2022.04.05.16.38.10.json',
            'cubic_iperf': 'wired.cubic.2022.04.05.16.33.36.json',
            'hybla_iperf': 'wired.hybla.2022.04.05.16.34.40.json',
            'owl_iperf': 'wired.owl.2022.04.05.16.35.43.json',
            'vegas_iperf': 'wired.vegas.2022.04.05.16.36.45.json',
            'basic_iperf': 'wired.bs.2022.04.05.16.45.27.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/wired/pantheon_perf.json'),

            'bw': 'trace-3189663-timessquare',
            'trace': 'wired',
            'step': 1,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': 60
        }

def get_prod_musketeers(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':
        return {
            'mimic': 'att.lte.driving.mimic.2022.03.28.00.22.18.csv',
            'cubic': 'att.lte.driving.cubic.2022.03.07.17.34.02.csv',
            'hybla': 'att.lte.driving.hybla.2022.03.07.17.44.26.csv',
            'vegas': 'att.lte.driving.vegas.2022.03.07.17.37.55.csv',
            'owl': 'att.lte.driving.owl.2022.03.07.17.36.42.csv',
            'basic': 'bs.att.lte.driving.2022.03.07.13.21.54.csv',

            'mimic_iperf': 'att.lte.driving.mimic.2022.03.28.00.21.03.json',
            'cubic_iperf': 'att.lte.driving.cubic.2022.02.22.16.55.51.json',
            'hybla_iperf': 'att.lte.driving.hybla.2022.02.22.17.21.39.json',
            'vegas_iperf': 'att.lte.driving.vegas.2022.02.22.17.09.03.json',
            'owl_iperf': 'att.lte.driving.owl.2022.02.22.17.45.27.json',
            'basic_iperf': 'bs.att.lte.driving.2022.02.24.19.09.15.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/att.lte.driving/v1/pantheon_perf.v1.json'),

            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving',
            'step': 1,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': 60
        }

    if trace == 'tm.lte.short':
        return {
            'mimic': 'tm.lte.short.mimic.2022.03.28.00.26.13.csv',
            'cubic': 'tm.lte.short.cubic.2022.03.07.19.51.31.csv',
            'hybla': 'tm.lte.short.hybla.2022.03.07.19.52.35.csv',
            'owl': 'tm.lte.short.owl.2022.03.07.19.53.39.csv',
            'vegas': 'tm.lte.short.vegas.2022.03.07.19.54.42.csv',
            'basic': 'bs.tm.lte.short.2022.03.07.14.12.09.csv',

            'mimic_iperf': 'tm.lte.short.mimic.2022.03.28.00.25.09.json',
            'cubic_iperf': 'tm.lte.short.cubic.2022.02.22.18.34.31.json',
            'hybla_iperf': 'tm.lte.short.hybla.2022.02.22.18.12.00.json',
            'vegas_iperf': 'tm.lte.short.vegas.2022.02.22.18.23.06.json',
            'owl_iperf': 'tm.lte.short.owl.2022.02.22.18.00.41.json',
            'basic_iperf': 'bs.tm.lte.short.2022.02.24.20.00.24.json',

            'pantheon': os.path.join(utils.entry_path, 'log/pantheon/tm.lte.short/v1/pantheon_perf.v1.json'),

            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short',
            'step': 1,
            'info': 'Mimic experiment with verizon lte short up for 1000 steps',
            'max': 60
        }

    return {
        'mimic': 'vz.lte.short.mimic.2022.03.28.00.23.55.csv',
        'cubic': 'vz.lte.short.cubic.2022.03.07.21.34.11.csv',
        'hybla': 'vz.lte.short.hybla.2022.03.07.21.35.27.csv',
        'owl': 'vz.lte.short.owl.2022.03.07.21.36.36.csv',
        'vegas': 'vz.lte.short.vegas.2022.03.07.21.37.51.csv',
        'basic': 'bs.vz.lte.short.2022.03.07.15.39.30.csv',

        'mimic_iperf': 'vz.lte.short.mimic.2022.03.28.00.22.50.json',
        'cubic_iperf': 'vz.lte.short.cubic.2022.02.22.19.09.14.json',
        'hybla_iperf': 'vz.lte.short.hybla.2022.02.22.19.33.19.json',
        'vegas_iperf': 'vz.lte.short.vegas.2022.02.22.19.20.36.json',
        'owl_iperf': 'vz.lte.short.owl.2022.02.22.19.45.52.json',
        'basic_iperf': 'bs.vz.lte.short.2022.02.24.20.26.48.json',

        'pantheon': os.path.join(utils.entry_path, 'log/pantheon/vz.lte.short/v1/pantheon_perf.v1.json'),

        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short',
        'step': 1,
        'info': 'Mimic experiment with verizon lte short up for 1000 steps',
        'max': 60
    }


def get_policy_iperf(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':

        return {
            'active_explorer': 'att.lte.driving.active_explorer.2022.03.17.23.47.40.json',
            'active_greedy_percentile': 'att.lte.driving.adaptive_greedy_percentile.2022.03.17.23.36.53.json',
            'active_greedy_threshold': 'att.lte.driving.adaptive_greedy_threshold.2022.03.17.23.35.36.json',
            'active_greedy_weighted': 'att.lte.driving.adaptive_greedy_weighted.2022.03.17.23.38.12.json',
            'bootstrapped_ts': 'att.lte.driving.bootstrapped_ts.2022.03.17.23.39.45.json',
            'bootstrapped_ucb': 'att.lte.driving.bootstrapped_ucb.2022.03.17.23.41.27.json',
            'epsilon_greedy': 'att.lte.driving.epsilon_greedy.2022.03.17.23.44.29.json',
            'epsilon_greedy_decay': 'att.lte.driving.epsilon_greedy_decay.2022.03.17.23.43.03.json',
            'explore_first': 'att.lte.driving.explore_first.2022.03.17.23.46.04.json',
            'separate_classifiers': 'att.lte.driving.separate_classifiers.2022.03.17.23.49.57.json',
            'softmax_explorer': 'att.lte.driving.softmax_explorer.2022.03.17.23.51.22.json',
            # 'owl': 'att.lte.driving.2016.owl.2022.03.17.23.59.08.json',
            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving',
            'step': 10,
        }

    if trace == 'tm.lte.short':
        return {
            'active_explorer': 'tm.lte.short.active_explorer.2022.03.18.00.49.23.json',
            'active_greedy_percentile': 'tm.lte.short.adaptive_greedy_percentile.2022.03.18.00.25.39.json',
            'active_greedy_threshold': 'tm.lte.short.adaptive_greedy_threshold.2022.03.18.00.42.14.json',
            'active_greedy_weighted': 'tm.lte.short.adaptive_greedy_weighted.2022.03.18.00.26.13.json',
            'bootstrapped_ts': 'tm.lte.short.bootstrapped_ts.2022.03.18.00.43.19.json',
            'bootstrapped_ucb': 'tm.lte.short.bootstrapped_ucb.2022.03.18.00.44.34.json',
            'epsilon_greedy': 'tm.lte.short.epsilon_greedy.2022.03.18.00.47.12.json',
            'epsilon_greedy_decay': 'tm.lte.short.epsilon_greedy_decay.2022.03.18.00.46.05.json',
            'explore_first': 'tm.lte.short.explore_first.2022.03.18.00.48.17.json',
            'separate_classifiers': 'tm.lte.short.separate_classifiers.2022.03.18.00.30.04.json',
            'softmax_explorer': 'tm.lte.short.softmax_explorer.2022.03.18.00.30.39.json',
            # 'owl': 'tm.lte.short.owl.agent.2022.03.18.00.24.34.json',
            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short',
            'step': 10,
        }

    return {
        'active_explorer': 'vz.lte.short.active_explorer.2022.03.18.02.05.47.json',
        'active_greedy_percentile': 'vz.lte.short.adaptive_greedy_percentile.2022.03.18.02.02.18.json',
        'active_greedy_threshold': 'vz.lte.short.adaptive_greedy_threshold.2022.03.18.12.35.24.json',
        'active_greedy_weighted': 'vz.lte.short.adaptive_greedy_weighted.2022.03.18.12.36.27.json',
        'bootstrapped_ts': 'vz.lte.short.bootstrapped_ts.2022.03.18.12.37.46.json',
        'bootstrapped_ucb': 'vz.lte.short.bootstrapped_ucb.2022.03.18.12.38.57.json',
        'epsilon_greedy': 'vz.lte.short.epsilon_greedy.2022.03.18.02.04.42.json',
        'epsilon_greedy_decay': 'vz.lte.short.epsilon_greedy_decay.2022.03.18.12.40.02.json',
        'explore_first': 'vz.lte.short.explore_first.2022.03.18.12.41.08.json',
        'separate_classifiers': 'vz.lte.short.separate_classifiers.2022.03.18.12.42.18.json',
        'softmax_explorer': 'vz.lte.short.softmax_explorer.2022.03.18.14.55.50.json',
        # 'owl': 'vz.lte.short.owl.agent.2022.03.18.02.01.07.json',
        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short',
        'step': 10,
    }


def get_harm_iperf(trace: str = 'vz.lte.short') -> dict:

    if trace == 'att.lte.driving':

        return {
            # 'solo': 'att.lte.driving.cubic.solo.2022.04.19.19.35.04.json',
            'solo': 'att.lte.driving.cubic.solo.2022.04.20.10.48.05.json',
            # 'against': 'att.lte.driving.cubic.against.2022.04.19.19.44.35.json',
            'against': 'att.lte.driving.cubic.against.2022.04.20.10.14.38.json',
            'bw': 'ATT-LTE-driving.up',
            'trace': 'att.lte.driving',
        }

    if trace == 'tm.lte.short':
        return {
            # 'solo': 'tm.lte.short.cubic.solo.2022.04.19.19.36.57.json',
            'solo': 'tm.lte.short.cubic.solo.2022.04.20.10.44.45.json',
            # 'against': 'tm.lte.short.cubic.against.2022.04.19.19.42.14.json',
            'against': 'tm.lte.short.cubic.against.2022.04.20.10.16.16.json',
            'bw': 'TMobile-LTE-short.up',
            'trace': 'tm.lte.short',
        }

    return {
        # 'solo': 'vz.lte.short.cubic.solo.2022.04.19.19.38.16.json',
        'solo': 'vz.lte.short.cubic.solo.2022.04.20.10.43.29.json',
        # 'against': 'vz.lte.short.cubic.against.2022.04.19.19.39.53.json',
        'against': 'vz.lte.short.cubic.against.2022.04.20.10.18.24.json',
        'bw': 'Verizon-LTE-short.up',
        'trace': 'vz.lte.short',
    }

def get_geni_illinois_iperf() -> dict:

    return {
        'solo': 'none.cubic.solo.2022.04.21.22.06.35.json',
        'against': 'none.cubic.against.2022.04.21.22.14.04.json',
        'mimic_iperf': 'none.mimic.2022.04.21.22.14.05.json',
        'cubic_iperf': 'none.cubic.2022.04.21.17.22.16.json',
        'hybla_iperf': 'none.hybla.2022.04.21.17.23.18.json',
        'vegas_iperf': 'att.lte.driving.vegas.2022.02.22.17.09.03.json',
        'owl_iperf': 'none.owl.2022.04.21.17.24.19.json',
        'basic_iperf': 'none.bs.2022.04.21.22.43.43.jso n',
        'trace': 'none',
        'dir_path': 'log/iperf/geni/illinois'
    }

def get_geni_stanford_iperf() -> dict:

    return {
        'trace': 'none',
        'dir_path': 'log/iperf/geni/stanford'
    }


def get_geni_washington_iperf() -> dict:

    return {
        'trace': 'none',
        'dir_path': 'log/iperf/geni/washington'
    }