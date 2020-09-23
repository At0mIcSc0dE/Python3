from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.Qt import Qt

DEFAULTFONT = 'MS Shell Dlg 2'


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    # def keyPressEvent(self, event, *keys):
    #     if event.key() == Qt.Key_Return:
    #         lstbox.insertItem(0, 'hello')


class Button(QtWidgets.QPushButton):
    """Simplyfied button class for PyQt5.QtWindgets.QPushButton"""

    def __init__(self, win: MainWindow, text: str = None, x: int = 0, y: int = 0, width: int = 75,
                 height: int = 23,
                 font: str = 'MS Shell Dlg 2', fontsize: int = 8, command: callable = None) -> None:
        super().__init__()

        self._text = text
        self.command = command
        self.button = QtWidgets.QPushButton(win)
        self.button.setGeometry(QtCore.QRect(x, y, width, height))
        self.button.setText(self.text)
        self.button.clicked.connect(self.command)
        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.button.setFont(self.font)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value
        self.button.setText(self._text)


class Label(QtWidgets.QLabel):
    """Simplified class for PyQt5.QtWidgets.QLabel Label"""

    def __init__(self, win: MainWindow, text: str = None, x: int = 0, y: int = 0, width: int = 75,
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
    def text(self, value):
        self._text = value
        self.label.setText(value)


class CheckBox(QtWidgets.QCheckBox, QtWidgets.QAbstractButton):
    """Simplified class for PyQt5.QtWidgets.QCheckBox CheckBox"""

    def __init__(self, win: MainWindow, text: str, command: callable = None, checked: bool = False, x: int = 0,
                 y: int = 0, width:
            int = 75, height: int = 23, font: str = DEFAULTFONT, fontsize: int = 8) -> None:

        super().__init__()

        self.text = text
        self.command = command
        self.checkbox = QtWidgets.QCheckBox(win)
        self.checkbox.setGeometry(QtCore.QRect(x, y, width, height))

        self.font = QtGui.QFont()
        self.font.setPointSize(fontsize)
        self.font.setFamily(font)
        self.checkbox.setFont(self.font)
        self.setChecked(checked)
        if self.command:
            self.checkbox.clicked.connect(self.command)

    def setChecked(self, value: bool) -> None:
        self.checkbox.setChecked(value)

    def unckeckAny(self, checked: bool, *chbs: QtWidgets.QCheckBox) -> None:

        """:arg checked: bool should equal True if the checkbox was checked before the click"""

        for chb in chbs:
            if checked:
                self.checkbox.setChecked(False)
                chb.setChecked(True)
            elif not checked:
                self.checkbox.setChecked(True)
                chb.setChecked(False)


class ListBox(QtWidgets.QListWidget):
    """Simplified class for PyQt5.QtWidgets.QListWidget ListBox"""

    def __init__(self, win: MainWindow, x: int = 0, y: int = 0, width: int = 75, height: int = 23,
                 font: str = DEFAULTFONT, fontsize: int = 8) -> None:
        QtWidgets.QListWidget.__init__(self)
        self.lstbox = QtWidgets.QListWidget(win)
        self.lstbox.setGeometry(QtCore.QRect(x, y, width, height))
        self.font = QtGui.QFont()
        self.font.setFamily(font)
        self.font.setPointSize(fontsize)
        self.lstbox.setFont(self.font)

    def insertItems(self, row: int, *args: str) -> None:
        """Inserts all Items specified as args"""

        for arg in args:
            self.lstbox.insertItem(0, arg)

    def currselection(self) -> int:
        """:returns: the current selection of listbox as a rowID"""

        return self.lstbox.currentIndex().row()

    def currselectionItem(self) -> str:
        """:returns: the text of the current selection of listbox"""

        return self.lstbox.currentItem().text()

    def delete(self, rowID: int) -> None:
        """Deletes item with index rowID"""

        self.lstbox.takeItem(rowID)


class TextBox(QtWidgets.QLineEdit):
    """Simplified class of PyQt5.QtWidgets.QLineEdit TextBox"""

    def __init__(self, win: MainWindow, text: str = '', x: int = 0, y: int = 0, width: int = 75, height: int = 23,
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


class ComboBox(QtWidgets.QComboBox):
    """Simplified class of PyQt5.QtWidgets.QComboBox ComboBox"""

    def __init__(self, win: MainWindow, x: int = 0, y: int = 0, width: int = 75, height: int = 23,
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

    def __init__(self, win: MainWindow, text: str = '', x: int = 0, y: int = 0, width: int = 75, height: int = 23,
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

    # def mousePressEvent(self, event) -> None:
    #     print('MouseEvent executed')
    #     if self.getText() == 'Write more info about your expense here...':
    #         self.text = ''


class SpinBox(QtWidgets.QSpinBox):
    """Simplified class of PyQt5.QtWidgets.QSpinBox SpinBox"""

    def __init__(self, win: MainWindow, text: int = 0, x: int = 0, y: int = 0, width: int = 75, height: int = 23,
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
        return self.spinbox.value()


class FileDialog(QtWidgets.QFileDialog):
    """Simplified class for PyQt5.QtWidgets.QFileDialog FileDialog"""

    def __init__(self, win: MainWindow, text: str):
        super().__init__()
        self.filedialog = QtWidgets.QFileDialog(self, text)
        self.filedialog.show()

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)


if __name__ == '__main__':
    def onClickchb1():
        print('done')
        chb1.unckeckAny(False, chb2)


    def onClickchb2():
        print('2')
        chb2.unckeckAny(False, chb1)


    def onClickbtn():
        print(lstbox.currselection())
        print(txtbox.getText())
        lstbox.delete(lstbox.currselection())


    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.resize(1200, 600)

    btn1 = Button(mainWin, text='done', x=20, fontsize=10, command=onClickbtn)
    lbl1 = Label(mainWin, text='hello', x=100)
    chb1 = CheckBox(mainWin, text='checkb', command=onClickchb1, x=300)
    chb2 = CheckBox(mainWin, text='should be unchecked', x=500, checked=True, command=onClickchb2)
    lstbox = ListBox(mainWin, y=200, x=10, height=200)
    lstbox.insertItems(0, 'hello', 'noe')
    txtbox = TextBox(mainWin, text='hello', x=200, y=200)
    combo = ComboBox(mainWin, x=200, y=300)
    combo.addItems('helo', 'none', 'im done')
    plain = PlainText(mainWin, text='Write more info about your expense here...', x=400, y=20, width=120, height=200)
    spin = SpinBox(mainWin, text=1, x=100, y=400, mincount=1)
    filedialog = FileDialog(mainWin, 'hello')
    filedialog.fileMode()

    mainWin.show()

    sys.exit(app.exec_())
