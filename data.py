from copy import deepcopy
from importlib.metadata import distribution
from tkinter import Pack
from colorama import init, Fore
import numpy as np
import itertools as it
from util import logAll

"""
This file handles aspects of the data associated with the game. Some of these functions are not my own. Much credit has
to be given to Grant Sanderson, aka 3Blue1Brown. Without his help, I would not have been able to produce some of my
results. More documentation coming soon!
"""

GREY = np.uint8(0)
YELLOW = np.uint8(1)
GREEN = np.uint8(2)

WORD_FILE = "data/allowed_words.txt"
PATTERN_FILE = "data/patternMatrix.npy"

class Data:
    def __init__(self, answer, allowed = None, possible = None):
        init(autoreset=True)
        if not possible:
            with open(WORD_FILE, "r") as f:
                allowed = list(f.read().upper().split())
                possible = deepcopy(allowed)
        self.allowed = allowed
        self.possible = possible
        self.trueAnswer = answer
        self.patterns = dict()

    # Functions to use in Game

    def processGuess(self, guess):
        pattern = self.getPattern(guess, self.trueAnswer)
        string = self.patternToString(pattern, guess)
        self.updateData(guess, pattern)
        return string

    def updateData(self, guess, pattern):
        self.possible = self.getPossibleWords(guess, pattern, self.possible)

    def giveNextGuess(self):
        if len(self.possible) < 4:
            return self.possible[0]
        else:
            C = self.getPatternProbs(self.allowed, self.possible)
            C[C==0.0] = 1.0
            E = (-C*np.log2(C)).sum(1)
            return self.allowed[np.argmax(E)]


    def giveTopTen(self):
        if len(self.possible) == 1:
            return [(self.possible[0], 0.0, 1.0)]
        if len(self.possible) == 2:
            return [(self.possible[0], 1.0, 0.5), (self.possible[1], 1.0, 0.5)]
        probs = {p : 1 / len(self.possible) for p in self.possible}
        C = self.getPatternProbs(self.allowed, self.possible)
        C[C==0.0] = 1.0
        E = (-C * np.log2(C)).sum(1)
        ind = np.argsort(E)[-10:]
        topTen = []
        for i in ind:
            topTen.insert(0, (self.allowed[i], E[i], probs.get(self.allowed[i], 0.0)))
        return topTen
        

    def statsToPrint(self):
        topTen = self.giveTopTen()
    
    # General Functions

    def wordsToArrays(self, words):
        return np.array([[ord(c) for c in w] for w in words], dtype=np.uint8)
    
    
    def patternMatrix(self, words1, words2):
        array1, array2 = map(self.wordsToArrays, (words1, words2))
        equality = np.zeros((len(words1), len(words2), 5, 5), dtype=bool)
        for i, j in it.product(range(5), range(5)):
            equality[:, :, i, j] = np.equal.outer(array1[:,i], array2[:,j])
        patterns = np.zeros((len(array1), len(array2), 5), dtype=np.uint8)
        for i in range(5):
            matches = equality[:, :, i, i].flatten()
            patterns[:,:,i].flat[matches] = GREEN
            for k in range(5):
                equality[:,:,k,i].flat[matches] = False
                equality[:,:,i,k].flat[matches] = False
        for i, j in it.product(range(5), range(5)):
            matches = equality[:,:,i,j].flatten()
            patterns[:,:,i].flat[matches] = YELLOW
        return np.dot(patterns, (3**np.arange(5)).astype(np.uint8))

    def getPatternMatrix(self, words1, words2):
        if not self.patterns:
            self.patterns["grid"] = np.load(PATTERN_FILE)
            self.patterns["wordsToIndex"] = dict(zip(self.allowed, it.count()))
        grid = self.patterns["grid"]
        wordsToIndex = self.patterns["wordsToIndex"]
        ind1 = [wordsToIndex[w] for w in words1]
        ind2 = [wordsToIndex[w] for w in words2]
        return grid[np.ix_(ind1, ind2)]


    def getPattern(self, guess, answer):
        if self.patterns:
            saved_words = self.patterns["wordsToIndex"]
            if guess in saved_words and answer in saved_words:
                return self.getPatternMatrix([guess], [answer])[0,0]
        return self.patternMatrix([guess], [answer])[0,0]


    def stringToPattern(self, pattern_string):
        return sum((3**i) * int(c) for i, c in enumerate(pattern_string))


    def patternToList(self, pattern):
        result = []
        curr = pattern
        for x in range(5):
            result.append(curr % 3)
            curr = curr // 3
        return result    

    def patternToString(self, pattern, word):
        d = {GREY : Fore.BLACK, YELLOW : Fore.YELLOW, GREEN : Fore.GREEN}
        return "".join(d[c] + word[i] for i, c in enumerate(self.patternToList(pattern)))

    def patternsToString(self, patterns, words):
        return "\n".join(map(self.patternToString, (patterns, words)))

    def getPossibleWords(self, guess, pattern, words):
        all_patterns = self.getPatternMatrix([guess], words).flatten()
        return list(np.array(words)[all_patterns == pattern])

    def getAllowedWords(self, guess, pattern, words):
        all_patterns = self.getPatternMatrix([guess], words).flatten()
        list = self.patternToList(pattern)
        return

    def getWordBuckets(self, guess, possibleWords):
        buckets = [[] for _ in range(243)]
        hashes = self.getPatternMatrix([guess], possibleWords).flatten()
        for i, word in zip(hashes, possibleWords):
            buckets[i].append(word)
        return buckets
    
    def getPatternProbs(self, allowed, possible):
        probs = [1.0 / len(possible) for _ in possible]
        patterns = self.getPatternMatrix(allowed, possible)
        counts = np.zeros((len(allowed), 243))
        for j, prob in enumerate(probs):
            counts[np.arange(len(allowed)), patterns[:, j]] += prob
        return counts