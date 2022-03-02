"""
Utility file for storing functions for project
"""

def create_dict(list) -> dict[str, bool]:
    dict = {}
    for x in list:
        dict[x] = True
    return dict

def printAsKeyboard(dict) -> None:
    firstRow  = "Q W E R T Y U I O P "
    secondRow = " A S D F G H J K L  "
    thirdRow  = "  Z X C V B N M     "
    for pair in dict.items():
        letter, info = pair
        if info == "":
            continue
        i = firstRow.find(letter)
        if i < 0:
            i = secondRow.find(letter)
            if i < 0:
                i = thirdRow.find(letter)
                if info == " ":
                    thirdRow = thirdRow.replace(f"{letter} ", "  ")
                else:
                    thirdRow = thirdRow.replace(f"{letter} ", f"{letter}{info}")
            else:
                if info == " ":
                    secondRow = secondRow.replace(f"{letter} ", "  ")
                else:
                    secondRow = secondRow.replace(f"{letter} ", f"{letter}{info}")
        else:
            if info == " ":
                firstRow = firstRow.replace(f"{letter} ", "  ")
            else:
                firstRow = firstRow.replace(f"{letter} ", f"{letter}{info}")
    print(f"{firstRow}\n{secondRow}\n{thirdRow}")