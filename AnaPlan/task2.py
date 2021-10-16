from typing import List, Dict


class Packet():
    def __init__(self, PID, continuity_counter):
        self.PID = PID
        self.countinuity_counter = continuity_counter


def count_lost_packets(list_packets: List[Packet]) -> Dict[str, int]:
    """
    Counts the number of missing packets for each PID in list packets
    :param list_packets: a list of Packet objects
    :return: a dictionary of the following format: {PID: #missing packets}
    """
    default_info = dict(last_countinuity_counter=-1, missing_packets=0)
    dict_pid_continuity_info = dict()
    calc_diff = lambda x, y: x - y if (x - y) > 0 else x - y + 16
    for pct in list_packets:
        pid = pct.PID
        info = dict_pid_continuity_info.get(pid, default_info)
        # countinuity_counter_diff = pct.countinuity_counter - info['last_countinuity_counter']
        # if countinuity_counter_diff < 0:
        #     countinuity_counter_diff += 16
        countinuity_counter_diff = calc_diff(pct.countinuity_counter, info['last_countinuity_counter'])

        info['missing_packets'] += countinuity_counter_diff - 1
        info['last_countinuity_counter'] = pct.countinuity_counter
        dict_pid_continuity_info[pid] = info

    return {pid: info['missing_packets'] for pid, info in dict_pid_continuity_info.items()}
