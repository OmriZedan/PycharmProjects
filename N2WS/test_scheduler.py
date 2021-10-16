from typing import Tuple, List


class Scheduler:
    def __init__(self, time_frame: Tuple[int, int]):
        self.time_frame = time_frame


def is_overlapping(time_frame_1: Tuple[int, int], time_frame_2: Tuple[int, int]):
    start_1, end_1 = time_frame_1
    start_2, end_2 = time_frame_2

    #        [3,    5]
    # [1,       4]
    if start_1 < start_2:
        if start_2 > end_1 > end_2:
            return True

    if start_1 > end_2 > end_1:
        return True

    return False


def check_overlapping_time_frames(schd_list: List[Scheduler]) -> bool:
    """
    check if all given schedulers describe mutually exclusive time frames.
    :param schd_list: list of Scheduler objects
    """

    list_time_frames = [schd.time_frame for schd in schd_list]
    for i, time_frame_2 in enumerate(list_time_frames):
        for j, time_frame_1 in enumerate(list_time_frames):
            if i <= j:
                continue
            if is_overlapping(time_frame_1, time_frame_2):
                return False

    return True

