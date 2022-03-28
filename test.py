import unittest

from game import Game
from data import Data
from pattern import Pattern
from colorama import Fore, init
from copy import deepcopy
from util import *
import random

from util import buildRandList, listMinus

init(autoreset=True)

class TestPattern(unittest.TestCase):
    """
    Unit Test for the initializing method for Pattern class.

    We initialize one of the data objects with the answer
    set to CHEST. We then initialize an instance of Pattern 
    using this data object and a guess of SLATE. It should be
    that the pattern has the S, T, and E yellow ("Y") and the 
    rest should be grey ("b").
    """
    def test_initializer_1(self):
        testWord = "SLATE"
        testAnswer = "CHEST"
        testPattern = ("Y", "b", "b", "Y", "Y")
        testString = Fore.YELLOW + "S" + Fore.BLACK + "L" + Fore.BLACK + "A" + Fore.YELLOW + "T" + Fore.YELLOW + "E"

        pattern = Pattern("SLATE", "CHEST")

        self.assertEqual(testWord, pattern.word)
        self.assertEqual(testAnswer, pattern.answer)
        self.assertEqual(testPattern, pattern.pattern)
        self.assertEqual(testString, pattern.string)

    def test_initializer_2(self):
        testWord = "FREED"
        testAnswer = "SEAMS"
        testPattern = ("b", "b", "Y", "b", "b")
        testString = Fore.BLACK + "F" + Fore.BLACK + "R" + Fore.YELLOW + "E" + Fore.BLACK + "E" + Fore.BLACK + "D"

        pattern = Pattern("FREED", "SEAMS")

        self.assertEqual(testWord, pattern.word)
        self.assertEqual(testAnswer, pattern.answer)
        self.assertEqual(testPattern, pattern.pattern)
        self.assertEqual(testString, pattern.string)

    def test_initializer_3(self):
        testWord = "CRETE"
        testAnswer = "CREED"
        testPattern = ("G", "G", "G", "b", "Y")
        testString = Fore.GREEN + "C" + Fore.GREEN + "R" + Fore.GREEN + "E" + Fore.BLACK + "T" + Fore.YELLOW + "E"

        pattern = Pattern("CRETE", "CREED")

        self.assertEqual(testWord, pattern.word)
        self.assertEqual(testAnswer, pattern.answer)
        self.assertEqual(testPattern, pattern.pattern)
        self.assertEqual(testString, pattern.string)

    def test_initializer_4(self):
        testWord = "SCOOT"
        testAnswer = "ROTOR"
        testPattern = ("b", "b", "Y", "G", "Y")
        testString = Fore.BLACK + "S" + Fore.BLACK + "C" + Fore.YELLOW + "O" + Fore.GREEN + "O" + Fore.YELLOW + "T"

        pattern = Pattern("SCOOT", "ROTOR")

        self.assertEqual(testWord, pattern.word)
        self.assertEqual(testAnswer, pattern.answer)
        self.assertEqual(testPattern, pattern.pattern)
        self.assertEqual(testString, pattern.string)

    def test_violate_1(self):
        # Guess = "SLATE"
        # Answer = "CHEST"
        # Pattern = ("Y", "b", "b", "Y", "Y")
        # input = ["SHTIK", "HOMIE", "DEPOT", "MANOR", "ALONE", "SNOOT", "SLATE", 
        #          "CHEST", "BEACH", "FOCUS", "MEDIA", "PENIS", "TITTY", "PUBES"]
        testViolates = ["SHTIK", "MANOR", "ALONE", "SNOOT", "SLATE", "BEACH", "MEDIA",
                        "TITTY"]

        pattern = Pattern("SLATE", "CHEST")
        testViolate = True
        for word in testViolates:
            testViolate = testViolate and pattern.violate(word)
        self.assertEqual(testViolate, True)
    
    def test_violate_2(self):
        # Guess = "FREED"
        # Answer = "SEAMS"
        # Pattern = ("b", "b", "Y", "b", "b")
        # input = ["WHORE", "SLUTS", "BEGIN", "MANOR", "CHEWY", "INDIA", "SLATE", 
        #          "CHEST", "FRONT", "FOCUS", "RIGHT", "PENIS", "CLOSE", "NIGER"]
        testViolates = ["WHORE", "MANOR", "CHEWY", "INDIA", "CHEST", "FRONT", "FOCUS", 
                        "RIGHT", "NIGER"]

        pattern = Pattern("FREED", "SEAMS")
        testViolate = True
        for word in testViolates:
            testViolate = testViolate and pattern.violate(word)
        self.assertEqual(testViolate, True)

    def test_violate_3(self):
        # Guess = "CRETE"
        # Answer = "CREED"
        # Pattern = ("G", "G", "G", "b", "Y")
        # input = ["WHORE", "SLUTS", "BEGIN", "MANOR", "CHEWY", "INDIA", "SLATE", 
        #          "CHEST", "FRONT", "FOCUS", "RIGHT", "PENIS", "CLOSE", "NIGER"]
        testViolates = ["WHORE", "SLUTS", "CHEST", "SLATE", "FRONT", "RIGHT", 
                        "CLOSE"]

        pattern = Pattern("CRETE", "CREED")
        testViolate = True
        for word in testViolates:
            testViolate = testViolate and pattern.violate(word)
        self.assertEqual(testViolate, True)

    def test_match_1(self):
        # Guess = "CRETE"
        # Answer = "CREED"
        # Pattern = ("G", "G", "G", "b", "Y")
        # input = ["CREPE", "CREEP", "CREED", "CRETE", "CREEK", "INDIA", "SLATE", 
        #          "CHEST", "FRONT", "FOCUS", "RIGHT", "PENIS", "CLOSE", "NIGER"]
        testMatches = ["CREEP", "CREED", "CREEK"]

        pattern = Pattern("CRETE", "CREED")
        testMatch = True
        for word in testMatches:
            testMatch = testMatch and pattern.match(word)
        self.assertEqual(testMatch, True)

    def test_match_2(self):
        # Guess = "SLATE"
        # Answer = "LATCH"
        # Pattern = ("b", "Y", "Y", "Y", "b")
        # input = ["SLATE", "LATCH", "HATCH", "MATCH", "CATCH", "LATIN", "LATHI", 
        #          "SOARE", "SMITE", "SAUCE", "LATHY", "PENIS", "CLOSE", "NIGER"]
        testMatches = ["LATCH", "LATIN", "LATHI", "LATHY"]

        pattern = Pattern("SLATE", "LATCH")
        testMatch = True
        for word in testMatches:
            testMatch = testMatch and pattern.match(word)
        self.assertEqual(testMatch, True)




        

