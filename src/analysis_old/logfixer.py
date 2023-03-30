import os
import traceback

from helper import utils

def get_iperf_logs() -> list:
    dir = os.path.join(utils.entry_path, "log/iperf/protocol")
    files = sorted(os.listdir(dir))

    traces = []

    for file in files:

        if  file.find(".bs.") == -1:
            traces.append(file)

    
    return traces

def get_trace_logs() -> list:
    dir = os.path.join(utils.entry_path, "log/prod/thesis")
    files = sorted(os.listdir(dir))

    traces = []

    for file in files:

        if file.endswith("csv") and file.find("verbose") == -1 and file.find(".bs.") == -1:
            traces.append(file)

    
    return traces

def main():
    
    iperf_logs = get_iperf_logs()
    trace_logs = get_trace_logs()

    # for f in iperf_logs:
    for index in range(len(iperf_logs)):
        iperf_log = iperf_logs[index]
        trace_log = trace_logs[index]

        iperf_logfile = utils.get_fullpath(iperf_log)

        new_logfilename = trace_log.replace("csv", "json")
        iperfList = iperf_logfile.split("/")
        iperfList[len(iperfList) - 1] = new_logfilename
        new_logfilepath = "/".join(iperfList)

        print(f'Fixing: {trace_logs[index]} -> {iperf_logs[index]} -> {new_logfilename}')    
        utils.change_file_name(iperf_logfile, new_logfilepath)
        # print(f'{iperf_logfile}, {new_logfilepath}')




if __name__ == '__main__':

    try:
        main()

    except Exception as err:
        print('\n')
        print(traceback.format_exc())
