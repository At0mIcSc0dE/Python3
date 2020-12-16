from tkinter import *
import collections
import random
import Alphabet as alpha

root = Tk()


def getWord():
    while True:
        # word = random.choice(open('C:/Temp/WordBank.txt', 'r').read().splitlines())
        # if ' ' not in word : return word
        return 'hello'


def genLbl(root, amount, x_inc):
    x_coord = 0
    lbl_list = []
    for itr in range(amount):
        lbl = Label(root, height=1, width=5)
        lbl.config(font=('Courier', 17))
        lbl.place(x=x_coord, y=450)
        lbl_list.append(lbl)
        x_coord += x_inc
    return lbl_list


def makeBtn(root, text, height, width):
    button = Button(root, text=text, command=lambda : onClick(button, 6), height=height, width=width)
    return button


def genBtn(root, x_inc):
    btn_x_coord = 0
    btn_list = []
    for char in alpha.getUpper():
        btn = makeBtn(root, char, 2, 5)
        btn.place(x=btn_x_coord, y=10)
        btn_list.append(btn)
        btn_x_coord += x_inc
    return btn_list


def isSameWord(word, correct_letters):
    if collections.Counter(word) == collections.Counter(correct_letters) : exit(), print('Done')


def onClick(btn, tries):
    text = btn['text']
    print(text)
    if text in word:
        btn.destroy()
        for char in range(word.count(text)):
            correct_letters.append(char)
        isSameWord(word, correct_letters)
    else:
        btn.destroy()



def main():
    global word, correct_letters
    correct_letters = []
    root.geometry('1295x500+10+10')
    word = getWord().upper()
    print(word)
    lbl_list = genLbl(root, len(word), 50)
    btn_list = genBtn(root, 50)
    root.mainloop()



main()
