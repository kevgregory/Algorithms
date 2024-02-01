"""
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *
    
def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """
    # [!] TODO! Implement alpha-beta-pruning minimax search!
    alpha = float("-inf")
    beta = float("inf")
    is_starting_as_odd = True
    initial_depth = 0
    
    best_move_decision = determine_optimal_action(state, alpha, beta, is_starting_as_odd, initial_depth)
    
    return best_move_decision.selected_action

def determine_optimal_action(state: "T3State", alpha: float, beta: float, is_odd_turn: bool, depth: int) -> "Decision":
    """
    This is to find out what is the next best move using alpha-beta pruning.
    
    Parameters:
    - state: The current mess we're in.
    - alpha: Best score from our previous play.
    - beta: Lowest score the opponent can force on us.
    - is_odd_turn: True if it's the odd player's jam. False otherwise.
    - depth: How deep we are into the game tree.

    Returns:
    - Decision: What's our play? Comes with a value, chosen action, and depth.
    """
    if state.is_terminal():
        utility_value = utility(state, is_odd_turn)
        return Decision(utility_value, None, depth)
    
    current_decision = Decision(float("-inf") if is_odd_turn else float("inf"), None, depth)
    
    for action, next_state in state.get_transitions():
        next_move_decision = determine_optimal_action(next_state, alpha, beta, not is_odd_turn, depth + 1)
        
        if current_decision.should_update(next_move_decision.value, action, next_move_decision.depth, is_odd_turn):
            current_decision = Decision(next_move_decision.value, action, next_move_decision.depth)
        
        if is_odd_turn:
            alpha = max(alpha, current_decision.value)
        else:
            beta = min(beta, current_decision.value)
        
        if beta <= alpha:
            break

    return current_decision


# [Optional / Suggested] TODO! Add any helper methods or dataclasses needed to
# manage the alpha-beta-pruning minimax operation

@dataclass
class Decision:
    """
    Stores the game decisions.
    
    Parameters:
    - value: How good is this decision?
    - selected_action: The move we might go for.
    - depth: How deep in thought were we?
    """
    value: float
    selected_action: Optional["T3Action"]
    depth: int

    def should_update(self, new_value: float, action: Optional["T3Action"], new_depth: int, is_odd_turn: bool) -> bool:
        """
        Just to check if there are better plays.

        Parameters:
        - new_value: New score.
        - action: The potential new move.
        - new_depth: Depth of this potential play.
        - is_odd_turn: Are we in the odd player's shoes?

        Returns:
        - bool: True if we should reconsider, False if we're good.
        """
        if self.value != new_value:
            return new_value > self.value if is_odd_turn else new_value < self.value
        if self.depth != new_depth:
            return new_depth < self.depth
        if self.selected_action and action:
            return action < self.selected_action
        return False

def utility(state: "T3State", is_odd_turn: bool) -> int:
    """
    Score a terminal state - win, lose, or tie.
    
    Parameters:
    - state: Game's current situation.
    - is_odd_turn: True if odd player's turn. False, otherwise.

    Returns:
    - int: 0 for a tie, -1 for an odd player win, 1 otherwise.
    """
    if state.is_tie():
        return 0
    return -1 if is_odd_turn else 1