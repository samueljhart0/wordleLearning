from copy import deepcopy
from tracemalloc import start
from typing import Counter
from data import Data
from colorama import Fore
import time, random

"""
This class handles the Wordle game itself. It is used to start a Wordle game and has a few options for how the game can
be played: classic, with information, and simulated by the computer algorithm devised in this project. It is the
instance of the game, whose data is handled by the corresponding Data class.
"""

ANSWER_FILE = "data/answer_words.txt"

class Game:
    """
    Game initializer that sets up the Wordle game with a predetermined answer. Note that the default answer is None
    which is used for the 'classic' mode in which the answer is decided randomly. This instance will initialize the
    Wordle answer, as well as the allowed guess lists and answer lists, and handle the progression of the game through 
    guesses.

    Parameters:

    answer : the true answer of the Wordle game that this instance represents.

    """
    def __init__(self, answer=None) -> None:
        if not answer:
            with open(ANSWER_FILE, "r") as f:
                self.gameData = Data(random.choice(list(f.read().upper().split())))
        else:
            self.gameData = Data(answer)
        self.accepted = {}
        for guess in self.gameData.allowed:
            self.accepted[guess] = True


    def simulate(self, startWord):
        """
        This function simulates an entire Wordle game given the starting word. It then returns the number of guesses
        required to get the answer.

        Parameters:

        startWord : the start word for the puzzle.

        Returns:

        guessCnt : the number of guesses it took to reach the answer.
        """
        guess = startWord
        guessCnt = 1
        self.gameData.processGuess(guess)
        while guess != self.gameData.trueAnswer:
            nextGuess = self.gameData.giveNextGuess()
            self.gameData.processGuess(nextGuess)
            guessCnt += 1
            guess = nextGuess
        return guessCnt


    def playWithInfo(self):
        """
        This function is used to play a normal Wordle game except the player receives information about best guesses
        from the computer. They must use their own first guess and the computer will assist on future guesses.
        """
        print("This is the Wordle game with assistance from the computer. After each of your guesses, the computer\n"+
              "will give recommendations as to what your next guess should be. Note that for each word it will\n"+
              "display the amount of information you can expect to gain and the probability of that word being the\n"+
              "answer.")
        print("Now give your five-letter guesses in all caps:")
        guess = ""
        firstFlag = True
        while guess != self.gameData.trueAnswer:
            print()
            if not firstFlag:
                print(Fore.BLACK + "WORD   E[Info]   p(WORD)")
                topTen = self.gameData.giveTop(10)
                for row in topTen:
                    word, info, prob = row[0], row[1], row[2]
                    print(f"{word}  {round(info, 4)}     {round(prob, 6)}")
            guess = input()
            if guess == "ANSWER":
                print(self.gameData.trueAnswer)
            elif len(guess) != 5 or self.accepted.get(guess) is None:
                print("Invalid word!")
                time.sleep(2)
                if firstFlag:
                    print("\033[A                                                                  \033[A")
                    print("\033[A                                                                  \033[A")
                else:
                    for _ in range(len(topTen) + 2):
                        print("\033[A                                                                  \033[A")
                    print("\033[A                                                                  \033[A")
                guess = ""
            else:
                if firstFlag:
                    firstFlag = False
                    print("\033[A                                                                  \033[A")
                    print("\033[A                                                                  \033[A")
                    print(self.gameData.processGuess(guess))
                else:
                    for _ in range(len(topTen) + 2):
                        print("\033[A                                                                  \033[A")
                    print("\033[A                                                                  \033[A")
                    print(self.gameData.processGuess(guess))             

    def playClassic(self):
        """
        This is the classic Wordle game with no assistance from the computer. You are on your own.
        """
        print("This is the classic Wordle game with no assistance from the computer. You are on your own.")
        print("Now give your five-letter guesses in all caps:")
        guess = ""
        while guess != self.gameData.trueAnswer:
            guess = input()
            if len(guess) != 5 or self.accepted.get(guess) is None:
                print("Invalid word!")
                time.sleep(2)
                guess = ""
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
            else:
                print("\033[A                   \033[A")
                print(self.gameData.processGuess(guess))