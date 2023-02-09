import os
import sys
import subprocess
import traceback
from helper import context, utils
from datetime import datetime
import yaml
from network.netlink_communicator import NetlinkCommunicator

TIME_FORMAT = '%Y.%m.%d.%H.%M.%S'


def time_to_str() -> str:

    return datetime.now().strftime(TIME_FORMAT)


def str_to_time(time: str) -> datetime:

    return datetime.strptime(time, TIME_FORMAT)


def parse_models_config():
    with open(os.path.join(context.entry_dir, 'config/models.yml')) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)


def parse_protocols_config():
    with open(os.path.join(context.entry_dir, 'config/protocols.yml')) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)


def parse_pantheon_protocols_config():
    location = utils.get_fullpath('/pantheon/src/config.yml')

    if location == None or location.strip() == '':
         sys.exit('Pantheon not installed on your machine')

    with open(location) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)

    
def parse_traces_config():
    with open(os.path.join(context.entry_dir, 'config/traces.yml')) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)


def parse_training_config():
    with open(os.path.join(context.entry_dir, 'config/train.yml')) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)


def parse_prod_config():
    with open(os.path.join(context.entry_dir, 'config/prod.yml')) as config:
        return yaml.load(config, Loader=yaml.BaseLoader)


def get_number_of_actions(comm: NetlinkCommunicator) -> int:

    response = comm.recv_msg()
    data = comm.read_netlink_msg(response)
    data_decoded = data.decode('utf-8')
    split_data = data_decoded.split(';')

    nchoices = int(split_data[0])
    protocols = {}

    for index, entry in enumerate(split_data):
        if index > 0 and entry != '':
            protocolKey = entry.split(':')
            protocols[protocolKey[1]] = int(protocolKey[0])

    return nchoices, protocols


def get_fullpath(file: str) -> str:

    try:

        path = subprocess.check_output(['locate', file])

        return path.strip().decode('utf-8')

    except Exception as _:
        print('\n')
        print(traceback.ormat_exc())


def change_file_name(old_name: str, new_name: str) -> None:
    try:
        os.rename(old_name, new_name)
    except Exception as _:
        print('\n')
        print(traceback.print_exc())


def check_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
