import os
from tkinter import *
from tkinter.filedialog import askdirectory
import subprocess
from shutil import move


class Application(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.geometry('300x200')

        Frame.__init__(self, self.root)


    def start(self):
        self.root.mainloop()



class Btn:
    def __init__(self, text, command, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.button = Button(app.root, text=text, command=command, height=height, width=width)

        self.button.pack()
        self.button.place(x=self.x, y=self.y)



class TxtBox:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.txtbox = Entry(app.root, width=40)
        self.txtbox.insert(0, text)

        self.txtbox.pack()
        self.txtbox.place(x=x, y=y)


    def updateLbl(self):
        self.txtbox.delete(0, END)
        self.txtbox.insert(0, path)


    def getTxt(self):
        return self.txtbox.get()


def makeLbl():
    global lblPath
    lblPath = TxtBox(text=path, x=50, y=50)


def pyinstallerCommand():
    print('hello')
    currdir = os.getcwd() + '//ExpenseTracker.py//'
    subprocess.call(f'pyinstaller -w C:/tmp/InstallerTest/ExpenseTracker.py')
    move(currdir, path)


def setDir():
    global path
    path = askdirectory() + '/'
    lblPath.updateLbl()


app = Application()

path = 'C:/Program Files (x86)/ExpenseTracker/'
dirBtn = Btn(text='Select Directory', command=setDir, x=75, y=10, height=2, width=20)
installBtn = Btn(text='Install', command=pyinstallerCommand, x=75, y=120, height=2, width=20)
lblPath = TxtBox(text=path, x=30, y=60)

app.start()