class TestData(unittest.TestCase):
    def test_initData_1(self):
        inputList = buildRandList(5000)
        inputG1 = random.choice(inputList)
        inputG2 = random.choice(inputList)
        inputG3 = random.choice(inputList)
        inputA = random.choice(inputList)
        data = Data(inputA, inputList, inputList)
        
        pattern1 = Pattern(inputG1, inputA)
        print(pattern1.string)
        data.guessToString(inputG1)

        testGuesses = True
        testAnswers = True
        flag = True
        for word in data.guesses:
            testGuesses = testGuesses and not pattern1.violate(word)
            if not testGuesses and flag:
                print(f"Violating word:{word}")
                flag = False
        flag = True
        for word in listMinus(inputList, data.guesses):
            testGuesses = testGuesses and pattern1.violate(word)
            if not testGuesses and flag:
                print(f"Non-violating word:{word}")
                flag = False
        flag = True
        for word in data.answers:
            testAnswers = testAnswers and pattern1.match(word)
            if not testAnswers and flag:
                print(f"Non-matching word:{word}")
                flag = False
        flag = True
        for word in listMinus(inputList, data.answers):
            testAnswers = testAnswers and not pattern1.match(word)
            if not testAnswers and flag:
                print(f"Matching word:{word}")
                flag = False

        oldGuesses = data.guesses
        oldAnswers = data.answers
        pattern2 = Pattern(inputG2, inputA)
        print(pattern2.string)
        data.guessToString(inputG2)
        flag = True
        for word in data.guesses:
            testGuesses = testGuesses and not pattern2.violate(word)
            if not testGuesses and flag:
                print(f"Violating word:{word}")
                flag = False
        flag = True
        for word in listMinus(oldGuesses, data.guesses):
            testGuesses = testGuesses and pattern2.violate(word)
            if not testGuesses and flag:
                print(f"Non-violating word:{word}")
                flag = False
        flag = True
        for word in data.answers:
            testAnswers = testAnswers and pattern2.match(word)
            if not testAnswers and flag:
                print(f"Non-matching word:{word}")
                flag = False
        flag = True
        for word in listMinus(oldAnswers, data.answers):
            testAnswers = testAnswers and not pattern2.match(word)
            if not testAnswers and flag:
                print(f"Matching word:{word}")
                flag = False

        oldGuesses = data.guesses
        oldAnswers = data.answers
        pattern3 = Pattern(inputG3, inputA)
        print(pattern3.string)
        data.guessToString(inputG3)
        flag = True
        for word in data.guesses:
            testGuesses = testGuesses and not pattern3.violate(word)
            if not testGuesses and flag:
                print(f"Violating word:{word}")
                flag = False
        flag = True
        for word in listMinus(oldGuesses, data.guesses):
            testGuesses = testGuesses and pattern3.violate(word)
            if not testGuesses and flag:
                print(f"Non-violating word:{word}")
                flag = False
        flag = True
        for word in data.answers:
            testAnswers = testAnswers and pattern3.match(word)
            if not testAnswers and flag:
                print(f"Non-matching word:{word}")
                flag = False
        flag = True
        for word in listMinus(oldAnswers, data.answers):
            testAnswers = testAnswers and not pattern3.match(word)
            if not testAnswers and flag:
                print(f"Matching word:{word}")
                flag = False
        self.assertEqual(testGuesses, True)
        self.assertEqual(testAnswers, True)

if __name__ == '__main__':
    unittest.main()