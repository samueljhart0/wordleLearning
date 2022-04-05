"""
Wordle Game Class

"""

from copy import deepcopy
from tracemalloc import start
from typing import Counter
from data import Data
from colorama import init, Fore, Back
import util, time, random

ANSWER_FILE = "data/answer_words.txt"

class Game:
    def __init__(self, answer=None) -> None:
        init(autoreset=True)
        if not answer:
            with open(ANSWER_FILE, "r") as f:
                self.gameData = Data(random.choice(list(f.read().upper().split())))
        else:
            self.gameData = Data(answer)
        self.accepted = {}
        for guess in self.gameData.allowed:
            self.accepted[guess] = True

    def simulate(self, startWord):
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
        guess = ""
        firstFlag = True
        while guess != self.gameData.trueAnswer:
            print()
            if not firstFlag:
                print("WORD   E[Info]  p(WORD)")
                topTen = self.gameData.giveTopTen()
                for row in topTen:
                    word, info, prob = row[0], row[1], row[2]
                    print(word, round(info, 4), round(prob, 4))
            guess = input()
            if len(guess) != 5 or self.accepted.get(guess) is None:
                print("Invalid word!")
                time.sleep(2)
                if firstFlag:
                    print("\033[A                            \033[A")
                    print("\033[A                            \033[A")
                else:
                    for _ in range(len(topTen) + 2):
                        print("\033[A                            \033[A")
                    print("\033[A                            \033[A")
                guess = ""
            else:
                if firstFlag:
                    firstFlag = False
                    print("\033[A                            \033[A")
                    print("\033[A                            \033[A")
                    print(self.gameData.processGuess(guess))
                else:
                    for _ in range(len(topTen) + 2):
                        print("\033[A                            \033[A")
                    print("\033[A                            \033[A")
                    print(self.gameData.processGuess(guess))             

    def playClassic(self):
        guess = ""
        while guess != self.gameData.trueAnswer:
            print()
            guess = input()
            if len(guess) != 5 or self.accepted.get(guess) is None:
                print("Invalid word!")
                time.sleep(2)
                guess = ""
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
            else:
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print(self.gameData.processGuess(guess))