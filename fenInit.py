from PyQt5.QtWidgets import QWidget, QAction, qApp, QApplication, QLabel,QInputDialog, QCheckBox ,QDialog, QComboBox,QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, pyqtSlot
from PyQt5.QtCore import Qt
import cv2
import numpy as np

import sys

class InitScreen(QDialog):
    def __init__(self,robot):
        
        super().__init__()
        self.robot = robot
        self.isCheckedOne=False
        self.isCheckedTwo=False
        self.isCheckedThree=False

        self.isPlayerOne=False
        self.isPlayerTwo=False
        self.isPlayerThree=False

        self.UI()
        
    def UI(self):
        self.setWindowTitle("Fen Clear?")
        self.setGeometry(300, 150, 250, 125)
        noBtn = QPushButton('No',self)
        noBtn.move(10,20)
        noBtn.show()
        yesBtn = QPushButton('Yes',self)
        yesBtn.move(150,20)
        yesBtn.show()
        noBtn.clicked.connect(self.Close)
        yesBtn.clicked.connect(self.Clear)

        text = QLabel('Select players who will be clear', self)
        text.move(10, 60)
        self.playerFenOne = QCheckBox('Player 1', self)
        self.playerFenOne.move(10,80)
        self.playerFenOne.clicked.connect(self._clickedFirstPlayer)
        self.playerFenTwo = QCheckBox('Player 2', self)
        self.playerFenTwo.move(85,80)
        self.playerFenTwo.clicked.connect(self._clickedSecondPlayer)
        self.playerFenThree = QCheckBox('Player 3', self)
        self.playerFenThree.move(170,80)
        self.playerFenThree.clicked.connect(self._clickedThirdPlayer)
        self.show()
        
    def Close(self):
        self.close()
    
    def Clear(self):
        if self.isPlayerOne==True:
            filename = 'player0.txt'
            file = open(filename,'w')
            file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
            file.close()
        if self.isPlayerTwo==True:
            filename = 'player1.txt'
            file = open(filename,'w')
            file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
            file.close()
        if self.isPlayerThree==True:   
            filename = 'player2.txt'
            file = open(filename,'w')
            file.write('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
            file.close()

        self.close()

    @pyqtSlot()  
    def _clickedFirstPlayer(self):
        self.isCheckedOne = not self.isCheckedOne
        self.playerFenOne.setChecked(self.isCheckedOne)
        if self.playerFenOne.isChecked():
            self.isPlayerOne=True
        else:
            self.isPlayerOne=False

    @pyqtSlot()  
    def _clickedSecondPlayer(self):
        self.isCheckedTwo = not self.isCheckedTwo
        self.playerFenTwo.setChecked(self.isCheckedTwo)
        if self.playerFenTwo.isChecked():
            self.isPlayerTwo=True
        else:
            self.isPlayerTwo=False

    @pyqtSlot()
    def _clickedThirdPlayer(self):
        self.isCheckedThree = not self.isCheckedThree
        self.playerFenThree.setChecked(self.isCheckedThree)
        if self.playerFenThree.isChecked():
            self.isPlayerThree=True
        else:
            self.isPlayerThree=False
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    robot = []
    ex = InitScreen(robot)
    
    sys.exit(app.exec_())
