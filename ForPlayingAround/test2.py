from enum import Enum
from typing import List, Dict


class Sides(Enum):
    UP = 0
    DOWN = 1
    FRONT = 2
    BACK = 3
    LEFT = 4
    RIGHT = 5


class Colors(Enum):
    YELLOW = 0
    BLUE = 1
    RED = 2
    GREEN = 3


CUBE_SIDES = 6
SIDES_TO_CHECK = [Sides.UP.name, Sides.DOWN.name, Sides.FRONT.name, Sides.BACK.name]
# each number refers to a face on the cube
CUBE_PERMUTATIONS = [
    dict(UP=0, DOWN=1, FRONT=2, BACK=3, LEFT=4, RIGHT=5),
    dict(UP=0, DOWN=1, FRONT=5, BACK=4, LEFT=2, RIGHT=3),
    dict(UP=0, DOWN=1, FRONT=3, BACK=2, LEFT=5, RIGHT=4),
    dict(UP=0, DOWN=1, FRONT=4, BACK=5, LEFT=3, RIGHT=2),

    dict(UP=1, DOWN=0, FRONT=3, BACK=2, LEFT=4, RIGHT=5),
    dict(UP=1, DOWN=0, FRONT=5, BACK=4, LEFT=3, RIGHT=2),
    dict(UP=1, DOWN=0, FRONT=2, BACK=3, LEFT=5, RIGHT=4),
    dict(UP=1, DOWN=0, FRONT=4, BACK=5, LEFT=2, RIGHT=3),

    dict(UP=2, DOWN=3, FRONT=1, BACK=0, LEFT=4, RIGHT=5),
    dict(UP=2, DOWN=3, FRONT=5, BACK=4, LEFT=1, RIGHT=0),
    dict(UP=2, DOWN=3, FRONT=0, BACK=1, LEFT=5, RIGHT=4),
    dict(UP=2, DOWN=3, FRONT=4, BACK=5, LEFT=0, RIGHT=1),

    dict(UP=3, DOWN=2, FRONT=0, BACK=1, LEFT=4, RIGHT=5),
    dict(UP=3, DOWN=2, FRONT=5, BACK=4, LEFT=0, RIGHT=1),
    dict(UP=3, DOWN=2, FRONT=1, BACK=0, LEFT=5, RIGHT=4),
    dict(UP=3, DOWN=2, FRONT=4, BACK=5, LEFT=1, RIGHT=0),

    dict(UP=4, DOWN=5, FRONT=1, BACK=0, LEFT=3, RIGHT=2),
    dict(UP=4, DOWN=5, FRONT=2, BACK=3, LEFT=1, RIGHT=0),
    dict(UP=4, DOWN=5, FRONT=0, BACK=1, LEFT=2, RIGHT=3),
    dict(UP=4, DOWN=5, FRONT=3, BACK=2, LEFT=0, RIGHT=1),

    dict(UP=5, DOWN=4, FRONT=0, BACK=1, LEFT=3, RIGHT=2),
    dict(UP=5, DOWN=4, FRONT=2, BACK=3, LEFT=0, RIGHT=1),
    dict(UP=5, DOWN=4, FRONT=1, BACK=0, LEFT=2, RIGHT=3),
    dict(UP=5, DOWN=4, FRONT=3, BACK=2, LEFT=1, RIGHT=0),
]


class Cube(object):
    colors = dict
    list_permutations = []

    def __init__(self, colors: Dict[str, str] = None):
        assert len(colors) == CUBE_SIDES, "Illegal length"
        self.colors = colors
        self.list_permutations = self._list_all_color_permutations()

    def _get_permutation(self, perm: dict) -> dict:
        """
        Get a representation of a cube
        :param perm: an arrangement symbolized by (Side: Face) values
        :return: dict with (Side: color) pairs.
        """
        return {side: self.colors[Sides(face).name] for side, face in perm.items()}

    def _list_all_color_permutations(self) -> List[dict]:
        """
        get a list of all possible color cube permutations (states)
        :return: List of dictionaries representing color-cube permutations.
        """
        return [self._get_permutation(perm=perm) for perm in CUBE_PERMUTATIONS]


def good_solution(solution: List[Dict]):
    """
    A solution is good if all of it's checkable side show 4 different colors.
    :param solution: a list of cube permutations.
    :return: True if a solution is good else False.
    """
    for side in SIDES_TO_CHECK:
        values = [cube.get(side) for cube in solution]
        if len(values) != len(set(values)):
            return False

    return True


final_solution = None


def backtracking_solution(list_cubes: List[Cube], solution: List[dict] = None):
    """
    Use backtracking to search for a good solution.
    :param list_cubes: list of Cube objects.
    :param solution: place holder for current solution.
    """
    solution = solution or []
    if len(list_cubes) == 0:
        if good_solution(solution=solution):
            solution_str = '\n'.join([str(list(cube.items())) for cube in solution])
            print(f"Solution:\n\n{solution_str}")
            exit()
        else:
            return

    cube = list_cubes.pop()
    for permutation in cube.list_permutations:
        solution.append(permutation)
        if good_solution(solution=solution):
            backtracking_solution(list_cubes, solution)
        solution.pop()


# ===================================================  MAIN   ======================================================== #
c1_colors = dict(UP=Colors.BLUE.name,
                 DOWN=Colors.YELLOW.name,
                 FRONT=Colors.GREEN.name,
                 BACK=Colors.RED.name,
                 LEFT=Colors.RED.name,
                 RIGHT=Colors.RED.name)

c2_colors = dict(UP=Colors.GREEN.name,
                 DOWN=Colors.YELLOW.name,
                 FRONT=Colors.BLUE.name,
                 BACK=Colors.RED.name,
                 LEFT=Colors.YELLOW.name,
                 RIGHT=Colors.RED.name)

c3_colors = dict(UP=Colors.YELLOW.name,
                 DOWN=Colors.BLUE.name,
                 FRONT=Colors.RED.name,
                 BACK=Colors.BLUE.name,
                 LEFT=Colors.GREEN.name,
                 RIGHT=Colors.GREEN.name)

c4_colors = dict(UP=Colors.GREEN.name,
                 DOWN=Colors.YELLOW.name,
                 FRONT=Colors.RED.name,
                 BACK=Colors.GREEN.name,
                 LEFT=Colors.YELLOW.name,
                 RIGHT=Colors.BLUE.name)

c1 = Cube(colors=c1_colors)
c2 = Cube(colors=c2_colors)
c3 = Cube(colors=c3_colors)
c4 = Cube(colors=c4_colors)

backtracking_solution(list_cubes=[c1, c2, c3, c4])
