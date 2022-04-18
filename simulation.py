import numpy as np
from game import ANSWER_FILE, Game
from tqdm import tqdm
from data import WORD_FILE, Data
import itertools as it
import random
import matplotlib.pyplot as plt
from colorama import init
from  matplotlib.colors import LinearSegmentedColormap


def letterDistributions():
    with open(WORD_FILE, 'r') as f:
        guessList = list(f.read().upper().split())
    
    letters = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    engFreq = np.array([0.082, 0.015, 0.027, 0.047, 0.13, 0.022, 0.02, 0.062, 0.069, 0.0016, 0.0081, 0.04, 0.027,
                        0.067, 0.078, 0.019, 0.0011, 0.059, 0.062, 0.096, 0.027, 0.0097, 0.024, 0.0015, 0.02, 0.00078])
    engInd = np.argsort(engFreq)[::-1]
    alphabet = dict(zip(letters, it.count()))
    heatMap = np.zeros((26,5))
    letterBuckets = np.zeros(26)
    for word in guessList:
        for i, l in enumerate(word):
            heatMap[alphabet[l]][i] += 1
            letterBuckets[alphabet[l]] += 1
    byLetter = heatMap / heatMap.sum(1).reshape(-1,1)
    byPosition = heatMap / heatMap.sum(0).reshape(1,-1)
    letterFreq = letterBuckets / letterBuckets.sum()
    wordleInd = np.argsort(letterFreq)[::-1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(letters[engInd], engFreq[engInd], color='green')
    plt.ylabel('Frequency')
    fig.tight_layout()
    plt.savefig("plots/engFreq", dpi=300, bbox_inches="tight")

    cmap=LinearSegmentedColormap.from_list('bg',["gold", "green"], N=256)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(byLetter, cmap=cmap)
    plt.colorbar(im)
    ax.set_xticks(np.arange(5), labels=[1,2,3,4,5])
    ax.set_yticks(np.arange(26), labels=letters)
    plt.setp(ax.get_xticklabels(), ha="center")
    ax.set_title("Letter Distributions Over Positions")
    fig.tight_layout()
    plt.savefig("plots/byLetter", dpi=300, bbox_inches="tight")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(byPosition, cmap=cmap)
    plt.colorbar(im)
    ax.set_xticks(np.arange(5), labels=[1,2,3,4,5])
    ax.set_yticks(np.arange(26), labels=letters)
    plt.setp(ax.get_xticklabels(), ha="center")
    ax.set_title("Position Distributions Over Letters")
    fig.tight_layout()
    plt.savefig("plots/byPostion", dpi=300, bbox_inches="tight")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.bar(letters[wordleInd], letterFreq[wordleInd], color='green')
    plt.ylabel('Frequency')
    fig.tight_layout()
    plt.savefig("plots/wordleFreq", dpi=300, bbox_inches="tight")
    

def simulateAll(guessList):
    dataStore = dict()
    dataStore["wordsToIndex"] = dict(zip(guessList, it.count()))
    dataStore["avg"] = [0 for _ in range(len(guessList))]
    dataStore["buckets"] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(guessList))]

    with open(ANSWER_FILE, "r") as f:
        answerList = random.sample(list(f.read().upper().split()), 250)
    
    for guess in guessList:
        guessBuckets = [0 for _ in range(10)]
        print(f"Start Word:{guess}")
        numerator = 0
        denominator = 0
        avg = 1
        for i in tqdm(range(len(answerList)), ncols=100, leave=True):
            answer = answerList[i]
            game = Game(answer)
            trial = game.simulate(guess)
            guessBuckets[trial - 1] += 1
            numerator += trial
            denominator += 1
            avg = numerator / denominator
        idx = dataStore["wordsToIndex"][guess]
        dataStore["avg"][idx] = avg
        dataStore["buckets"][idx] = guessBuckets
        print(f"Avg # of guesses to answer:{avg}")
    return dataStore

def buildPlots():
    with open(ANSWER_FILE, "r") as f:
        trueAnswerList = list(f.read().upper().split())
    # Plot first step entropies
    data = Data(answer=None, allowed=None, possible=trueAnswerList)
    topTen = data.giveTop(10)
    words, infos = [], []
    for i in range(10):
        word, info  = topTen[i][0], topTen[i][1]
        words.append(word)
        infos.append(info)
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    plt.bar(words, infos)
    plt.xlabel('Start Word')
    plt.ylabel('Expected bits of Information')
    for i, v in enumerate(infos):
        ax.text(i, v + 0.05, "%.2f" %v, ha="center")
    plt.savefig("plots/entropiesFirstStep")
    # Plot second step entropies
    secondSteps = []
    for word, stepOne in zip(words, infos):
        patternProbs = data.getPatternProbs([word], data.possible).flatten()
        for i in range(242):
            patternProb = patternProbs[i]
            thisData = data.copy()
            thisData.processInput(word, i)
            topGuess = thisData.giveTop(1)
            stepOne += patternProb * topGuess[0][1]
        secondSteps.append(stepOne)
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    plt.bar(words, secondSteps)
    plt.xlabel('Start Word')
    plt.ylabel('Expected bits after second guess')
    for i, v in enumerate(secondSteps):
        ax.text(i, v + 0.05, "%.2f" %v, ha="center")
    plt.savefig("plots/entropiesSecondStep")
    # Make selection of good words
    selection = ["TARES", "SLATE", "SALET", "SOARE", "ARISE", "ADIEU", "CRANE", "TRACE", "CRATE"]

    # Simulate these and plot their histograms and display their averages
