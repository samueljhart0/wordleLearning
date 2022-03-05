"""
Wordle Game Class

"""

from typing import Counter
from colorama import init, Fore, Back
import util, time, random

class Game:

    def __init__(self) -> None:
        init(autoreset=True)
        with open("answer_words.txt", "r") as f:
            self.answerList = util.create_dict(f.read().upper().split())
        with open("allowed_words.txt", "r") as f:
            self.allowedWords = util.create_dict(f.read().upper().split())

    def playGames(self, answer=None) -> None:
        with open("welcome.txt", "r") as f:
            print(f.read())
        if answer == None:
            answer = random.choice(list(self.answerList.keys()))
        keyboard = {"A" : "B","B" : "B","C" : "B","D" : "B","E" : "B","F" : "B","G" : "B","H" : "B","I" : "B","J" : "B","K" : "B","L" : "B","M" : "B",
                    "N" : "B","O" : "B","P" : "B","Q" : "B","R" : "B","S" : "B","T" : "B","U" : "B","V" : "B","W" : "B","X" : "B","Y" : "B","Z" : "B"}
        guess = ""
        while guess != answer:
            print()
            util.printAsKeyboard(keyboard)
            guess = input()
            if len(guess) != 5 or self.allowedWords.get(guess) is None:
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
                toPrint = ""
                """
                How do we count for keeping track of if letter is in word twice?

                Guess 1: Take letter out of answer once it is found
                """
                for pair in self.processGuess(guess, answer):
                    c, info = pair
                    if info == "G":
                        toPrint += Fore.GREEN + f"{c}"
                        keyboard[c] = "G"
                    elif info == "Y":
                        if keyboard[c] != "G":
                            keyboard[c] = "Y"
                        toPrint += Fore.YELLOW + f"{c}"
                    elif info == "b":
                        if keyboard[c] != "G" and keyboard[c] != "Y":
                            keyboard[c] = "b"
                        toPrint += Fore.BLACK + f"{c}"
                print(toPrint)

    def processGuess(self, guess, answer):
        adic = Counter([a for a in answer])
        letters = []
        for i, g in enumerate(guess):
            if adic[g] is None:
                letters.extend([(g, "b")])
            elif adic[g] == 0:
                letters.extend([(g, "b")])
            else:
                if guess[i] == answer[i]:
                    letters.extend([(g, "G")])
                else:
                    letters.extend([(g, "Y")])
                adic[g] -= 1
        return letters