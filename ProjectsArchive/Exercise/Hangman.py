import random
from tkinter import *
import Alphabet as alpha
import collections
from PIL import ImageTk, Image
import time
from tkinter import messagebox


root = Tk()

#Creating labels where the guessed letters will be displayed
lbl_list = []
def make_lbl(amount, x_inc):
    lbl_x_coord = 0
    for num in range(amount):
        lbl = Label(root, height=1, width=5)
        lbl.config(font=('Courier', 17))
        lbl.place(x=lbl_x_coord, y=450)
        lbl_list.append(lbl)
        lbl_x_coord += x_inc


lbl_lines_list = []
def make_lbl_lines(amount, x_inc):
    lbl_x_coord = 0
    for num in range(amount):
        lbl = Label(root, text='---', height=1, width=4)
        lbl.config(font=('Courier', 17))
        lbl.place(x=lbl_x_coord, y=480)
        lbl_lines_list.append(lbl)
        lbl_x_coord += x_inc


#getting images
img_list = []
def get_images():
    for itr in range(7):
        img = ImageTk.PhotoImage(Image.open(f'C:/Temp/hangman{itr}.png'))
        img_list.append(img)


indx = 50
def get_word():
    while True:
        word = random.choice(open("C:/Temp/WordBank.txt", 'r').read().splitlines())
        if ' ' not in word : return word.lower()



class App(Button):
    def __init__(self, root):
        super().__init__()
        self.root = root


    def make_btn(self, text, height, width):
        button = Button(self.root, text=text, command=lambda : on_click(button), height=height, width=width)
        return button

    @staticmethod
    def draw_guessed_inpt():
        gen_indcs = []
        for itr, letter in enumerate(word):
            if letter == txt:
                gen_indcs.append(itr)

        #place the guessed right char at the right label
        for indx in gen_indcs:
            if indx == 0:
                lbl_list[0]['text'] = txt
            elif indx == 1:
                lbl_list[1]['text'] = txt
            elif indx == 2:
                lbl_list[2]['text'] = txt
            elif indx == 3:
                lbl_list[3]['text'] = txt
            elif indx == 4:
                lbl_list[4]['text'] = txt
            elif indx == 5:
                lbl_list[5]['text'] = txt
            elif indx == 6:
                lbl_list[6]['text'] = txt
            elif indx == 7:
                lbl_list[7]['text'] = txt
            elif indx == 8:
                lbl_list[8]['text'] = txt
            elif indx == 9:
                lbl_list[9]['text'] = txt
            elif indx == 10:
                lbl_list[10]['text'] = txt
            elif indx == 11:
                lbl_list[11]['text'] = txt
            elif indx == 12:
                lbl_list[12]['text'] = txt
            elif indx == 13:
                lbl_list[13]['text'] = txt
            elif indx == 14:
                lbl_list[14]['text'] = txt
            elif indx == 15:
                lbl_list[15]['text'] = txt


#check wether the word and the correct_letters list are the same no matter the sorting
def is_same_word():
    if collections.Counter(word) == collections.Counter(correct_letters):
        exit_application()


def exit_application():
    msg_box = messagebox.askquestion('Exit Application', 'Do you want to exit the application?')
    if msg_box == 'yes':
        root.destroy()
    else:
        [element.destroy() for element in btn_list]
        [element.destroy() for element in lbl_list]
        [element.destroy() for element in lbl_lines_list]
        lbl_list.clear()
        btn_list.clear()
        lbl_lines_list.clear()

        main()


def on_click(btn):
    global tries, txt
    #check if btn text in word if so: destroy button and add it to label
    txt = btn['text']
    if txt in word:
        btn.destroy()

        for i in range(word.count(txt)):
            correct_letters.append(txt)
        App.draw_guessed_inpt()
        is_same_word()
    else:
        btn.destroy()

        #draw hangman
        if tries == 6:
            panel = Label(root, height=350, width=450, image=img_list[1])
            panel.place(x=425, y=60)
        elif tries == 5:
            panel = Label(root, height=350, width=450, image=img_list[2])
            panel.place(x=425, y=60)
        elif tries == 4:
            panel = Label(root, height=350, width=450, image=img_list[3])
            panel.place(x=425, y=60)
        elif tries == 3:
            panel = Label(root, height=350, width=450, image=img_list[4])
            panel.place(x=425, y=60)
        elif tries == 2:
            panel = Label(root, height=350, width=450, image=img_list[5])
            panel.place(x=425, y=60)
        elif tries == 1:
            panel = Label(root, height=350, width=450, image=img_list[6])
            panel.place(x=425, y=60)
            time.sleep(2)
            root.destroy()

        tries -= 1
        if tries == 0 : print('Failed')


def initialize():
    global btn_list
    program = App(root)

    # App.draw_hangman()
    panel = Label(root, height=350, width=450, image=img_list[0])
    panel.place(x=425, y=60)

    #create all buttons :)
    btn_x_coord = 0
    btn_list = []
    for char in alpha.getLower():
        btn = App.make_btn(program, char, 2, 5)
        btn.pack()
        btn.place(x=btn_x_coord, y=10)
        btn_list.append(btn)
        btn_x_coord += 50

    #Set location and size of window and initialize it
    root.geometry('1295x500+10+10')
    root.mainloop()


#initialize everything
def main():
    while True:
        global word, correct_letters, tries
        word = get_word()
        make_lbl(len(word), 50)
        make_lbl_lines(len(word), 50)
        print(word)
        correct_letters = []
        tries = 6
        get_images()
        initialize()


main()
