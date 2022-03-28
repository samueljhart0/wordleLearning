from typing import Counter
from colorama import Fore, init


"""
Class to delegate pattern matching to
"""

class Pattern:
    def __init__(self, word, answer) -> None:
        self.word = word
        self.answer = answer
        self.pattern = self.buildPattern()
        self.string = self.buildString()
        

    def buildPattern(self):
        adic = Counter([a for a in self.answer])
        pattern = ["b"] * len(self.word)
        for i, a in enumerate(self.answer):
            if self.word[i] == a:
                pattern[i] = "G"
                adic[a] -= 1
        for j, g in enumerate(self.word):
            if pattern[j] == "G":
                continue
            elif adic[g] is None:
                pattern[j] = "b"
            else:
                if adic[g] == 0:
                    pattern[j] = "b"
                else:
                    pattern[j] = "Y"
                    adic[g] -= 1
        return tuple(pattern)
    
    
    def buildString(self):
        toPrint = ""
        for i in range(len(self.word)):
            l, c  = self.word[i], self.pattern[i]
            if c == "G":
                toPrint += Fore.GREEN + f"{l}"
            elif c == "Y":
                toPrint += Fore.YELLOW + f"{l}"
            elif c == "b":
                toPrint += Fore.BLACK + f"{l}"
        return toPrint
    

    def violate(self, word):
        letterIndex = {l : [1, 1, 1, 1, 1] for l in self.word}
        letterColor = {l : "b" for l in self.word}
        for i, l in enumerate(self.word):
            if self.pattern[i] == "G":
                letterColor[l] = "G"
            elif self.pattern[i] == "Y":
                if letterColor[l] != "G":
                    letterColor[l] = "Y"
                letterIndex[l][i] = 0
            else:
                if letterColor[l] != "b":
                    letterIndex[l][i] = 0
                else:
                    letterIndex[l] = [0, 0, 0, 0, 0]
        for i, l in enumerate(word):
            if letterColor.get(l) is None:
                continue
            else:
                if letterIndex[l][i] == 0:
                    return True
        return False


    def match(self, word):
        for i, l in enumerate(word):
            if self.pattern[i] == "G" and l != self.word[i]:
                return False
            if self.pattern[i] == "Y" and self.word[i] not in word:
                return False
        return not self.violate(word)
