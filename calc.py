# -*- coding: utf-8 -*-
# ---------------------
from PyQt5 import QtCore, QtWidgets, QtGui
import time


class MyLineEdit(QtWidgets.QLineEdit):  # Делаем свой однострочный ввод со своим id
    def __init__(self, id, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.id = id

    def focusInEvent(self, e):  # перехватываем событие полуение фокуса
        # print("Focus lineEdit ", self.id)
        QtWidgets.QLineEdit.focusInEvent(self, e)  # передаем получение фокуса дальше

    def keyPressEvent(self, e):  # перехватываем нажатие клавиш
        # маски кнопок, которые можно нажимать в поле ввода (включая курсор лево право и бакспейс
        hex_mask = (QtCore.Qt.Key_0, QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4,
                    QtCore.Qt.Key_5, QtCore.Qt.Key_6, QtCore.Qt.Key_7, QtCore.Qt.Key_8, QtCore.Qt.Key_9,
                    QtCore.Qt.Key_A, QtCore.Qt.Key_B, QtCore.Qt.Key_C, QtCore.Qt.Key_D, QtCore.Qt.Key_E,
                    QtCore.Qt.Key_F, QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right)
        dec_mask = (QtCore.Qt.Key_0, QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4,
                    QtCore.Qt.Key_5, QtCore.Qt.Key_6, QtCore.Qt.Key_7, QtCore.Qt.Key_8, QtCore.Qt.Key_9,
                    QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right)
        bin_mask = (QtCore.Qt.Key_0, QtCore.Qt.Key_1, QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Left, QtCore.Qt.Key_Right)

        # print("MyLine Key press: ", e.key(), "text: ", e.text())
        window.label3.setText(str(e.key()) + ' ' + str(e.text()))

        if self.id == 1:  # первый id - для hex
            if e.key() in hex_mask:
                # self.keyPress_hex()
                QtWidgets.QLineEdit.keyPressEvent(self, e)  # передаем обработку клавишь дальше
        if self.id == 2:  # второй для десятичных
            if e.key() in dec_mask:
                QtWidgets.QLineEdit.keyPressEvent(self, e)  # передаем обработку клавишь дальше
        if self.id == 3:  # третий id для текста, любые символы
            QtWidgets.QLineEdit.keyPressEvent(self, e)  # передаем обработку клавишь дальше
        if self.id == 4:  # четверты для двоичных цифр
            if e.key() in bin_mask:
                # если курсор в позиции и не нажата клавиша  DEL то добавляем пробел, разделяем на байты
                if (window.lineEdit_bin.cursorPosition() in (8, 17, 26)) & (e.key() != QtCore.Qt.Key_Backspace):
                    window.lineEdit_bin.insert(' ')
                # если курсор в позиции и нажата DEL то дополнительно удаляем пробел
                elif (window.lineEdit_bin.cursorPosition() in (9, 18, 27)) & (e.key() == QtCore.Qt.Key_Backspace):
                    window.lineEdit_bin.backspace()
                QtWidgets.QLineEdit.keyPressEvent(self, e)  # передаем обработку клавиш дальше

    def enterEvent(self, e):
        # print("Enter event", self.id)
        QtWidgets.QLineEdit.enterEvent(self, e)


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Calc")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.resize(300, 100)
        self.setFont(QtGui.QFont("Latha", 11))

        self.label1 = QtWidgets.QLabel("")
        self.label1.setAlignment(QtCore.Qt.AlignHCenter)
        self.label2 = QtWidgets.QLabel("")
        self.label2.setAlignment(QtCore.Qt.AlignHCenter)
        self.label3 = QtWidgets.QLabel("")
        self.label3.setAlignment(QtCore.Qt.AlignHCenter)

        self.lineEdit_hex = MyLineEdit(1)
        self.lineEdit_hex.setMaxLength(8)
        self.lineEdit_hex.textEdited.connect(self.keyPress_hex)  # вызывается сразу при изменении текста в поле
        self.lineEdit_dec = MyLineEdit(2)
        self.lineEdit_dec.setMaxLength(10)
        self.lineEdit_dec.textEdited.connect(self.keyPress_dec)
        self.lineEdit_txt = MyLineEdit(3)
        self.lineEdit_txt.setMaxLength(4)
        self.lineEdit_txt.textEdited.connect(self.keyPress_txt)
        self.lineEdit_bin = MyLineEdit(4)
        self.lineEdit_bin.setMaxLength(35)
        self.lineEdit_bin.textEdited.connect(self.keyPress_bin)

        self.button_hex = QtWidgets.QPushButton('HEX')
        self.button_hex.setMaximumWidth(35)
        self.button_dec = QtWidgets.QPushButton('DEC')
        self.button_dec.setMaximumWidth(35)
        self.button_txt = QtWidgets.QPushButton('TXT')
        self.button_txt.setMaximumWidth(35)
        self.button_bin = QtWidgets.QPushButton('BIN')
        self.button_bin.setMaximumWidth(35)

        self.hbox_hex = QtWidgets.QHBoxLayout()
        self.hbox_dec = QtWidgets.QHBoxLayout()
        self.hbox_bin = QtWidgets.QHBoxLayout()
        self.hbox_txt = QtWidgets.QHBoxLayout()
        self.hbox_hex.addWidget(self.button_hex)
        self.hbox_hex.addWidget(self.lineEdit_hex)
        self.hbox_dec.addWidget(self.button_dec)
        self.hbox_dec.addWidget(self.lineEdit_dec)
        self.hbox_txt.addWidget(self.button_txt)
        self.hbox_txt.addWidget(self.lineEdit_txt)
        self.hbox_bin.addWidget(self.button_bin)
        self.hbox_bin.addWidget(self.lineEdit_bin)
        self.vbox_lineEdit = QtWidgets.QVBoxLayout()
        self.vbox_lineEdit.addLayout(self.hbox_hex)
        self.vbox_lineEdit.addLayout(self.hbox_dec)
        self.vbox_lineEdit.addLayout(self.hbox_txt)
        self.vbox_lineEdit.addLayout(self.hbox_bin)

        vbox = QtWidgets.QVBoxLayout()

        vbox.addWidget(self.label1)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.label3)
        vbox.addLayout(self.vbox_lineEdit)

        self.checkBoxItem()

        vbox.addLayout(self.hbox_check_line2)
        vbox.addLayout(self.hbox_check_line1)
        vbox.addStretch()

        self.setLayout(vbox)

    def keyPress_hex(self):
        # преобразовать шестнадцатиричную строку в целое по основанию системы счисления
        # если строка пустая, то результат преобразования 0
        if window.lineEdit_hex.text():
            result_dec = int(window.lineEdit_hex.text(), base=16)
        else:
            result_dec = 0
        window.lineEdit_dec.setText(str(result_dec))
        # преобразовать из кода символа в символ
        res_text1 = result_dec % 256
        res_text2 = (result_dec // 256) % 256
        res_text3 = (result_dec // 65536) % 256
        res_text4 = (result_dec // 16777216) % 256
        self.lineEdit_txt.setText(chr(res_text4) + chr(res_text3) + chr(res_text2) + chr(res_text1))
        # преобразование в бинарную строку, откинуть два первых символа и добавить пробелов
        res_bin = bin(result_dec)[2:].rjust(32, '0')  # добавляем в двоичную строку незначащие нули до 32
        res_bin2 = ' '.join([res_bin[i:i + 8] for i in range(0, len(res_bin), 8)])  # добавляем пробелов
        self.lineEdit_bin.setText(res_bin2)
        # преобразование десятичного числа в чекбоксы
        index = len(self.check) - 1
        while index >= 0:
            if (result_dec % 2) == 1:
                self.check[index].setCheckState(2)
            else:
                self.check[index].setCheckState(0)
            result_dec = result_dec >> 1
            index -= 1

    def keyPress_dec(self):
        # если строка пустая, то результат равен 0
        if window.lineEdit_dec.text():
            result_dec = int(window.lineEdit_dec.text())
        else:
            result_dec = 0
        window.lineEdit_hex.setText(hex(result_dec)[2:])
        # преобразовать из кода символа в символ
        res_text1 = result_dec % 256
        res_text2 = (result_dec // 256) % 256
        res_text3 = (result_dec // 65536) % 256
        res_text4 = (result_dec // 16777216) % 256
        self.lineEdit_txt.setText(chr(res_text4) + chr(res_text3) + chr(res_text2) + chr(res_text1))
        # преобразование в бинарную строку, откинуть два первых символа и добавить пробелов
        res_bin = bin(result_dec)[2:].rjust(32, '0')  # добавляем в двоичную строку незначащие нули до 32
        res_bin2 = ' '.join([res_bin[i:i + 8] for i in range(0, len(res_bin), 8)])  # добавляем пробелов
        self.lineEdit_bin.setText(res_bin2)
        # преобразование десятичного числа в чекбоксы
        index = len(self.check) - 1
        while index >= 0:
            if (result_dec % 2) == 1:
                self.check[index].setCheckState(2)
            else:
                self.check[index].setCheckState(0)
            result_dec = result_dec >> 1
            index -= 1

    def keyPress_txt(self):
        # преобразуем текстовые символы в коды , сдвигаем
        result_dec = 0
        i = 0
        while i < len(window.lineEdit_txt.text()):
            result_dec = result_dec << 8
            result_dec += ord(window.lineEdit_txt.text()[i])
            i += 1
        window.lineEdit_dec.setText(str(result_dec))
        window.lineEdit_hex.setText(hex(result_dec)[2:])
        # преобразование в бинарную строку, откинуть два первых символа и добавить пробелов
        res_bin = bin(result_dec)[2:].rjust(32, '0')  # добавляем в двоичную строку незначащие нули до 32
        res_bin2 = ' '.join([res_bin[i:i + 8] for i in range(0, len(res_bin), 8)])  # добавляем пробелов
        self.lineEdit_bin.setText(res_bin2)
        # преобразование десятичного числа в чекбоксы
        index = len(self.check) - 1
        while index >= 0:
            if (result_dec % 2) == 1:
                self.check[index].setCheckState(2)
            else:
                self.check[index].setCheckState(0)
            result_dec = result_dec >> 1
            index -= 1

    def keyPress_bin(self):
        # преобразовать двоичную строку в целое по основанию системы счисления
        # если строка пустая, то результат преобразования 0
        if window.lineEdit_bin.text():
            # удаляем все разделительные пробелы в двоичной строке
            res_temp = window.lineEdit_bin.text().replace(' ', '')
            result_dec = int(res_temp, base=2)
        else:
            result_dec = 0
        window.lineEdit_dec.setText(str(result_dec))
        window.lineEdit_hex.setText(hex(result_dec)[2:])
        # преобразовать из кода символа в символ
        res_text1 = result_dec % 256
        res_text2 = (result_dec // 256) % 256
        res_text3 = (result_dec // 65536) % 256
        res_text4 = (result_dec // 16777216) % 256
        self.lineEdit_txt.setText(chr(res_text4) + chr(res_text3) + chr(res_text2) + chr(res_text1))
        # преобразование десятичного числа в чекбоксы
        index = len(self.check) - 1
        while index >= 0:
            if (result_dec % 2) == 1:
                self.check[index].setCheckState(2)
            else:
                self.check[index].setCheckState(0)
            result_dec = result_dec >> 1
            index -= 1

    def checkBoxItem(self):  # функция делает массив чекбоксов и лейбл, помещает все в массив vbox-ов
        # а все vbox помещает в два Hbox
        # все чекбоксы законнекчены на функцию checkBoxItem_func
        self.hbox_check_line1 = QtWidgets.QHBoxLayout()
        self.hbox_check_line2 = QtWidgets.QHBoxLayout()
        self.check = []
        self.check_label = []
        self.vbox_check = []

        index = 0
        for item_name in range(31, 15, -1):
            self.check.append(QtWidgets.QCheckBox())
            self.check_label.append(QtWidgets.QLabel(str(item_name)))
            self.check_label[index].setAlignment(QtCore.Qt.AlignHCenter)
            self.vbox_check.append(QtWidgets.QVBoxLayout())
            self.vbox_check[index].addWidget(self.check[index], alignment=QtCore.Qt.AlignHCenter)
            self.vbox_check[index].addWidget(self.check_label[index])
            self.hbox_check_line2.addLayout(self.vbox_check[index])
            if index == 7:
                self.hbox_check_line2.addSpacing(20)
            self.check[index].clicked.connect(self.checkBoxItem_func)
            index += 1

        for item_name in (range(15, -1, -1)):
            self.check.append(QtWidgets.QCheckBox())
            self.check_label.append(QtWidgets.QLabel(str(item_name).rjust(2, '0')))  # добавляем незначащие нули
            self.check_label[index].setAlignment(QtCore.Qt.AlignHCenter)
            self.vbox_check.append(QtWidgets.QVBoxLayout())
            self.vbox_check[index].addWidget(self.check[index], alignment=QtCore.Qt.AlignHCenter)
            self.vbox_check[index].addWidget(self.check_label[index])
            self.hbox_check_line1.addLayout(self.vbox_check[index])
            if index == 23:
                self.hbox_check_line1.addSpacing(20)
            self.check[index].clicked.connect(self.checkBoxItem_func)
            index += 1

    def checkBoxItem_func(self):
        result_dec = 0
        index = len(self.check) - 1
        while index >= 0:
            result_dec += self.check[index].checkState() // 2 * 2 ** (len(self.check) - 1 - index)
            index -= 1
        self.lineEdit_dec.setText(str(result_dec))
        # преобразовать в hex и удалить первых два символа и к верхнему регистру
        self.lineEdit_hex.setText(str(hex(result_dec)[2:]).upper())
        # преобразовать из кода символа в символ
        res_text1 = result_dec % 256
        res_text2 = (result_dec // 256) % 256
        res_text3 = (result_dec // 65536) % 256
        res_text4 = (result_dec // 16777216) % 256
        self.lineEdit_txt.setText(chr(res_text4) + chr(res_text3) + chr(res_text2) + chr(res_text1))
        # преобразование в бинарную строку, откинуть два первых символа и добавить пробелов
        res_bin = bin(result_dec)[2:].rjust(32, '0')  # добавляем в двоичную строку незначащие нули до 32
        res_bin2 = ' '.join([res_bin[i:i + 8] for i in range(0, len(res_bin), 8)])  # добавляем пробелов
        self.lineEdit_bin.setText(res_bin2)

    def event(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            self.label1.setText("Key Press")
            # print("event Key press: ", e.key(), "text: ", e.text())
        elif e.type() == QtCore.QEvent.Close:
            # print("Window closed")
            pass
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            self.label1.setText('Click mouse ' + str(e.x()) + ' ' + str(e.y()))
            # print("Click mouse ", e.x(), e.y())
        return QtWidgets.QWidget.event(self, e)

    def resizeEvent(self, e):
        self.label2.setText(str(e.size().width()) + ' ' + str(e.size().height()))
        QtWidgets.QWidget.resizeEvent(self, e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
