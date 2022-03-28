import math
from typing import Counter
"""

File to hold decision tree class

"""

class TreeNode:
    def __init__(self, word = None, possibleAnswers = None, buildTree = False) -> None:
        self.word = word
        self.possibleAnswers = possibleAnswers
        if word and possibleAnswers:
            self.numberAnswers = len(self.possibleAnswers)
            self.patterns = self.generatePatterns(word)
            self.expectedInfo = 0
            for answers in self.patterns.values():
                prob = len(answers) / self.numberAnswers
                h = -1 * math.log2(prob)
                self.expectedInfo += prob * h
            if buildTree:
                self.children = self.buildChildren(buildTree)
    
    
    def generatePatterns(self, word):
        patterns = dict()
        for answer in self.possibleAnswers:
            adic = Counter([a for a in answer])
            letters = ["b"] * 5
            for i, a in enumerate(answer):
                if word[i] == a:
                    letters[i] = "G"
                    adic[a] -= 1
            for j, g in enumerate(word):
                if letters[j] == "G":
                    continue
                elif adic[g] is None:
                    letters[j] = "b"
                else:
                    if adic[g] == 0:
                        letters[j] = "b"
                    else:
                        letters[j] = "Y"
                        adic[g] -= 1
            letters = tuple(letters)
            if patterns.get(letters) is None:
                patterns[letters] = [answer]
            else:
                patterns[letters].append(answer)
        return patterns

    def buildChildren(self, buildTree):
        children = []
        for answers in self.patterns.values():
            if len(answers) == 1 and answers[0] == self.word:
                children.append(TreeNode())
                continue
            best = answers[0]
            maxInfo = 0
            for word in answers:
                node = TreeNode(word, answers)
                info = node.expectedInfo
                if info > maxInfo:
                    maxInfo = info
                    best = word
            children.append(TreeNode(best, answers, buildTree))




class WordleTree:
    """

    Class that builds tree with tree nodes. It can be built with a specified word or not.

    """

    def __init__(self, rootWord = None) -> None:
        with open("allowed_words.txt", "r") as f:
            self.guesses = list(f.read().upper().split())
        self.answers = self.guesses.copy()
        self.root = rootWord
        self.buildTree()
    
    def buildTree(self):
        if self.root is None:
            maxInfo = 0
            for word in self.answers:
                node = TreeNode(word, self.answers)
                info = node.expectedInfo
                if info > maxInfo:
                    maxInfo = info
                    self.root = node
        self.root.buildChildren(True)