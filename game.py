"""
Wordle Game Class

"""

import enum
import random, util, time


class Game:

    def __init__(self) -> None:
        with open("answer_words.txt", "r") as f:
            self.answerList = util.create_dict(f.read().upper().split())
        with open("allowed_words.txt", "r") as f:
            self.allowedWords = util.create_dict(f.read().upper().split())

    def playGames(self) -> None:
        with open("welcome.txt", "r") as f:
            print(f.read())
        answer = random.choice(list(self.answerList.keys()))
        guess = ""
        keyboard = {"A" : "","B" : "","C" : "","D" : "","E" : "","F" : "","G" : "","H" : "","I" : "","J" : "","K" : "","L" : "","M" : "",
                    "N" : "","O" : "","P" : "","Q" : "","R" : "","S" : "","T" : "","U" : "","V" : "","W" : "","X" : "","Y" : "","Z" : ""}
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
                for i, c in enumerate(guess):
                    if c == answer[i]:
                        keyboard[c] = "*"
                        toPrint += f"{c}*"
                    elif c in answer:
                        toPrint += f"{c}`"
                        keyboard[c] = "`"
                    else:
                        toPrint += f"{c} "
                        keyboard[c] = " "
                print(toPrint)
                    
                    


