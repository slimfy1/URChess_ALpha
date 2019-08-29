#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import  QApplication ,QPushButton,QLabel, QInputDialog, QDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
from PyQt5.QtCore import *
import time


class ExitDialog(QDialog):

    def __init__(self,code):
        super().__init__()
        
        self.exitCode = code
        self.res = 0
        self.initUI()
        
    def initUI(self):
        self.message = QLabel(self)
        self.message.setText('Введите пин для выхода')
        self.message.move(80,0)
        self.message.setFont(QFont("Calibri", 20, QFont.Bold))
        
        self.inputLabel = QLabel(self)
        #self.inputLabel.setText('')
        self.inputLabel.setFont(QFont("Calibri", 35, QFont.Bold))
        self.inputLabel.move(310,30)
        self.inputLabel.updatesEnabled()
        
        button0 = QPushButton('0',self)
        button0.resize(100,100)
        button0.move(200,460)
        button0.setFont(QFont("Calibri", 20, QFont.Bold))
        button0.clicked.connect(lambda: self.buttonPress(0))
        
        button1 = QPushButton('1',self)
        button1.resize(100,100)
        button1.move(80,100)
        button1.setFont(QFont("Calibri", 20, QFont.Bold))
        button1.clicked.connect(lambda: self.buttonPress(1))
        
        button2 = QPushButton('2',self)
        button2.resize(100,100)
        button2.move(200,100)
        button2.setFont(QFont("Calibri", 20, QFont.Bold))
        button2.clicked.connect(lambda: self.buttonPress(2))
        
        button3 = QPushButton('3',self)
        button3.resize(100,100)
        button3.move(320,100)
        button3.setFont(QFont("Calibri", 20, QFont.Bold))
        button3.clicked.connect(lambda: self.buttonPress(3))
        
        button4 = QPushButton('4',self)
        button4.resize(100,100)
        button4.move(80,220)
        button4.setFont(QFont("Calibri", 20, QFont.Bold))
        button4.clicked.connect(lambda: self.buttonPress(4))
        
        button5 = QPushButton('5',self)
        button5.resize(100,100)
        button5.move(200,220)
        button5.setFont(QFont("Calibri", 20, QFont.Bold))
        button5.clicked.connect(lambda: self.buttonPress(5))
        
        button6 = QPushButton('6',self)
        button6.resize(100,100)
        button6.move(320,220)
        button6.setFont(QFont("Calibri", 20, QFont.Bold))
        button6.clicked.connect(lambda: self.buttonPress(6))
        
        button7 = QPushButton('7',self)
        button7.resize(100,100)
        button7.move(80,340)
        button7.setFont(QFont("Calibri", 20, QFont.Bold))
        button7.clicked.connect(lambda: self.buttonPress(7))
        
        button8 = QPushButton('8',self)
        button8.resize(100,100)
        button8.move(200,340)
        button8.setFont(QFont("Calibri", 20, QFont.Bold))
        button8.clicked.connect(lambda: self.buttonPress(8))
        
        button9 = QPushButton('9',self)
        button9.resize(100,100)
        button9.move(320,340)
        button9.setFont(QFont("Calibri", 20, QFont.Bold))
        button9.clicked.connect(lambda: self.buttonPress(9))
        
        buttonDel = QPushButton('Del',self)
        buttonDel.resize(100,100)
        buttonDel.move(80,460)
        buttonDel.setFont(QFont("Calibri", 20, QFont.Bold))
        buttonDel.clicked.connect(lambda: self.buttonPress(10))
        
        buttonEnter = QPushButton('Ok',self)
        buttonEnter.resize(100,100)
        buttonEnter.move(320,460)
        buttonEnter.setFont(QFont("Calibri", 20, QFont.Bold))
        buttonEnter.clicked.connect(lambda: self.buttonPress(11))
        
        
        self.setGeometry(710, 300, 500, 600)  
        self.setWindowFlags(Qt.FramelessWindowHint)  
        #elf.setWindowTitle('Exit ?')
        
        self.show()
    def buttonPress(self,button):
        if button<10:
            text = self.inputLabel.text() +str(button)
            s = len(text)
            #print (text)
            #self.inputLabel = QLabel(self)
            self.inputLabel.setText(text)
            self.inputLabel.adjustSize()
            #self.inputLabel.setFont(QFont("Calibri", 35, QFont.Bold))
            self.inputLabel.move(310-29*s,30)
            #self.inputLabel.setText(text)
            #self.inputLabel.show()
            #elf.update()
        elif button ==10:
            text = self.inputLabel.text()
            text= text[0:-1]
            #print (text)
            s = len(text)
            self.inputLabel.move(310-29*s,30)
            self.inputLabel.setText(text)
            self.inputLabel.adjustSize()
        elif button ==11:
            text = self.inputLabel.text()
            if int(text)==self.exitCode:
                #print('end ok')
                self.res=1
                self.done(1)
                
                
            else:
                #print('end wrong')
                self.res = 0
                self.done(0)
                
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ExitDialog(1234)
    print(ex.res)
    sys.exit(app.exec_())