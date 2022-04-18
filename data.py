from copy import deepcopy, copy
from colorama import init, Fore
import numpy as np
import itertools as it
import os


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
    """
    Data initializer that sets up the list of words we can guess, the list of possible answers, and the true answer of 
    the game instance. It also initializes the dictionary that holds the patterns between all possible pairs of
    allowed guesses. 

    Parameters:

    answer : the true answer of the game instance for which this Data instance is managing the data.

    allowed : the list of words that we are allowed to guess. Note that if no list is passed in this uses the original 
    Wordle guess list before the NYT buyout.

    possible : the list of words that could possible be the answer. Note that if no list is passed in then this is the
    same as the guess list since the algorithms assume that any possible guess could be the answer.
    """
    def __init__(self, answer = None, allowed = None, possible = None):
        if not allowed:
            with open(WORD_FILE, "r") as f:
                allowed = list(f.read().upper().split())
        if not possible:
            possible = deepcopy(allowed)
        self.allowed = allowed
        self.possible = possible
        self.trueAnswer = answer
        self.patterns = dict()


    def processInput(self, guess, pattern):
        if not isinstance(pattern, int):
            pattern = self.stringToPattern(pattern)
        self.possible = self.getPossibleWords(guess, pattern, self.possible)


    def processGuess(self, guess):
        """
        This function processes a guess by getting its numeric pattern, converting that to the string displayed in the
        terminal, updating all of the data given this guess, and returning the string to be displayed in the terminal.

        Parameters:

        guess : the word that was guessed by the player or simulator.

        Returns:

        string : the guess but with appropriate colors added to the letters.
        """
        pattern = self.getPattern(guess, self.trueAnswer)
        string = self.patternToString(pattern, guess)
        self.possible = self.getPossibleWords(guess, pattern, self.possible)
        return string
        

    def giveNextGuess(self):
        """
        This function returns what is the next best guess based on the metric of expected information gain from
        guessing that word.

        Returns:

        nextGuess : the word with the highest expected information gain.

        """
        # If there is 2 or less possible answers just return the first one.
        if len(self.possible) < 3:
            nextGuess = self.possible[0]
        else:
            C = self.getPatternProbs(self.allowed, self.possible)
            C[C==0.0] = 1.0
            E = (-C*np.log2(C)).sum(1)
            nextGuess = self.allowed[np.argmax(E)]
        return nextGuess


    def giveTop(self, number):
        """
        This function returns a number of top guesses based on expected information gain.

        Parameters:

        number : the number of top guesses that should be returned

        Returns:

        top : the list of top number of guesses, their expected information gains, the variance in the expectation and
              the probability that the guess is the answer.
        """
        # If there is 2 or less possible answers those are the top guesses
        if len(self.possible) == 1:
            top = [(self.possible[0], 0.0, 0.0, 1.0)]
        elif len(self.possible) == 2:
            top = [(self.possible[0], 1.0,0.0, 0.5), (self.possible[1], 1.0,0.0, 0.5)]
        else:
            # Perform information gain calculations

            # Get the probability of each possible answer
            probs = {p : 1 / len(self.possible) for p in self.possible}

            # Get the probabilities of all possible patterns we could see for each guess
            C = self.getPatternProbs(self.allowed, self.possible)

            # Mask the zeros with 1s so we may take log base 2 of the matrix
            C[C==0.0] = 1.0
            logC = -np.log2(C)

            # This matrix holds expected information gain for each word
            E = (C * logC).sum(1)

            # Reshaped version of info matrix to perform variance calculation

            # Variance calculation
            V = (C * logC * logC).sum(1) - (E * E)

            # Get the number of words with the highest expected information gain
            ind = np.argsort(E)[-number:]

            # Build the top matrix
            top = []
            for i in ind:
                top.insert(0, (self.allowed[i], E[i], V[i], probs.get(self.allowed[i], 0.0)))
        return top


    def copy(self):
        """
        This function returns a copy of this data instance. Note that the answer, allowed guesses, and possible answers
        are all the same for this copy.
        """
        return Data(copy(self.trueAnswer), deepcopy(self.allowed), deepcopy(self.possible))
    

    """
    The following functions come from https://github.com/3b1b/videos/blob/master/_2022/wordle/simulations.py
    It follows the code from Grant Sanderson (3Blue1Brown) and includes some changes to suit my needs. Note I attempted
    to code these functions entirely on my own, however, my implementations were entirely impractical due to time and
    memory complexity. Thus, I enlisted the help of the legend.
    """


    def wordsToArrays(self, words):
        """
        This function converts a list of n strings (words) into a n x 5 NumPy array where the entry in the ith row and 
        jth column is the ordinal number associated with the jth character in the ith word in the list.

        Parameters:

        words : the list of strings

        Returns:

        array : the n x 5 array with rows representing a word transformed into their ordinal numbers for each character
        """
        return np.array([[ord(c) for c in w] for w in words], dtype=np.uint8)
    
    
    def patternMatrix(self, words1, words2):
        """
        This function takes two lists of words and builds their associated pattern matrix. A pattern matrix refers to a
        matrix of patterns in which the entry in the ith row and jth column is the pattern that would be seen if we
        guessed the ith word in the list words1 and the answer was the jth word in the list words2.

        Parameters:

        words1 : the first list of words

        words2 : the second list of words

        Returns:

        matrix : the pattern matrix associated with the input word lists
        """

        # build n x 5 arrays where each word is decomposed into ordinal numbers of its characters
        array1, array2 = map(self.wordsToArrays, (words1, words2))

        # this 4-D matrix will hold where words have the same character
        equality = np.zeros((len(words1), len(words2), 5, 5), dtype=bool)

        # equality[a,b,i,j] = True iff array1[a][i] = array2[b][j]
        for i, j in it.product(range(5), range(5)):
            equality[:, :, i, j] = np.equal.outer(array1[:,i], array2[:,j])

        # create 3-D array to hold patterns
        patterns = np.zeros((len(array1), len(array2), 5), dtype=np.uint8)

        # Find the characters that need to be colored GREEN(2) first
        for i in range(5):
            # matches is True where patterns should be GREEN(2)
            matches = equality[:, :, i, i].flatten()
            patterns[:,:,i].flat[matches] = GREEN

            # GREEN (2) letters have been matched and do not need to be matched to possible YELLOW(1) letters
            for k in range(5):
                equality[:,:,k,i].flat[matches] = False
                equality[:,:,i,k].flat[matches] = False

        # Find characters that need to be YELLOW (1) and everything else can just be GREY (0)
        for i, j in it.product(range(5), range(5)):
            matches = equality[:,:,i,j].flatten()
            patterns[:,:,i].flat[matches] = YELLOW
            for k in range(5):
                equality[:, :, i, k].flat[matches] = False
                equality[:, :, k, j].flat[matches] = False

        # Here comes the real magic. Note that as of right now our patterns matrix is a 3-D matrix where patterns[i, j]
        # is a list of length 5 of 0s, 1s, or 2s representing the pattern between the ith word in words1 as a guess and
        # the jth word in words2 as the answer. Note that we can concatenate these together to get a ternary number
        # whose decimal representation is unique. Thus, we can represent the 3^5 possible patterns using decimal 
        # numbers 0 to 242. Thus, we do the dot product between our patterns matrix and the vector of powers of three
        # from 3^0 to 3^4.
        matrix = np.dot(patterns, (3**np.arange(5)).astype(np.uint8))
        return matrix


    def getPatternMatrix(self, words1, words2):
        """
        This function takes two lists of words and retrieves their pattern matrix using the pattern matrix saved to the
        file. However, if this file does not exist the file must be created.

        Parameters:

        words1 : list of words that will be treated as guesses

        words2 : list of words that will be treated as possible answers

        Returns: 

        matrix : the pattern matrix in which the entry in the ith row and jth column is the pattern that would be seen 
                 if we guessed the ith word in the list words1 and the answer was the jth word in the list words2.
        """
        # If our patterns dictionary has not yet been filled
        if not self.patterns:

            # If the patterns file has note been created
            if not os.path.exists(PATTERN_FILE):

                # Create and save pattern matrix
                patterns = self.patternMatrix(self.allowed, self.allowed)
                np.save(PATTERN_FILE, patterns)
            
            # Fill patterns dictionary
            self.patterns["grid"] = np.load(PATTERN_FILE)
            self.patterns["wordsToIndex"] = dict(zip(self.allowed, it.count()))
        
        grid = self.patterns["grid"]
        wordsToIndex = self.patterns["wordsToIndex"]

        # Get the column and row indices for the words we actually need patterns for
        ind1 = [wordsToIndex[w] for w in words1]
        ind2 = [wordsToIndex[w] for w in words2]

        # Only take the patterns which are part of the rows and columns corresponding to the words in our lists
        matrix = grid[np.ix_(ind1, ind2)]
        return matrix


    def getPattern(self, guess, answer):
        """
        This function retrieves the pattern that would appear with the guess parameter as the guess and the answer
        parameter as the answer.

        Parameters:

        guess : the word that is being guessed

        answer : the word that is considered as the answer. Note this may not be the trueAnswer but is considered so to
                 build the pattern.

        Returns:

        pattern : the decimal number representing the pattern between the guess word and the answer word
        """
        pattern = self.patternMatrix([guess], [answer])[0,0]
        return pattern


    def stringToPattern(self, pattern_string):
        """
        This function takes in the ternary representation of a pattern as a string and converts it to its decimal
        representation.
        """
        return sum((3**i) * int(c) for i, c in enumerate(pattern_string))


    def patternToList(self, pattern):
        """
        This function takes in a decimal representation of a pattern and converts it into its ternary representation,
        but as a list of 0s, 1s, and 2s.
        """
        result = []
        curr = pattern
        for _ in range(5):
            result.append(curr % 3)
            curr = curr // 3
        return result    


    def patternToString(self, pattern, word):
        """
        This function takes in the decimal representation of a pattern as well as the word it is associated with and
        colors its characters based on the pattern passed in.
        """
        d = {GREY : Fore.BLACK, YELLOW : Fore.YELLOW, GREEN : Fore.GREEN}
        return "".join(d[c] + word[i] for i, c in enumerate(self.patternToList(pattern)))


    def patternsToString(self, patterns, words):
        """
        This function can join a series of patterns and their corresponding words in a line-by-line format like the
        Wordle game.
        """
        return "\n".join(map(self.patternToString, (patterns, words)))


    def getPossibleWords(self, guess, pattern, words):
        """
        This function cuts down a list of words based on the guess and its corresponding pattern. For example, if the
        words list contained a word with a character that was greyed out in the guess/pattern then this function will
        return a word list without this word.

        Parameters: 
        
        guess : the guess word

        pattern : the pattern given corresponding to the guess word

        words : the possible answer space that needs to be trimmed

        Returns:

        possible : the new possible answer space
        """
        all_patterns = self.getPatternMatrix([guess], words).flatten()
        possible = list(np.array(words)[all_patterns == pattern])
        return possible

    
    def getPatternProbs(self, allowed, possible):
        """
        This function returns a n x 243 matrix where n is the number of allowed guesses. The entry in the ith row and
        jth column of this matrix corresponds to the probability of seeing the pattern, whose decimal representation is
        given by j, when guessing the ith word in the allowed guesses list.
        """
        probs = [1.0 / len(possible) for _ in possible]
        patterns = self.getPatternMatrix(allowed, possible)
        counts = np.zeros((len(allowed), 243))
        for j, prob in enumerate(probs):
            counts[np.arange(len(allowed)), patterns[:, j]] += prob
        return counts