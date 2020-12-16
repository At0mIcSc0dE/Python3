"""
This programm will allow you to enter your monthly budget. Every expense will be stored and removed from it.
You will be able to show a graph showing if your expenses increased or decreased (30 days, 12 months).
The GUI will have a list of all of your expenses on the left, to which you can add using a text box right next to it.
You will also be able to enter monthly expenses that are always the same so these will be automatically subtracted from
your budget.
All of this will be stored in a databasein the chosen directory, which you will be able to select
when you first open the program. I will also add a way to change the path and move all files from the previous one
to the newer one.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from os import execl, mkdir
from os.path import exists
from shutil import move
from time import time
from datetime import datetime
from sqlite3 import connect
from matplotlib.pyplot import plot, legend, title, xlabel, ylabel, show
from concurrent.futures import ThreadPoolExecutor
from string import ascii_lowercase, ascii_uppercase

global budget, path, expenseDtbPath
DEFAULTFONT = 'MS Shell Dlg 2'
DEFAULTPLAINTEXT = 'Write more info about your expense here...'


class MainWindow:
    def __init__(self, mainWindowTitle: str = 'MainWindow',
                 appl: QtWidgets.QApplication = None, minsizeX: int = 0, minsizeY: int = 0,
                 maxsizeX: int = 1920, maxsizeY: int = 1080):
        self.app = appl
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle(mainWindowTitle)
        self.win.setMinimumSize(QtCore.QSize(minsizeX, minsizeY))
        self.win.setMaximumSize(QtCore.QSize(maxsizeX, maxsizeY))

    def resize(self, x, y):
        self.win.resize(x, y)


class Editor(object):
    """The editor to edit the selected entry"""

    def __init__(self, editWindowTitle: str = 'MainWindow'):
        super().__init__()
        self.editWin = QtWidgets.QMainWindow()
        self.editWin.setWindowTitle(editWindowTitle)
        self.setupUi(self.editWin)

    def setupUi(self, main):

        """Sets up the editor ui"""

        main.setWindowTitle('Editor')
        main.setObjectName("main")
        main.setMaximumSize(800, 400)
        main.setMinimumSize(800, 400)
        main.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 70, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(300, 70, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main)
        self.statusbar.setObjectName("statusbar")
        main.setStatusBar(self.statusbar)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "MainWindow"))
        self.label.setText(_translate("main", "Expense name"))
        self.label_2.setText(_translate("main", "Expense price"))

    def apply(self, selectionOnce: int, selectionMonth: int, name: str, price: float, info: str) -> callable:

        """Constructor, takes your selection, and the text of the textbox elements!
            Has a wrapper function"""

        def wrapper(*args, **kwargs):
            if args[0] != -1 or selectionOnce != -1:
                lstbox.update(selectionOnce, name, price)
                dtbOnce.update(selectionOnce, name, price, info)
                lblNetto.text = f'Your remaining budget: {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'
                self.editWin.destroy()
            elif selectionMonth != -1 or args[1] != -1:
                lstboxMonth.update(selectionMonth, name, price)
                dtbMonth.update(selectionMonth, name, price, info)
                lblNetto.text = f'Your remaining budget: {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'
                self.editWin.destroy()

        return wrapper

    def close(self):

        """Closes the editwindow"""

        self.editWin.destroy()

    def show(self):
        self.editWin.show()


class DataBase:
    """Database class, no inheritance"""

    def __init__(self, databasePath: str, table: str):

        """Will create table if it does not exist.
        Args: your databasePath and the name of your table"""

        self.table = table
        self.conn = connect(databasePath)
        self.cursor = self.conn.cursor()

        self.cursor.execute('CREATE TABLE IF NOT EXISTS ' + self.table + '''(
                            ID INTEGER,
                            Expense TEXT,
                            Price INTEGER,
                            MoreInfo TEXT,
                            Day INTEGER,
                            Month INTEGER,
                            Year INTEGER,
                            PRIMARY KEY(ID)
                            )''')

    def getRowValuesById(self, rowid: int, *elemIndex: int):

        """Enter the ID by which the record is stored and the function will return you a list if you want multiple elements
        of one record or it will return the entire row if no elemIndex given."""

        self.cursor.execute('SELECT ID FROM ' + self.table)
        rws = self.cursor.fetchall()
        rws = rws[::-1]
        r = rws[rowid][0]
        self.cursor.execute('SELECT * FROM ' + self.table + ' WHERE ID = ?', (r,))
        row = self.cursor.fetchall()
        returns = []
        for arg in elemIndex:
            returns.append(row[0][arg])
        return returns if returns != [] else row[0]

    def getAllRecords(self):
        self.cursor.execute('SELECT * FROM ' + self.table)
        return self.cursor.fetchall()

    def dataEntry(self, price: float, expTime: str, exp: str, moreInfo: str = None):

        """Enters data into a database
        ExpTime argument: 'once', 'month' to specify to which database you want to add"""

        day, month, year = str(datetime.fromtimestamp(time()).strftime('%d-%m-%Y')).split('-')
        if expTime == 'once':
            self.cursor.execute(
                'INSERT INTO ' + self.table + ' (Expense, Price, MoreInfo, Day, Month, Year) VALUES (?, ?, ?, ?, ?, ?)',
                (exp, price, moreInfo.rstrip('\n').strip(DEFAULTPLAINTEXT), day, month, year))
            self.conn.commit()
        elif expTime == 'month':
            self.cursor.execute(
                'INSERT INTO ' + self.table + ' (Expense, Price, MoreInfo, Day, Month, Year) VALUES (?, ?, ?, ?, ?, ?)',
                (exp, price, moreInfo.rstrip('\n').strip(DEFAULTPLAINTEXT), day, month, year))
            self.conn.commit()
        else:
            raise ValueError

    def clearDtb(self):

        """Clears the database of all records. Also updates labels"""

        self.cursor.execute('DELETE FROM ' + self.table)
        self.conn.commit()

    def removeFromDtb(self, currselect: int):

        """Removes item with the reversed rowid from listbox"""

        self.cursor.execute('SELECT ID FROM ' + self.table)
        rws = self.cursor.fetchall()
        rws = rws[::-1]
        rw = rws[currselect]
        self.cursor.execute('DELETE FROM ' + self.table + ' WHERE ID = ?', (str(rw[0]),))
        self.conn.commit()
        self.updateId()

    def updateId(self):

        """Updates IDs because if you delete ID=1 ID=2 will then be the first element in the dtb"""

        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = self.cursor.fetchall()

        r = []
        for row in range(len(rows)):
            r.append(row + 1)
        with ThreadPoolExecutor() as executor:
            executor.map(self._update, r, rows)

    def _update(self, index: list, row: list):
        self.cursor.execute('UPDATE ' + self.table + ' SET ID = ? WHERE ID = ?', (index[0], row[0]))
        self.conn.commit()

    def cal(self):

        """Calculation of totalExpenses"""

        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.setWindowTitle('Invalid Input')
        msgbox.setText('Invalid Input, try again!')
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        self.cursor.execute('SELECT Price FROM ' + self.table)
        expenses = self.cursor.fetchall()
        totalExpense = 0
        for expense in expenses:
            while True:
                try:
                    expense = str(expense[0])
                    for L, l in zip(ascii_uppercase, ascii_lowercase):
                        expense = expense.strip(L)
                        expense = expense.strip(l)
                    totalExpense += float(expense)
                    break
                except ValueError:
                    msgbox.show()
        return totalExpense

    def readFromDtb(self):

        """Reads Expense, Price, MoreInfo from Database"""

        self.cursor.execute('SELECT Expense, Price, MoreInfo FROM ' + self.table)
        return self.cursor.fetchall()

    def update(self, rowid: int, name: str, price: float, moreInfo: str):

        """Updates one record with the rowid and replaces the name, price and moreInfo with the passed parameters"""

        self.cursor.execute('SELECT ID FROM ' + self.table)
        ids = self.cursor.fetchall()
        ids = ids[::-1]
        ids = ids[rowid][0]
        self.cursor.execute('UPDATE ' + self.table + ' SET Expense = ?, Price = ?, MoreInfo = ? WHERE ID = ?',
                            (name, price, moreInfo, ids))
        self.conn.commit()


class Button(QtWidgets.QPushButton):
    """Simplyfied button class for PyQt5.QtWindgets.QPushButton"""

    def __init__(self, win: QtWidgets.QMainWindow, text: str = None, x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23, font: str = 'MS Shell Dlg 2', fontsize: int = 8,
                 command: callable = None, key: str = '') -> None:
        super().__init__()

        self._text = text
        self.command = command
        self.button = QtWidgets.QPushButton(win)
        self.button.setGeometry(QtCore.QRect(x, y, width, height))
        self.button.setText(self.text)
        if self.command:
            self.button.clicked.connect(self.command)
        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.button.setFont(self.font)
        self.dialogs = []

        if key != '':
            self.button.setShortcut(key)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value
        self.button.setText(self._text)


class TextBox(QtWidgets.QLineEdit):
    """Simplified class of PyQt5.QtWidgets.QLineEdit TextBox"""

    def __init__(self, win: QtWidgets.QMainWindow, text: str = '', x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8) -> None:
        super().__init__()
        self._text = text
        self.textbox = QtWidgets.QLineEdit(win)
        self.textbox.setGeometry(QtCore.QRect(x, y, width, height))
        self.textbox.setText(self.text)
        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(fontsize)
        self.textbox.setFont(self.font)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self.textbox.setText(value)

    def getText(self) -> str:
        """:returns the current text of a QLineEdit"""

        return str(self.textbox.text())


def pr():
    print('hello')


class ListBox(QtWidgets.QListWidget, QtWidgets.QWidget):
    """Simplified class for PyQt5.QtWidgets.QListWidget ListBox"""

    def __init__(self, win: QtWidgets.QMainWindow, x: int = 0, y: int = 0, width: int = 75, height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8) -> None:
        QtWidgets.QListWidget.__init__(self)
        self.listbox = QtWidgets.QListWidget(win)
        self.listbox.setGeometry(QtCore.QRect(x, y, width, height))
        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(fontsize)
        self.listbox.setFont(self.font)

    def add(self, expenseTime, txt: str = None, currselect: tuple = None, index: int = 0):

        """Adds items into listbox.
        Valid expenseTime: ('dup', 'once'), ('dup', 'month'), 'once', 'month'"""

        if isinstance(expenseTime, tuple):
            self.listbox.insert(index, txt)
            name = txt.split(',')[0]
            currency = comboBoxCur.getText().split(' ')[1]
            price = txt.split(' ')[1].split(currency)[0]
            expTime = expenseTime[1]
            moreInfo = ''
            if expenseTime == ('dup', 'once'):
                moreInfo = dtbOnce.getRowValuesById(currselect[0], 3)
            elif expenseTime == ('dup', 'month'):
                moreInfo = dtbMonth.getRowValuesById(currselect[0], 3)
            addListToDtb(float(price), name, expTime, moreInfo)
            return True

        name = expNameTxt.getText()
        price = expPriceTxt.getText()
        moreInfo = expInfo.getText()
        currency = comboBoxCur.getText().split(' ')[1]
        multiplier = expMultiTxt.getText()

        # Check if valid price and multiplier input
        msgbox = QtWidgets.QMessageBox(mainWin.win)
        msgbox.setWindowTitle('Error')
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
        msgbox.setGeometry(500, 200, 300, 500)
        try:
            price = float(price)
            multiplier = int(multiplier)
        except:
            msgbox.information(msgbox, 'Invalid Input', 'Invalid Input, try again!')
            return False

        if name and price != '':
            text = f'{name}, {price}{currency}'
            for i in range(multiplier):
                self.insertItems(0, text)
                addListToDtb(price, name, expenseTime, moreInfo)
                expMultiTxt.text = 1
            return True
        else:
            msgbox.information(msgbox, 'Invalid Input', 'Invalid Input, try again!')
            return False

    def insertItems(self, row: int, *args: str) -> None:

        """Inserts all Items specified as args"""

        for arg in args:
            self.listbox.insertItem(0, arg)

    def curselection(self) -> int:

        """:returns: the current selection of listbox as a rowID"""

        return self.listbox.currentIndex().row()

    def curselectionItem(self) -> str:

        """:returns: the text of the current selection of listbox"""

        return self.listbox.currentItem().text()

    def delete(self, rowID: int) -> None:

        """Deletes item with index rowID"""

        self.listbox.takeItem(rowID)

    def update(self, selection: int, name: str, price: float):
        """Updates listboxselection. Works by deleting the previos entry and replacing it with a new one"""

        self.delete(selection)
        self.insertItems(selection, f'{name}, {price}{comboBoxCur.getText().split(" ")[1]}')


class CheckBox(QtWidgets.QCheckBox, QtWidgets.QAbstractButton):
    """Simplified class for PyQt5.QtWidgets.QCheckBox CheckBox"""

    def __init__(self, win: QtWidgets.QMainWindow, text: str, command: callable = None, checked: bool = False,
                 x: int = 0, y: int = 0, width:
            int = 75, height: int = 23, font: str = DEFAULTFONT, fontsize: int = 8) -> None:

        super().__init__()

        self.text = text
        self._command = command
        self.checkbox = QtWidgets.QCheckBox(win)
        self.checkbox.setGeometry(QtCore.QRect(x, y, width, height))
        self.checkbox.setText(self.text)

        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.checkbox.setFont(self.font)
        self.setChecked(checked)
        if self.command:
            self.checkbox.clicked.connect(self.command)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, func: callable):
        self._command = func

    def unckeckAny(self, checked: bool, *chbs: QtWidgets.QCheckBox) -> None:

        """checked: bool should equal True if the checkbox was checked before the click"""

        for chb in chbs:
            if checked:
                self.checkbox.setChecked(False)
                chb.setChecked(True)
            elif not checked:
                self.checkbox.setChecked(True)
                chb.setChecked(False)

    def setChecked(self, value: bool) -> None:

        """Set checked value"""

        self.checkbox.setChecked(value)

    def uncheck(self):

        """Unchecks checkbox"""

        self.setChecked(False)

    def check(self):

        """Checkes checkbox"""

        self.setChecked(True)


class ComboBox(QtWidgets.QComboBox):
    """Simplified class of PyQt5.QtWidgets.QComboBox ComboBox"""

    def __init__(self, win: QtWidgets.QMainWindow, x: int = 0, y: int = 0, width: int = 75, height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8) -> None:
        super().__init__()
        self.combobox = QtWidgets.QComboBox(win)
        self.combobox.setGeometry(QtCore.QRect(x, y, width, height))
        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(fontsize)
        self.combobox.setFont(self.font)

    def addItems(self, *drops: str) -> None:
        """Adds items with param drops"""

        self.combobox.addItems(drops)

    def addItem(self, drop: str, userData: any = None) -> None:
        """Adds single item to combobox"""

        self.combobox.addItem(drop)

    def getText(self) -> str:
        """:returns the current text of the combobox"""

        return self.combobox.currentText()


class PlainText(QtWidgets.QPlainTextEdit):
    """Simplified class of PyQt5.QtWidgets.QPlainTextEdit PlainText"""

    def __init__(self, win: QtWidgets.QMainWindow, text: str = '', x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8) -> None:
        super().__init__()
        self._text = text
        self.plain = QtWidgets.QPlainTextEdit(win)
        self.plain.setGeometry(QtCore.QRect(x, y, width, height))
        self.plain.insertPlainText(self.text)
        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.plain.setFont(self.font)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.plain.setPlainText(value)

    def getText(self):
        """:returns the current text of the plain"""

        return self.plain.toPlainText()

    def mousePressEvent(self, event) -> None:
        print('MouseEvent executed')
        if self.getText() == DEFAULTPLAINTEXT:
            self.text = ''


class Label(QtWidgets.QLabel):
    """Simplified class for PyQt5.QtWidgets.QLabel Label"""

    def __init__(self, win: QtWidgets.QMainWindow, text: str = None, x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23, font: str = 'MS Shell Dlg 2', fontsize: int = 8) -> None:
        super().__init__()

        self._text = text
        self.label = QtWidgets.QLabel(win)
        self.label.setText(self._text)
        self.label.setGeometry(QtCore.QRect(x, y, width, height))
        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.label.setFont(self.font)

    # def setText(self, value) -> None:
    #     self.label.setText(value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.label.setText(value)

    def delete(self):
        """Deletes(destroys) label"""

        self.label.destroy()


class SpinBox(QtWidgets.QSpinBox):
    """Simplified class of PyQt5.QtWidgets.QSpinBox SpinBox"""

    def __init__(self, win: QtWidgets.QMainWindow, text: int = 0, x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8, mincount: int = 0, maxcount: int = 999) -> None:
        super().__init__()
        self._text = text
        self.spinbox = QtWidgets.QSpinBox(win)
        self.spinbox.setGeometry(QtCore.QRect(x, y, width, height))
        self.spinbox.setMinimum(mincount)
        self.spinbox.setMaximum(maxcount)
        self.spinbox.setValue(text)
        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(fontsize)
        self.spinbox.setFont(self.font)

    @property
    def text(self):
        return self._value

    @text.setter
    def text(self, value):
        self._text = value
        self.spinbox.setValue(value)

    def getText(self):
        """:returns the text(value) of the spinbox"""

        return self.spinbox.value()


def delOnce(currselectOnce: int):
    try:
        dtbOnce.removeFromDtb(currselectOnce)
        lstbox.delete(currselectOnce)
        lblNetto.text = f'Your remaining budget: {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'
    except IndexError:
        return


def delMonth(currselectMonth):
    try:
        dtbMonth.removeFromDtb(currselectMonth)
        lstboxMonth.delete(currselectMonth)
        lblNetto.text = f'Your remaining budget: {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'
    except IndexError:
        return


def delSelectedItem(event=None):
    """Main handler for deleting the selected item."""

    currselectOnce = lstbox.curselection()
    currselectMonth = lstboxMonth.curselection()
    if currselectOnce != -1 and currselectMonth != -1:
        if chbOneTime.checkbox.isChecked():
            delOnce(currselectOnce)
        elif chbMonthly.checkbox.isChecked():
            delMonth(currselectMonth)
    elif currselectOnce != -1:
        delOnce(currselectOnce)
    elif currselectMonth != -1:
        delMonth(currselectMonth)


def addItem(event=None):
    """Main handler for adding items to listbox"""

    if chbOneTime.checkbox.isChecked():
        if lstbox.add('once'):
            expNameTxt.text = ''
            expPriceTxt.text = ''
            if expInfo.getText() != DEFAULTPLAINTEXT:
                expInfo.text = ''
            else:
                expInfo.text = DEFAULTPLAINTEXT
            lblNetto.text = f'Your remaining budget: {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'
    elif chbMonthly.checkbox.isChecked():
        if lstboxMonth.add('month'):
            expNameTxt.text = ''
            expPriceTxt.text = ''
            expInfo.text = '' if expInfo.text != DEFAULTPLAINTEXT else DEFAULTPLAINTEXT
            lblNetto.text = f'Your remaining budget {str(calculateResult())}{comboBoxCur.getText().split(" ")[1]}'


def dupSelectedItem(event=None):
    """Duplication of the current selection and adding it to the list at index 0"""

    currselectOnce = lstbox.curselection()
    currselectMonth = lstboxMonth.curselection()
    if currselectOnce != -1:
        lstbox.insertItems(currselectOnce + 1, lstbox.currentItem().text())
        lblNetto.update()
    elif currselectMonth != -1:
        lstboxMonth.insertItems(currselectMonth + 1, lstboxMonth.currentItem().text())
        lblNetto.update()


def selectDirMoveFiles():
    """Used when the 'select directory' button is pressed. closes all database connections and moves the files."""

    global path
    newPath = ''
    filedialog = QtWidgets.QFileDialog(mainWin.win, 'Select Directory')
    filedialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
    if filedialog.exec_() == QtWidgets.QDialog.Accepted:
        newPath = filedialog.selectedFiles()[0]
    if newPath is not path:
        dtbOnce.cursor.close()
        dtbOnce.conn.close()
        dtbMonth.cursor.close()
        dtbMonth.conn.close()
        dtbOldOnce.cursor.close()
        dtbOldOnce.conn.close()

        move(path, newPath)
        path = newPath
        writeToTxtFile(dirfile, path + '/ExpenseTracker/')
        restart()


def addListToDtb(price: float, exp: str, t: str, moreInfo: str = None):
    """Adds parameters to database"""

    if t == 'once':
        dtbOnce.dataEntry(float(price), t, exp, moreInfo)
    elif t == 'month':
        dtbMonth.dataEntry(float(price), t, exp, moreInfo)
    else:
        raise ValueError


def isFirstTime():
    """Checks if this is the first time the user openes the program"""

    if exists(path + 'FirstTime.txt'):
        if readFromTxtFile(path + 'FirstTime.txt', 'str') == 'False':
            return False
        else:
            writeToTxtFile(path + 'FirstTime.txt', 'False')
            return True
    else:
        return True


def setBudget():
    """Sets the budget with a messagebox and writes it to txt file"""

    inpt, okpressed = QtWidgets.QInputDialog.getDouble(mainWin.win, 'Set Budget', 'Please enter your monthly budget',
                                                       min=0, decimals=2)
    if okpressed:
        writeToTxtFile(path + 'Budget.txt', str(inpt))
        return inpt
    else:
        exit()


def setBudgetBtn():
    """Main handler for button press"""

    setBudget()
    restart()


def restart():
    execl(sys.executable, sys.executable, *sys.argv)


def showExpenseInfo(event=None):
    """Displays the info in a messagebox"""

    curselectOnce = lstbox.curselection()
    curselectMonth = lstboxMonth.curselection()
    msgbox = QtWidgets.QMessageBox(mainWin.win)
    msgbox.setWindowTitle('Expense Info')
    msgbox.setGeometry(500, 200, 300, 500)
    if curselectOnce != -1:
        infoOnce = dtbOnce.getRowValuesById(curselectOnce, 3)
        if infoOnce != [None]: msgbox.information(msgbox, 'Product Info', ''.join(infoOnce))
    elif curselectMonth != -1:
        infoMonth = dtbMonth.getRowValuesById(curselectMonth, 3)
        if infoMonth != [None]: msgbox.information(msgbox, 'Product Info', ''.join(infoMonth))


def readFromTxtFile(pa: str, typ: str):
    """Reads from text file. Valid typ params: 'str', 'float'"""

    global budget
    try:
        with open(pa, 'r') as f:
            if typ == 'float':
                return float(f.readline())
            elif typ == 'str':
                r = f.readline()
                return r
            else:
                raise ValueError('Invalid type!')
    except FileNotFoundError:
        f = open(pa, 'w+')
        f.close()
    except ValueError:
        return setBudget()


def writeToTxtFile(pa: str, text: str):
    """Writes to text file in write mode"""

    with open(pa, 'w') as f:
        f.write(str(text))


def calculateResult():
    """Returns the end result of the expense calculation"""

    return round(float(budget) - (dtbOnce.cal() + dtbMonth.cal()), 2)


def clearD():
    """Clears database depending on the checked checkbox"""

    if chbOneTime.checkbox.isChecked():
        dtbOnce.clearDtb()
        lstbox.listbox.clear()
    elif chbMonthly.checkbox.isChecked():
        dtbMonth.clearDtb()
        lstboxMonth.listbox.clear()


def isMonthEnd():
    """Returns True if the month has ended, else False"""

    lastDate = readFromTxtFile(path + 'LastOpened.txt', 'str')
    today = datetime.today()
    lastMonth, lastYear = lastDate.split(';')
    lastMonth = int(lastMonth)
    lastYear = int(lastYear)
    if today.month > lastMonth and today.year == lastYear:
        writeToTxtFile(path + 'LastOpened.txt', f'{str(today.month)};{str(today.year)}')
        return True
    elif today.year > lastYear:
        writeToTxtFile(path + 'LastOpened.txt', f'{str(today.month)};{str(today.year)}')
        return True
    return False


def monthEnd():
    """The events that have to happen if the month has ended. Line moving all old One-Time expenses to the oldDtb and writing date to text file"""

    if isMonthEnd():
        msgbox = QtWidgets.QMessageBox(mainWin.win)
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.setWindowTitle('New month!')
        for data in dtbOnce.getAllRecords():
            dtbOldOnce.dataEntry(data[2], 'once', data[1], data[3])
            dtbOnce.clearDtb()
            lstbox.listbox.clear()
            msgbox.information(msgbox, 'New Month', 'A new month has begun, all One-Time-Expenses were deleted!')


def initPlot(l1, l2, label: str, tile: str, xlabl: str, ylabl: str, linestyle: str = None):
    """Plots the plot used to show expense graph"""

    plot(l1, l2, marker='o', linestyle=linestyle, label=label, color='k')
    legend()
    title(tile)
    xlabel(xlabl)
    ylabel(ylabl)
    show()


def lstSum(lst: list) -> float:
    """Returns a float of the sum of two lists"""

    org = 0
    for elem in lst: org += elem
    return org


def showGraph(t: str, tile: str, xaxis: str, yaxis: str):
    """Gets items from dtb and calls initPlot method"""

    now = datetime.now()
    if t == 'month':
        dtbOnce.cursor.execute('SELECT Day, Price FROM OneTimeExpenseTable WHERE Month = ?', (now.month,))
    elif t == 'year':
        dtbOnce.cursor.execute('SELECT Month, Price FROM OneTimeExpenseTable WHERE Year = ?', (now.year,))
    else:
        raise ValueError('Please Enter "month" or "year"')

    days = []
    prices = []
    for val in dtbOnce.cursor.fetchall():
        days.append(val[0])
        prices.append(val[1])

    dic = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
           17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0}

    valueLst = [elem for elem in zip(days, prices)]

    p = []
    for value in valueLst:
        p.append(value[1])
        dic[value[0]] = round(lstSum(p), 2)

    initPlot(list(dic.keys()), list(dic.values()), 'One-Time Expenses', tile, xaxis, yaxis, linestyle='--')


def showYearGraph():
    showGraph('year', 'Expenses of the last year', 'month', 'price')


def showMonthGraph():
    showGraph('month', 'Expenses of the last month', 'days', 'price')


def createFiles():
    """Creates the files when the program is first opened."""

    try:
        mkdir('C:/tmp/')
    except:
        pass
    try:
        mkdir(path)
    except:
        pass
    open(dirfile, 'w+')
    open(path + 'Budget.txt', 'w+')
    open(expenseDtbPath, 'w+')
    open(path + 'FirstTime.txt', 'w+')
    open(path + 'LastOpened.txt', 'w+')
    f = open(path + 'OldExpenses.db', 'w+')
    f.close()


def chb1CommandHandler():
    chbOneTime.unckeckAny(False, chbMonthly)


def chb2CommandHandler():
    chbMonthly.unckeckAny(False, chbOneTime)


def edit():
    """Function to handle the edit window"""
    editWin = Editor('Editor')
    currselectOnce = lstbox.curselection()
    currselectMonth = lstboxMonth.curselection()

    if currselectOnce != -1 or currselectMonth != -1:

        expNameTxtEdit = TextBox(editWin.editWin, x=60, y=110, width=220, height=40, fontsize=16)
        expPriceTxtEdit = TextBox(editWin.editWin, x=300, y=110, width=220, height=40, fontsize=16)
        expInfoEdit = PlainText(editWin.editWin, x=60, y=160, width=460, height=180, fontsize=11)

        # insert all texts
        if currselectOnce != -1:
            values = dtbOnce.getRowValuesById(currselectOnce, 1, 2, 3, 4, 5, 6)
            expNameTxtEdit.text = str(values[0])
            expPriceTxtEdit.text = str(float(values[1]))
            expInfoEdit.text = str(values[2])
            Label(editWin.editWin, f'This expense was added on {values[3]}-{values[4]}-{values[5]}', x=60,
                  y=10, width=550, height=40, fontsize=18)
            try:
                editWin.apply = editWin.apply(currselectOnce, currselectMonth, expNameTxtEdit.text,
                                              float(expPriceTxtEdit.text), expInfoEdit.text)
            except TypeError:
                pass
            except ValueError:
                msgbox = QtWidgets.QMessageBox.critical(None, 'Invalid Input', 'Invalid Input, try again',
                                                        QtWidgets.QMessageBox.Ok)
                if msgbox == QtWidgets.QMessageBox.Ok:
                    return
        elif currselectMonth != -1:
            values = dtbMonth.getRowValuesById(currselectMonth, 1, 2, 3, 4, 5, 6)
            expNameTxtEdit.text = str(values[0])
            expPriceTxtEdit.text = str(values[1])
            expInfoEdit.text = str(values[2])
            Label(editWin.editWin, f'This expense was added on {values[3]}-{values[4]}-{values[5]}', x=60,
                  y=10, width=550, height=40, fontsize=18)

            try:
                editWin.apply = editWin.apply(currselectOnce, currselectMonth, expNameTxtEdit.text,
                                              float(expPriceTxtEdit.text), expInfoEdit.text)
            except TypeError:
                pass
            except ValueError:
                msgbox = QtWidgets.QMessageBox.critical(None, 'Invalid Input', 'Invalid Input, try again',
                                                        QtWidgets.QMessageBox.Ok)
                if msgbox == QtWidgets.QMessageBox.Ok:
                    return

        Button(editWin.editWin, text='Ok', x=590, y=320, width=90, height=35, key='Return',
               command=editWin.apply)
        Button(editWin.editWin, text='Cancel', x=700, y=320, width=90, height=35, command=editWin.close)
        editWin.show()


if __name__ == '__main__':
    # Initialize main app
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(mainWindowTitle='ExpenseTracker', minsizeX=1200, minsizeY=600,
                         maxsizeX=1200, maxsizeY=600)
    mainWin.resize(1200, 600)
    lstbox = ListBox(mainWin.win, x=20, y=50, width=180, height=300, fontsize=13)
    lstboxMonth = ListBox(mainWin.win, x=20, y=380, width=180, height=210, fontsize=13)
    expenseDtbPath = 'C:/tmp/ExpenseTracker/Expenses.db'
    dirfile = 'C:/tmp/dir.txt'

    # Try to read from dirfile and set path = standart if it catches error
    try:
        path = readFromTxtFile(dirfile, 'str') if readFromTxtFile(dirfile, 'str') != '' else 'C:/tmp/ExpenseTracker/'
    except:
        path = 'C:/tmp/ExpenseTracker/'

    # All the first Time things like creating files and entering config data
    if isFirstTime():
        createFiles()
        writeToTxtFile(path + 'LastOpened.txt', str(datetime.today().month))
        writeToTxtFile(path + 'FirstTime.txt', 'False')
        writeToTxtFile(dirfile, path)
        budget = setBudget()
    else:
        expenseDtbPath = path + 'Expenses.db'
        budget = readFromTxtFile(path + 'Budget.txt', 'float')
    #
    #     # Drop down menu for currency
    comboBoxCur = ComboBox(mainWin.win, x=800, y=100, height=40, width=80, fontsize=11)
    comboBoxCur.addItems('Euro €', 'Dollar $', 'Pound £')

    # Database
    dtbOnce = DataBase(expenseDtbPath, 'OneTimeExpenseTable')
    dtbMonth = DataBase(expenseDtbPath, 'MonthlyExpenseTable')
    dtbOldOnce = DataBase(path + 'OldExpenses.db', 'OneTimeExpenseTable')

    for data in dtbOnce.readFromDtb():
        lstbox.insertItems(0, f'{data[0]}, {float(data[1])}{comboBoxCur.getText().split(" ")[1]}')
    for data in dtbMonth.readFromDtb():
        lstboxMonth.insertItems(0, f'{data[0]}, {float(data[1])}{comboBoxCur.getText().split(" ")[1]}')

    # Textboxes
    expNameTxt = TextBox(mainWin.win, x=350, y=100, width=220, height=40, fontsize=16)
    expPriceTxt = TextBox(mainWin.win, x=590, y=100, width=210, height=40, fontsize=16)

    # SpinBox for Multiplier
    expMultiTxt = SpinBox(mainWin.win, text=1, x=350, y=190, width=70, height=30, mincount=1)

    # Extra Info Text
    expInfo = PlainText(mainWin.win, text=DEFAULTPLAINTEXT, x=350, y=250, width=510, height=200, fontsize=11)

    # Labels
    totalexp = calculateResult()
    lblBrutto = Label(mainWin.win, text=f'Your monthly brutto budget: {budget}{comboBoxCur.getText().split(" ")[1]}',
                      x=440, y=10, height=50, width=500, fontsize=17)
    lblNetto = Label(mainWin.win, text=f'Your remaining budget: {totalexp}{comboBoxCur.getText().split(" ")[1]}', x=440,
                     y=480, height=50, width=500, fontsize=17)
    lbloneTime = Label(mainWin.win, 'One-Time-Expenses', 20, 20, 170, 20, fontsize=14)
    lblmonthly = Label(mainWin.win, 'Monthly-Expenses', 20, 360, 170, 20, fontsize=14)
    lblinfoExp = Label(mainWin.win, 'Expense name', 350, 80, 160, 20, fontsize=13)
    lblinfoPrice = Label(mainWin.win, 'Expense price ', 590, 80, 160, 20, fontsize=13)
    lblinfoMulti = Label(mainWin.win, 'Multiplier', 350, 160, 100, 20, fontsize=13)
    lblshortcutInfo = Label(mainWin.win,
                            text='<html><head/><body><p><span style=" font-weight:600; text-decoration: underline;">Controlls:</span></p><p>Add Item: 	&quot;Enter&quot;</p><p>Remove Item: 	&quot;Delete&quot;</p><p>Deselect Item: 	&quot;Ctrl+LMB&quot;</p><p>Edit: 	&quot;Ctrl+E&quot;</p><p>Duplicate: 	&quot;Ctrl+D&quot;</p><p>Clear list: 	&quot;Ctrl+C&quot;</p><p>Show more info: &quot;Ctrl+F&quot;</p></body></html>',
                            x=920, y=20, width=240, height=480, fontsize=15)

    # Checkboxes
    chbOneTime = CheckBox(mainWin.win, text='One-Time-Expense', command=chb1CommandHandler, x=780, y=180, width=250,
                          height=20)
    chbMonthly = CheckBox(mainWin.win, text='Monthly-Expense', command=chb2CommandHandler, x=780, y=220, width=250,
                          height=20)
    chbOneTime.check()

    # Check wether the month has ended
    monthEnd()

    # Buttons
    addBtn = Button(mainWin.win, text='Add', command=addItem, x=230, y=100, height=35, width=90, key='Return')
    delBtn = Button(mainWin.win, text='Delete', command=delSelectedItem, x=230, y=140, height=35, width=90,
                    key='Delete')
    editBtn = Button(mainWin.win, text='Edit', command=edit, x=230, y=200, height=35, width=90, key='Ctrl+E')
    dupBtn = Button(mainWin.win, text='Duplicate', command=dupSelectedItem, x=1080, y=300, height=2, width=10,
                    key='<Control-d>')
    dirBtn = Button(mainWin.win, text='Select Directory', command=selectDirMoveFiles, x=1080, y=555, height=35,
                    width=110)
    clearBtn = Button(mainWin.win, text='Clear List', command=clearD, x=230, y=240, height=35, width=90, key='Ctrl+C')
    moreInfoBtn = Button(mainWin.win, text='More Info', command=showExpenseInfo, x=230, y=300, height=35, width=90,
                         key='Ctrl+F')
    updBrutto = Button(mainWin.win, text='Set Budget', command=setBudgetBtn, x=230, y=20, height=35, width=90)
    showExpGraph_30 = Button(mainWin.win, text='30-Day-Graph', command=showMonthGraph, x=230, y=360, height=35,
                             width=90)
    showExpGraph_365 = Button(mainWin.win, text='1-Year-Graph', command=showYearGraph, x=230, y=400, height=35,
                              width=90)

    # start the app
    mainWin.win.show()
    sys.exit(app.exec_())
