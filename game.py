"""
Wordle Game Class

"""

from copy import deepcopy
from typing import Counter
from data import Data
from colorama import init, Fore, Back
import util, time, random

class Game:

    def __init__(self) -> None:
        init(autoreset=True)
        with open("answer_words.txt", "r") as f:
            self.gameData = Data(random.choice(list(f.read().upper().split())))
        self.accepted = {}
        for guess in self.gameData.guesses:
            self.accepted[guess] = True

    def playWithInfo(self):
        guess = ""
        firstFlag = True
        while guess != self.gameData.trueAnswer:
            print()
            util.printAsKeyboard(self.gameData.letters)
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
                guess = ""
            else:
                if firstFlag:
                    firstFlag = False
                print(self.gameData.guessToString(guess))

    def limitedInfo(self):
        self.gameData.guesses = random.sample(self.gameData.guesses, 50)
        self.gameData.answers = deepcopy(self.gameData.guesses)
        if self.gameData.trueAnswer not in self.gameData.guesses:
            self.gameData.guesses.append(self.gameData.trueAnswer)
        if self.gameData.trueAnswer not in self.gameData.answers:
            self.gameData.answers.append(self.gameData.trueAnswer)
        guess = ""
        firstFlag = True
        while guess != self.gameData.trueAnswer:
            print(self.gameData.guesses)
            print(self.gameData.answers)
            print()
            util.printAsKeyboard(self.gameData.letters)
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
                guess = ""
            else:
                if firstFlag:
                    firstFlag = False
                print(self.gameData.guessToString(guess))
                

    def playClassic(self):
        guess = ""
        while guess != self.gameData.trueAnswer:
            print()
            util.printAsKeyboard(self.gameData.letters)
            guess = input()
            if len(guess) != 5 or guess not in self.gameData.guesses:
                print("Invalid word!")
                time.sleep(2)
                guess = ""
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
            else:
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print("\033[A                   \033[A")
                print(self.gameData.processGuess(guess, self.gameData.trueAnswer))