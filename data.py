from copy import deepcopy
from colorama import init
from math import log2 as log
from decision import TreeNode
from pattern import Pattern

"""
File for data processing and data exploration

Ideas for data storage:
1. Nested dictionaries where the first is all words starting with A and so on
2. N

Ideas for data exploration:
1. 26x5 heat map of prob of letter in each position; maybe two of these.
   One that sums by row and one that sums by column
2. 
"""

class Data:
    def __init__(self, answer, guessList = None, answerList = None):
        init(autoreset=True)
        if not guessList and not answerList:
            with open("allowed_words.txt", "r") as f:
                guessList = list(f.read().upper().split())
            answerList = deepcopy(guessList)
        self.guesses = guessList
        self.answers = answerList
        self.probTable = {}
        self.infoTable = {}
        self.trueAnswer = answer
        self.letters = {"A" : "B", "B" : "B", "C" : "B", "D" : "B", "E" : "B", "F" : "B", "G" : "B", "H" : "B", "I" : "B", "J" : "B", "K" : "B", "L" : "B", "M" : "B",
                        "N" : "B", "O" : "B", "P" : "B", "Q" : "B", "R" : "B", "S" : "B", "T" : "B", "U" : "B", "V" : "B", "W" : "B", "X" : "B", "Y" : "B", "Z" : "B"}


    def guessToString(self, guess):
        pattern = Pattern(guess, self.trueAnswer)
        self.update(pattern)
        return pattern.string


    def update(self, pattern):
        for i in range(len(pattern.word)):
            l, c = pattern.word[i], pattern.pattern[i]
            if c == "G":
                self.letters[l] = c
            elif c == "Y":
                if self.letters[l] != "G":
                    self.letters[l] = c
            elif c == "b":
                if self.letters[l] != "G" and self.letters[l] != "Y":
                    self.letters[l] = "b"
        newA = self.newAnswers(pattern)
        newG = self.newGuesses(pattern)
        self.probTable = {}
        self.infoTable = {}
        for w in newA:
            self.probTable[w] = 1 / len(newA)
        for w in newG:
            if self.probTable.get(w) is None:
                self.probTable[w] = 0.0
            self.infoTable[w] = 0
            patterns = {}
            for a in newA:
                p = Pattern(w, a)
                if patterns.get(p.pattern) is None:
                    patterns[p.pattern] = 0
                patterns[p.pattern] += 1
            for count in patterns.values():
                prob = count / len(newA)
                self.infoTable[w] += prob * -log(prob)
        self.guesses = newG
        self.answers = newA
        

    def newGuesses(self, pattern):
        newG = []
        for word in self.guesses:
            if not pattern.violate(word):
                newG.append(word)
        return newG

    def newAnswers(self, pattern):
        newA = []
        for word in self.answers:
            if pattern.match(word):
                newA.append(word)
        return newA

    def giveTopTen(self):
        if len(self.answers) == 1:
            return [(self.answers[0], 0.0, 1.0)]
        if len(self.answers) == 2:
            return [(self.answers[0], 1.0, 0.5), (self.answers[1], 1.0, 0.5)]
        topTen = []
        for word, info in self.infoTable.items():
            inserted = False
            for i, pack in enumerate(topTen):
                _, ti, _ = pack
                if info >= ti:
                    topTen.insert(i, (word, info, self.probTable[word]))
                    topTen.pop()
                    break
            if inserted == False and len(topTen) < 10:
                topTen.append((word, info, self.probTable[word]))
        return topTen



    def calcInfoGain(self, word):
        pattern = Pattern(word, self.trueAnswer)
