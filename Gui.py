import sys
from PyQt5.QtWidgets import QWidget, QAction, qApp, QApplication, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from _multiprocessing import send
import cv2
import numpy as np


class GameGui(QWidget):
    
    def __init__(self,debug,playersNum):
        
        super().__init__()
        self.debug = debug
        self.playersNum = playersNum
        self.InitUI()
        self.InitDraw()
        
    def InitUI(self): 
        
        
        sendButton = QPushButton("Send")
        sendButton.clicked.connect(self.ClickButtonSend)
        cancelButton = QPushButton('Exit')
        cancelButton.clicked.connect(qApp.quit)
        self.textBox = QTextEdit()
        self.textBox.setReadOnly(True)
        
        self.textEdit = QTextEdit()
        
        self.pic = QLabel()
        
        
        self.pic.setPixmap(QPixmap("images/BoardBase.png"))
        self.pic.resize(350,350)
        self.pic.show()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        vbox.addStretch(1)
        hbox.addWidget(sendButton)
        hbox.addWidget(cancelButton)
        vbox.addWidget(self.pic)
        vbox.addWidget(self.textBox)
        vbox.addLayout(hbox)
            
        #self.statusBar().showMessage('Ready')         
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        #self.statusBar()
        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAction)
        
        self.setGeometry(500, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.setLayout(vbox) 
        self.show()  
    
    def InitDraw(self):
        #gameboard picture
        fontWhite = cv2.imread("images/white_square.png")
        fontBlack = cv2.imread("images/brown_square.png")  
        boardPic = np.zeros((400,400,3),dtype=np.uint8)
        tick =0
        
        for x in range(8):
            for y in range(8):
                
                if x%2 == 0:
                    if tick %2==0:
                    
                        boardPic[50*x:50+50*x,50*y:50+50*y]  = fontWhite
                
                    else:
                    
                        boardPic[50*x:50+50*x,50*y:50+50*y]  = fontBlack
                        
                    
                else:
                
                    if tick %2==0:
                    
                        boardPic[50*x:50+50*x,50*y:50+50*y]  = fontBlack
                
                    else:
                    
                        boardPic[50*x:50+50*x,50*y:50+50*y]  = fontWhite
                        
                tick += 1
        if self.debug:
            cv2.imshow("BoardPic",boardPic)
        else:
            cv2.imwrite("images/BoardBase.png",boardPic)
        
    def DrawBoard(self,board):
        pass
    
    def ClickButtonSend(self):
            text = self.textEdit.toPlainText()
            text = 'sender: ' + '/u000a ' + text
            
            self.textBox.append( text)
            
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameGui(False,1)
    sys.exit(app.exec_())