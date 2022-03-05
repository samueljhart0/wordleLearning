"""
Utility file for storing functions for project
"""

from ast import For
from colorama import init, Fore, Back

def create_dict(list) -> dict[str, bool]:
    dict = {}
    for x in list:
        dict[x] = True
    return dict

def printAsKeyboard(dict) -> None:
    firstRow  = "Q W E R T Y U I O P "
    secondRow = " A S D F G H J K L  "
    thirdRow  = "  Z X C V B N M     "
    for f in firstRow:
        if f == " ":
            continue
        else:
            info = dict[f]
            if info == "b":
                firstRow = firstRow.replace(f"{f} ", Fore.BLACK + "  ")
            elif info == "G":
                firstRow = firstRow.replace(f"{f} ", Fore.GREEN + f"{f} ")
            elif info == "Y":
                firstRow = firstRow.replace(f"{f} ", Fore.YELLOW + f"{f} ")
            elif info == "B":
                firstRow = firstRow.replace(f"{f} ", Fore.BLACK + f"{f} ")
    for s in secondRow:
        if s == " ":
            continue
        else:
            info = dict[s]
            if info == "b":
                secondRow = secondRow.replace(f"{s} ", Fore.BLACK + "  ")
            elif info == "G":
                secondRow = secondRow.replace(f"{s} ", Fore.GREEN + f"{s} ")
            elif info == "Y":
                secondRow = secondRow.replace(f"{s} ", Fore.YELLOW + f"{s} ")
            elif info == "B":
                secondRow = secondRow.replace(f"{s} ", Fore.BLACK + f"{s} ")
    for t in thirdRow:
        if t == " ":
            continue
        else:
            info = dict[t]
            if info == "b":
                thirdRow = thirdRow.replace(f"{t} ", "  ")
            elif info == "G":
                thirdRow = thirdRow.replace(f"{t} ", Fore.GREEN + f"{t} ")
            elif info == "Y":
                thirdRow = thirdRow.replace(f"{t} ", Fore.YELLOW + f"{t} ")
            elif info == "B":
                thirdRow = thirdRow.replace(f"{t} ", Fore.BLACK + f"{t} ")     
    print(f"{firstRow}\n{secondRow}\n{thirdRow}")