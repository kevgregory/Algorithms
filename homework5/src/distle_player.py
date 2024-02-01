from edit_dist_utils import *
import random
from typing import Set, List, Tuple
class DistlePlayer:
    '''
    AI Distle Player! Contains all of the logic to automagically play
    the game of Distle with frightening accuracy (hopefully)
    '''

    def __init__(self) -> None:
        self.vocabSet: Set[str] = set()
        self.wordsToGuess: Set[str] = set()
        self.attemptsMade: int = 0
        self.lettersEliminated: Set[str] = set()
        self.guessRecord: List[Tuple[str, int, List[str]]] = []

    def start_new_game(self, dictionary: set[str], max_guesses: int) -> None:
        '''
        Called at the start of every new game of Distle, and parameterized by
        the dictionary composing all possible words that can be used as guesses,
        only ONE of which is the correct Secret word that your agent must
        deduce through repeated guesses and feedback.
        
        [!] Should initialize any attributes that are needed to play the
        game, e.g., by saving a copy of the dictionary, etc.
        
        Parameters:
            dictionary (set[str]):
                The dictionary of words from which the correct answer AND any
                possible guesses must be drawn
            max_guesses (int):
                The maximum number of guesses that are available to the agent
                in this game of Distle
        '''
        self.vocabSet = dictionary
        self.maxAttempts = max_guesses
        self.wordsToGuess = dictionary.copy()
        self.attemptsMade = 0
        self.lettersEliminated.clear()
        self.guessRecord.clear()

    def make_guess(self) -> str:
        '''
        Requests a new guess to be made by the agent in the current game of Distle.
        Uses only the DistlePlayer's attributes that had been originally initialized
        in the start_new_game method.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Returns:
            str:
                The next guessed word from this DistlePlayer
        '''
        if not self.wordsToGuess:
            raise ValueError("No more words left to guess.")

        # Selecting the first guess randomly
        if not self.guessRecord:
            chosenWord = random.choice(list(self.wordsToGuess))
        else:
            # Implementing a strategy for subsequent guesses
            chosenWord = self.next_guess_strategy()

        self.wordsToGuess.discard(chosenWord)
        self.attemptsMade += 1
        return chosenWord
    
    def next_guess_strategy(self) -> str:
        '''
        Strategy for choosing the next guess.
        
        Returns:
            str: The word selected as the next guess.
        '''
        # Example strategy: Choose the word with minimum edit distance from the last guess
        previousGuess = self.guessRecord[-1][0]
        return min(self.wordsToGuess, key=lambda word: edit_distance(word, previousGuess))

    def get_feedback(self, guess: str, edit_distance: int, transforms: list[str]) -> None:
        '''
        Called by the DistleGame after the DistlePlayer has made an incorrect guess.
        The feedback furnished is described in the parameters below. Your agent will
        use this feedback in an attempt to rule out as many remaining possible guess
        words as it can, through which it can then make better guesses in make_guess.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Parameters:
            guess (str):
                The last, incorrect guess made by this DistlePlayer
            edit_distance (int):
                The numerical edit distance between the guess your agent made and the
                secret word
            transforms (list[str]):
                The list of top-down transforms needed to turn the guess word into the
                secret word, i.e., the transforms that would be returned by your
                get_transformation_list(guess, secret_word)
        '''
        self.guessRecord.append((guess, edit_distance, transforms))

        # Refining the set of words to guess based on the feedback
        self.refine_guesses_based_on_feedback(guess, transforms)

    def refine_guesses_based_on_feedback(self, guess: str, transforms: list[str]):
        '''
        Refines the set of possible words based on the feedback received.
        
        Parameters:
            guess (str): The guessed word.
            transforms (list[str]): Required transformations to reach the secret word.
        '''
        updatedWordsToGuess = set()
        for word in self.wordsToGuess:
            if get_transformation_list(guess, word) == transforms:
                updatedWordsToGuess.add(word)
        self.wordsToGuess = updatedWordsToGuess
