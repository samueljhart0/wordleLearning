"""
Wordle Game Class

"""

from copy import deepcopy
from tracemalloc import start
from typing import Counter
from data import Data
from colorama import Fore
import util, time, random

ANSWER_FILE = "data/answer_words.txt"

class Game:
    def __init__(self, answer=None) -> None:
        if not answer:
            with open(ANSWER_FILE, "r") as f:
                self.gameData = Data(random.choice(list(f.read().upper().split())))
                f.close()
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
            # print(guess, self.gameData.trueAnswer)
        return guessCnt


    def playWithInfo(self):
        guess = ""
        firstFlag = True
        while guess != self.gameData.trueAnswer:
            print()
            if not firstFlag:
                print(Fore.BLACK + "WORD   E[Info]   Var[Info]  p(WORD)")
                topTen = self.gameData.giveTop(10)
                for row in topTen:
                    word, info, var, prob = row[0], row[1], row[2], row[3]
                    print(f"{word}  {round(info, 4)}     {round(var,4)}      {round(prob, 6)}")
                print(len(self.gameData.possible))
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