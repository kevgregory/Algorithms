'''
CMSI 2130 - Homework 1
Author: <Kevin Thomas>

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
from queue import PriorityQueue
from maze_problem import MazeProblem
from dataclasses import *
from typing import *

@dataclass(order=True)
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    # >> [MC] Don't forget docstrings for f, h, and g!
    # >> [MC] Poor variable name -- what's this hold, what's its purpose? (-0.5)
    f: float
    h: float
    g: float
    player_loc: tuple[int, int]
    action: str
    parent: Optional["SearchTreeNode"]
    # TODO: Add any other attributes and method overrides as necessary!

    # >> [MC] OK, but custom class objects like SearchTreeNodes can be stored directly inside of
    # a PriorityQueue as long as their __lt__ method is overridden, just like in CW1. Using the
    # tuple method (priority, item) isn't functionally wrong, but stylistically more verbose than
    # needed here.
    def __str__(self) -> str:
        return "@: " + str(self.player_loc)

# >> [MC] Provide proper docstrings for ALL methods, including helpers you write (-0.25)
# >> [MC] Does this compute the Manhattan distance to the nearest *unshot* target?
# Otherwise, you might be backtracking to an already-collected one
def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def total_target_distance(player_loc: tuple[int, int], targets_left: set) -> int:
    if not targets_left:
        return 0
    return sum(manhattan_distance(player_loc, target) for target in targets_left)

def _get_solution(node: "SearchTreeNode") -> list[str]:
    """
    Returns a solution (a sequence of str actions) from the given
    SearchTreeNode node, presumed to be a goal state

    Parameters:
        node (SearchTreeNode):
            A goal SearchTreeNode in the search tree

    Returns:
        list[str]:
            A solution to the problem: a sequence of actions leading from the initial
            state to the goal.
    """
    soln = []
    while node.parent is not None:
        soln.append(node.action)
        node = node.parent
    soln.reverse()
    return soln

def pathfind(problem: "MazeProblem") -> Optional[list[str]]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """
    # TODO: Implement A* Graph Search for the Pathfinding Biathlon!
    # Setup
    frontier: PriorityQueue["SearchTreeNode"] = PriorityQueue()
    
    start_loc = problem.get_initial_loc()
    start_targets = frozenset(problem.get_initial_targets())
    start_h = total_target_distance(start_loc, start_targets)
    start_node = SearchTreeNode(f=start_h, g=0.0, h=start_h, player_loc=(start_loc, start_targets), action="", parent=None)
    frontier.put(start_node)

    closed_list = set()
    
    while not frontier.empty():
        expanding = frontier.get()

        current_loc, targets_left = expanding.player_loc

        if (current_loc, targets_left) in closed_list:
            continue

        closed_list.add((current_loc, targets_left))
        
        # >> [MC] Remove print statements before submission in the future; they will substantially
        # slow your solution down! (-0.25)
        print(f"Moving {expanding.action} to {current_loc}")
        print(f"Cost of Node: {expanding.f}")
        
        if not targets_left:
            solution = _get_solution(expanding)
            print("BOOM , GOAL FOUND!")
            print(f"location? : {current_loc}")
            print(f"Solution:\n{solution}")
            return _get_solution(expanding)

        transitions = problem.get_transitions(current_loc, targets_left)
        for action, result in transitions.items():
            new_loc = result["next_loc"]
            new_targets_left = frozenset(targets_left - result["targets_hit"])

            if (new_loc, new_targets_left) in closed_list:
                continue

            g_new = expanding.g + problem.get_transition_cost(action, current_loc)
            h_new = total_target_distance(new_loc, new_targets_left)
            f_new = g_new + h_new

            child_node = SearchTreeNode(f=f_new, g=g_new, h=h_new, player_loc=(new_loc, new_targets_left), action=action, parent=expanding)
            frontier.put(child_node)

    # No solution
    return None

# ===================================================
# >>> [MC] Summary
# A great submission that shows strong command of
# programming fundamentals, generally good style,
# and a good grasp on the problem and supporting
# theory of A*. Indeed, there is definitely
# a lot to like in what you have above, but
# I think you could have tested it a little more just
# to round out the several edge cases that evaded your
# detection. Give yourself more time to test + debug
# future submissions and you'll be golden!
# ---------------------------------------------------
# >>> [MC] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
#
# [~] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [~] Proper docstrings provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:          88 / 100 (-2 / missed unit test)
# Mypy Penalty:        -2 (-2 if mypy wasn't clean)
# Style Penalty:       -1
# Total:                85 / 100
# ===================================================