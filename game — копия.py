
#РѕСЃРЅРѕРІРЅРѕР№ С„Р°Р№Р» РєРѕС‚РѕСЂС‹Р№ Р±СѓРґРµС‚ РІС‹Р·С‹РІР°С‚СЊ РѕСЃС‚Р°Р»СЊРЅС‹Рµ Рё РІ РєРѕС‚РѕСЂРѕРј Р±СѓРґРµС‚ РїСЂРѕРёСЃС…РѕРґРёС‚СЊ РёРіСЂРѕРІРѕР№ С†РёРєР»
import urx #Р±РёР±Р»РёРѕС‚РµРєР° РґР»СЏ РѕР±С‰РµРЅРёСЏ СЃ СЂРѕР±РѕС‚РѕРј
import chess #СЂР°Р±РѕС‚Р° СЃ РёРіСЂРѕР№
import sys
from PyQt5.QtWidgets import QWidget, QAction, qApp, QApplication, QLabel,QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from _multiprocessing import send
import cv2
import numpy as np
from UtilityFucntions import *
#import Gui
import InitScreen
import fenInit
from chessAi import *
import time
from Threads import *
from PyQt5 import QtCore
from pygame.mixer_music import play
from numpy.f2py.auxfuncs import isfalse
from urx.ursecmon import TimeoutException
import win32com.client
from dataStructers import camId as id
#from engine import Engine

class MainGame(QWidget):
    "'it` a game class"''
    def __init__(self,debug,playersNum):
        super().__init__()
        self.debug = debug
        self.camera = cv2.VideoCapture(id)
         
        try:
             while True:
                 done = self.connect2Robot()
                 if type(done)!='None':
                     break
        except TimeoutException:
            pass
          
        if  self.debug:
            self.debug = debug
            print('this is debug mode')
        else:
            print('all fine')
        #self.robot = FakeRobot('ip',1)
        dialog = fenInit.InitScreen(self.robot)
        dialog.exec()
        dialog = InitScreen.InitScreen(0,self.robot)
        dialog.exec()
        #print('tratatata',dialog.playersNum)
            
        self.playersNum = dialog.playersNum    
        self.restartStatus = [True,True,True]     
        self.difficulties =dialog.plDifficult
        self.aiDifficulties=dialog.aiDifficult
        self.players = dialog.isPlayer
        self.initDone = False
        self.curPlayer = [0,1]
        self.loopDone = [True,True,True]
        self.RobotMoveDone = [True,True,True]
        self.GenerateMoveDone = [True,True,True,True]
        self.playerPhotoStatus=[True,True,True]
        self.InitUI(False)
        self.CheckPermission = [False,False,False]
        self.InitDraw()
    
    def connect2Robot(self):
            self.robot = urx.Robot("192.168.0.20", use_rt=True)
            print(self.robot)
            for i in range(7):
                self.robot.set_digital_out(i, False)
            return(self.robot)
    
#     def ButtonLed(self, GenerateMoveDone, robot):
#         if GenerateMoveDone[0]==True:
#             self.robot.set_digital_out(dataStructers.led_flash, True)
#             
#             if self.robot.get_digital_in(0) == True:
#                 
#         else:
#             self.robot.set_digital_out(dataStructers.led_flash, False)
            
            
    def InitUI(self,old): 
        
        
        
        if old==False:
            
            
            self.buttonsPause=[]
            self.buttonsPhoto=[]
            self.buttonsReset=[]
            self.buttonsStop=[]
            self.playerNamesLabels = []
            self.aiNamesLabels = []
            self.chessboardDisplays = []
            self.turn = ['w','w','w']
            self.curTurn = []
            self.logs = []  
            
            for i in range(self.playersNum):

                self.playerNamesLabels.append(QLabel(self))
                if self.players[i]==True:
                    self.playerNamesLabels[i].setText("Player \nPlayer "+str(i+1))
                else:
                    self.playerNamesLabels[i].setText("Player \n Ai:"+str(self.aiDifficulties[i]))
                self.playerNamesLabels[i].resize(80,40)
                self.playerNamesLabels[i].move(4+500*i,0)
                
                self.aiNamesLabels.append(QLabel(self))
                self.aiNamesLabels[i].setText("Robot\n AI:"+ str(self.difficulties[i]))
                self.aiNamesLabels[i].resize(80,40)
                self.aiNamesLabels[i].move(4+500*i,55)
  
                self.curTurn.append(QLabel('123',self))
                if self.turn[i]=='w':
                    self.curTurn[i].setText('Current\n Turn:\n White')
                else:
                    self.curTurn[i].setText('Current\n Turn:\n Black')
                self.curTurn[i].resize(80,80)
                self.curTurn[i].move(4+500*i,110)    

                
                self.buttonsPause.append(QPushButton('Pause',self))
                self.buttonsReset.append(QPushButton('Restart',self))
                self.buttonsPhoto.append(QPushButton('ReMake',self))
                #self.buttonsStop.append(QPushButton('Stop',self))
                #self.buttonsStop[i].clicked.connect(self.StopGame)
                #self.buttonsStop[i].clicked.connect(self.StopGame)
                
                self.buttonsPause[i].resize(150,40)
                self.buttonsPause[i].move(80+500*i,540)
                  
                self.buttonsReset[i].resize(150,40)
                self.buttonsReset[i].move(250+500*i,540)
                
                self.buttonsPhoto[i].resize(40,40)
                self.buttonsPhoto[i].move(420+500*i,540)
                #self.buttonsStop[i].resize(150,40)
                #self.buttonsStop[i].move(250+500*i,590)

                  
                  
                self.logs.append(QTextEdit(self))
                self.logs[i].setReadOnly(True)
                self.logs[i].resize(400,100)
                self.logs[i].move(55+500*i,420)
                  
                  
                self.chessboardDisplays.append(QLabel(self))
                self.chessboardDisplays[i].setPixmap(QPixmap("images/BoardBase.png"))
                self.chessboardDisplays[i].resize(400,400)
                self.chessboardDisplays[i].move(55+500*i,0)
                  
            self.buttonsChange = QPushButton('',self)
            self.buttonsChange.setIcon(QIcon('images\settings.png'))
            self.buttonsChange.resize(48,48)
            self.buttonsChange.move(4,192)
            
            self.buttonsChange.clicked.connect(self.ChangeSetting)
            self.buttonsChange.show()  
            
            #button function
            if self.playersNum == 1:
                self.buttonsReset[0].clicked.connect(self.RestartOne)
                self.buttonsPhoto[0].clicked.connect(self.CorrectBaseOne)
                self.buttonsPause[0].clicked.connect(self.PauseOne)
            if self.playersNum == 2:
                self.buttonsReset[0].clicked.connect(self.RestartOne)
                self.buttonsReset[1].clicked.connect(self.RestartTwo)
                self.buttonsPhoto[0].clicked.connect(self.CorrectBaseOne)
                self.buttonsPhoto[1].clicked.connect(self.CorrectBaseTwo)
                self.buttonsPause[0].clicked.connect(self.PauseOne)
                self.buttonsPause[1].clicked.connect(self.PauseTwo)
            if self.playersNum == 3:
                self.buttonsReset[0].clicked.connect(self.RestartOne)
                self.buttonsReset[1].clicked.connect(self.RestartTwo)
                self.buttonsReset[2].clicked.connect(self.RestartThree)
                self.buttonsPhoto[0].clicked.connect(self.CorrectBaseOne)
                self.buttonsPhoto[1].clicked.connect(self.CorrectBaseTwo)
                self.buttonsPhoto[2].clicked.connect(self.CorrectBaseThree)
                self.buttonsPause[0].clicked.connect(self.PauseOne)
                self.buttonsPause[1].clicked.connect(self.PauseTwo)
                self.buttonsPause[2].clicked.connect(self.PauseThree)
                
            self.setWindowTitle('ChessGamer')
            self.setGeometry(100, 100, 520*self.playersNum, 590)
            self.setFixedSize(520*self.playersNum, 590)
            

            self.show()
        else:
            sendButton = QPushButton("Send",self)
        
            cancelButton = QPushButton('Exit',self)
            cancelButton.clicked.connect(qApp.quit)
            self.textBox = QTextEdit()
            self.textBox.setReadOnly(True)
        
            self.textEdit = QTextEdit()
        
            self.pic = QLabel()
        
        
            self.pic.setPixmap(QPixmap("images/BoardBase.png"))
            self.pic.resize(350,350)
            self.pic.show()
        
            self.debugBoard =chess.Board()
            if self.debug:
                print('this is board in init: ',self.debugBoard)
            sendButton.clicked.connect(self.DrawBoard)
        
            vbox = QVBoxLayout()
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            vbox.addStretch(1)
            hbox.addWidget(sendButton)
            hbox.addWidget(cancelButton)
            vbox.addWidget(self.pic)
            vbox.addWidget(self.textBox)
            vbox.addLayout(hbox)
            
       
        
            self.setGeometry(500, 300, 300, 200)
            self.setWindowTitle('ChessGamer')
            self.setLayout(vbox) 
            self.show()  
    
    
    def ChangeSetting(self):   
        
        self.close()
        self.__init__(False, 1)
        self.GameLoop()
        
        
    
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
       
    def DrawBoard(self,board,player):
        if self.debug:
            print("im in drawBoardCall")
            try:
                board = self.debugBoard
            except AttributeError:
                pass
        
        stringBoard=Board2String(board)
        boardPic = DrawBoardPic(stringBoard, self.debug)
        tmpImagename = "images/tmp"+str(player)+".png"    
        cv2.imwrite(tmpImagename,boardPic)
        
        self.chessboardDisplays[player-1].setPixmap(QPixmap(tmpImagename))
        self.chessboardDisplays[player-1].show()

    def DrawGui(self):

        if self.playersNum ==1:
            self.chessboardDisplays[0].setPixmap(QPixmap('images/tmp0.png'))
            self.chessboardDisplays[0].show()
        if self.playersNum ==2:
            self.chessboardDisplays[0].setPixmap(QPixmap('images/tmp0.png'))
            self.chessboardDisplays[0].show()
            self.chessboardDisplays[1].setPixmap(QPixmap('images/tmp1.png'))
            self.chessboardDisplays[1].show()
        if self.playersNum ==3:
            self.chessboardDisplays[0].setPixmap(QPixmap('images/tmp0.png'))
            self.chessboardDisplays[0].show()
            self.chessboardDisplays[1].setPixmap(QPixmap('images/tmp1.png'))
            self.chessboardDisplays[1].show()
            self.chessboardDisplays[2].setPixmap(QPixmap('images/tmp2.png'))
            self.chessboardDisplays[2].show()
   
    def Draw(self,board,player):
        
        if player ==0:
            self.garbage = 0
            self.drawThread = DrawThread(board,player)
            self.drawThread.finished.connect(self.DrawGui)
            self.drawThread.start()
            
        if player ==1:
            self.garbage = 1
            self.drawThread1 = DrawThread(board,player)
            self.drawThread1.finished.connect(self.DrawGui)
            self.drawThread1.start()
        if player ==2:
            self.garbage = 2
            self.drawThread2 = DrawThread(board,player)
            self.drawThread2.finished.connect(self.DrawGui)
            self.drawThread2.start()
     
    def GainDataFromThread(self,strData):    
        self.gainedData=strData
        #print('this is data in main loop',strData)
        
    def MoveDone(self,player):
        self.RobotMoveDone[player]=True
        self.GenerateMoveDone[player] = True
        
        
        if self.playersNum>1:
            
            
            if self.curPlayer[0]==0 and self.playersNum==2:
                self.curPlayer[0]=1
            elif self.curPlayer[0]==1 and self.playersNum==2:
                self.curPlayer[0]=0
            
                
        if self.playersNum==3:        
            
            if self.curPlayer[0]==0  and self.curPlayer[1]==1:
                self.curPlayer[0]=1
            elif self.curPlayer[0]==1  and self.curPlayer[1]==1:
                self.curPlayer[0]=2
                self.curPlayer[1]=0
            elif self.curPlayer[0]==2  and self.curPlayer[1]==0:
                self.curPlayer[0]=1
            elif self.curPlayer[0]==1  and self.curPlayer[1]==0:
                self.curPlayer[0]=0
                self.curPlayer[1]=1
        
    def RestartDone(self,player):
        #print('Restart Done')
        self.playerStatus[player][0] = chess.Board()
        #print('2',self.playerStatus[player][0].fen())
        self.RobotMoveDone[player] = True
        self.GenerateMoveDone[player] = True
        self.restartStatus[player]=False
        self.playerStatus[player][4] = False
 
 
    def PlayerCheckDone(self,data):
        
        player = int(data[1])
        if data[0]=='0':
            '''
            if first data symbol 0  then no turn done
            '''
            if self.curPlayer[0]==0:
            
                self.robot.set_digital_out(dataStructers.OutButtonOne,True)
            elif self.curPlayer[0]==1:
                self.robot.set_digital_out(dataStructers.OutButtonTwo,True)
            elif self.curPlayer[0]==2:
                self.robot.set_digital_out(dataStructers.OutButtonThree,True)
                
            if self.playersNum>1:
            
            
                if self.curPlayer[0]==0 and self.playersNum==2:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1 and self.playersNum==2:
                    self.curPlayer[0]=0
            
                
            if self.playersNum==3:        
            
                if self.curPlayer[0]==0  and self.curPlayer[1]==1:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1  and self.curPlayer[1]==1:
                    self.curPlayer[0]=2
                    self.curPlayer[1]=0
                elif self.curPlayer[0]==2  and self.curPlayer[1]==0:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1  and self.curPlayer[1]==0:
                    self.curPlayer[0]=0
                    self.curPlayer[1]=1
            
            self.GenerateMoveDone[player] = True
                
        elif data[0]=='1':
            '''
            Player has made a move, need to push board
            
            '''
            self.robot.set_digital_out(dataStructers.led_red,False)
            self.robot.set_digital_out(dataStructers.led_blue,False)
            filename = 'player'+str(player)+'.txt'
            file = open(filename,'w')
            a = data[2:data.find('-')]
            b = data[data.find('-')+1:len(data)]
            uci = square2Uci(int(a)) +square2Uci(int(b))
            move= chess.Move.from_uci(uci)
            self.playerStatus[player][0].push(move)
            file.write(self.playerStatus[player][0].fen())
            file.close()
            self.GenerateMoveDone[player] = True
            
            
        
        elif data[0]=='2':
            '''
            something gone wrong and need to be corrected
            '''
            print('Something went wrong')
            if self.curPlayer[0]==0:
            
                self.robot.set_digital_out(dataStructers.OutButtonOne,True)
            elif self.curPlayer[0]==1:
                self.robot.set_digital_out(dataStructers.OutButtonTwo,True)
            elif self.curPlayer[0]==2:
                self.robot.set_digital_out(dataStructers.OutButtonThree,True)
            if self.playersNum>1:
            
            
                if self.curPlayer[0]==0 and self.playersNum==2:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1 and self.playersNum==2:
                    self.curPlayer[0]=0
            
                
            if self.playersNum==3:        
            
                if self.curPlayer[0]==0  and self.curPlayer[1]==1:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1  and self.curPlayer[1]==1:
                    self.curPlayer[0]=2
                    self.curPlayer[1]=0
                elif self.curPlayer[0]==2  and self.curPlayer[1]==0:
                    self.curPlayer[0]=1
                elif self.curPlayer[0]==1  and self.curPlayer[1]==0:
                    self.curPlayer[0]=0
                    self.curPlayer[1]=1
            
            self.GenerateMoveDone[player] = True
            
            
    def LoopThreadDone(self):
        
        currentPlayer = self.curPlayer[0]
        self.robot.set_digital_out(dataStructers.led_red,False)
        self.robot.set_digital_out(dataStructers.led_blue,False)
        self.CheckPermission[currentPlayer]=False
        
        
        
        
        if self.RobotMoveDone[currentPlayer]:
            
            prevBoard=self.playerStatus[currentPlayer][0].copy()
            a = int(self.gainedData[0:self.gainedData.find("-")])
            
            if self.gainedData.count("+")==1:
                #c = self.gainedData[-1]
                c = FindPosiblePromotion(self.playerStatus[self.curPlayer[0]][0],self.gainedData[-1])
                b = int(self.gainedData[self.gainedData.find("-")+1:self.gainedData.find("+")])
                uci = square2Uci(a)+square2Uci(b)+c
            else:
                c = ''
                b = int(self.gainedData[self.gainedData.find("-")+1:len(self.gainedData)])
                uci = square2Uci(a)+square2Uci(b)
            move=chess.Move.from_uci(uci)
            
            
            
            if prevBoard.is_castling(move):
                castling = 1
            else:
                castling = 0
            
            filename = 'player'+str(currentPlayer)+'.txt'
            file = open(filename,'w')
            self.playerStatus[self.curPlayer[0]][0].push(move)
            file.write(self.playerStatus[self.curPlayer[0]][0].fen())
            file.close()
            boardWithMove = self.playerStatus[self.curPlayer[0]][0]
            #
            #print(boardWithMove.fen())
            #
            if self.playerStatus[currentPlayer][1]:
                if self.playerStatus[currentPlayer][0].is_check():
                
                    self.robot.set_digital_out(dataStructers.led_red,True)
                    self.robot.set_digital_out(dataStructers.led_blue,True)
                    
            self.RobotMoveDone[currentPlayer]=False
            if self.playerStatus[currentPlayer][1]==True:
                robotMoveThread=RoboWorker(currentPlayer,[a,b,c],[prevBoard,boardWithMove],self.robot,castling,self.camera) 
            elif self.playerStatus[currentPlayer][1]==False:
                castling+=3
                robotMoveThread=RoboWorker(currentPlayer,[a,b,c],[prevBoard,boardWithMove],self.robot,castling,self.camera)
            robotMoveThread.doneSignal.connect(self.MoveDone)
            robotMoveThread.start()
            
           
           
            
            if BoardTurn(prevBoard) =='w':
                message = 'Player move: '+uci
                self.logs[self.curPlayer[0]].setAlignment(QtCore.Qt.AlignLeft)
                self.logs[self.curPlayer[0]].append(message)
            else:
                message = 'Robot move: '+uci
                self.logs[self.curPlayer[0]].setAlignment(QtCore.Qt.AlignRight)
                self.logs[self.curPlayer[0]].append(message)
            
        self.Draw(self.playerStatus[currentPlayer][0],currentPlayer)
        
        #self.GenerateMoveDone[player]= True
        
        
        
        
    def Loop(self):           
            
            
            currentPlayer = self.curPlayer[0]
            #self.Draw(self.playerStatus[currentPlayer][0],currentPlayer)
            #print('Run gameloop')
            #print('Current turn',BoardTurn(self.playerStatus[self.curPlayer[0]][0]))
            
            if self.GenerateMoveDone[currentPlayer]:
                '''
                    If move Generation from player or Ai is finished, than game may be continued
                '''
                if self.playerStatus[currentPlayer][0].is_game_over() ==True or self.playerStatus[currentPlayer][4] == True:
                #print('Game is finished')
                    '''
                    If game is finished, then it must be restarted
                    '''
                    if self.playerStatus[currentPlayer][5]!=True:
                        
                        self.logs[currentPlayer].append("Game over")
                        
                        
                        print('Restart Started')
                        self.GenerateMoveDone[currentPlayer] = False
                        
                            
                        endBoard = self.playerStatus[currentPlayer][0].copy()
                        if self.playerStatus[self.curPlayer[0]][1]:
                            restartThread = RoboWorker(currentPlayer,[0,0,''],[endBoard,0],self.robot,6,self.camera)
                        else:
                            restartThread = RoboWorker(currentPlayer,[0,0,''],[endBoard,0],self.robot,2,self.camera)
                        restartThread.restarSignal[int].connect(self.RestartDone)
                        #restartThread.restarSignal[int].connect(self.LoopThreadDone)
                        restartThread.start()
            
            
                elif self.playerStatus[currentPlayer][0].is_game_over() ==False and self.playerStatus[currentPlayer][5]==False:
                    '''
                    If a game  is not finished and not paused, then it needs to Get move from ai or from player
                    '''
                    
                    if self.restartStatus[currentPlayer]==False:
                        '''
                        some help to restart game board CHECK IT!!!!!!!!!!!!
                        '''
                        self.playerStatus[currentPlayer][0]=chess.Board()
                    
                                      
                        self.restartStatus[currentPlayer]=True
                    
                #print('1',self.playerStatus[currentPlayer][0].fen())
                
                    if BoardTurn(self.playerStatus[self.curPlayer[0]][0]) =='w':
                    #print("White Move")
                        self.curTurn[currentPlayer].setText('Current\n Turn:\n White')
                    
                        if self.playerStatus[self.curPlayer[0]][1]:
                        
                            '''
                            main human iteraction event
                            '''
                            #print('player Move')
                            
                            if self.CheckPermission[self.curPlayer[0]]:
                                
                                self.robot.set_digital_out(2+currentPlayer,False)
                                self.GenerateMoveDone[currentPlayer] = False
                                #print('1111111111111111111111111111')
                                checkPlayer = CheckBoard(self.curPlayer[0],self.playerStatus[currentPlayer][0],self.robot,self.camera,2)
                                checkPlayer.result[str].connect(self.PlayerCheckDone)
                                checkPlayer.start()
                                #print('222222222222222')
                                self.CheckPermission[self.curPlayer[0]] = False
                            else:
                                if self.playersNum>1:
            
            
                                    if self.curPlayer[0]==0 and self.playersNum==2:
                                        self.curPlayer[0]=1
                                    elif self.curPlayer[0]==1 and self.playersNum==2:
                                        self.curPlayer[0]=0
            
                
                                if self.playersNum==3:        
                                
                                    if self.curPlayer[0]==0  and self.curPlayer[1]==1:
                                        self.curPlayer[0]=1
                                    elif self.curPlayer[0]==1  and self.curPlayer[1]==1:
                                        self.curPlayer[0]=2
                                        self.curPlayer[1]=0
                                    elif self.curPlayer[0]==2  and self.curPlayer[1]==0:
                                        self.curPlayer[0]=1
                                    elif self.curPlayer[0]==1  and self.curPlayer[1]==0:
                                        self.curPlayer[0]=0
                                        self.curPlayer[1]=1
                                                
                            #wait for videosource
                        else:
                        
                            self.GenerateMoveDone[currentPlayer] = False
                        
                            print('Player is Ai making movement')
                        
                            gameThread = GameLoop(self.playerStatus[currentPlayer][0],self.playerStatus[currentPlayer][2],self.engine,currentPlayer)
                            gameThread.dataSignal[str].connect(self.GainDataFromThread)
                            gameThread.doneSignal[int].connect(self.LoopThreadDone)
                            self.robot.set_digital_out(dataStructers.led_blue,True)
                            if gameThread.isFinished:
                                gameThread.start()
                            
                    if BoardTurn(self.playerStatus[self.curPlayer[0]][0]) =='b':
                    #print('Black Move')
                            self.curTurn[currentPlayer].setText('Current\n Turn:\n Black')
                            
                            self.GenerateMoveDone[currentPlayer] = False
                            self.robot.set_digital_out(2+currentPlayer,False)
                            #print(' Robot Move')
                            gameThread1 = GameLoop(self.playerStatus[currentPlayer][0],self.playerStatus[currentPlayer][3],self.engine,currentPlayer)
                            gameThread1.dataSignal[str].connect(self.GainDataFromThread)
                            gameThread1.doneSignal[int].connect(self.LoopThreadDone)
                            self.robot.set_digital_out(dataStructers.led_blue,True)
                            if gameThread1.isFinished:
                                gameThread1.start()
                            self.robot.set_digital_out(2+currentPlayer,False)
#                     
#             if self.playersNum==1:
#                     self.curPlayer[0]=0
#             if self.playersNum==2:
#                     pass
#             if self.playersNum==3:
#                     pass
        
               
            
            
            #self.Draw(self.playerStatus[currentPlayer][0],currentPlayer)    
                
            
            
    def CorrectBaseOne(self):
        
        restartThread = CheckBoard(0,'',self.robot,self.camera,3)
        self.robot.set_digital_out(dataStructers.OutButtonOne, True)
        restartThread.start()   
    def CorrectBaseTwo(self):
        
        restartThread = CheckBoard(1,'',self.robot,self.camera,3)
        self.robot.set_digital_out(dataStructers.OutButtonTwo, True)
        restartThread.start()   
    def CorrectBaseThree(self):
        
        restartThread = CheckBoard(2,'',self.robot,self.camera,3)
        self.robot.set_digital_out(dataStructers.OutButtonThree, True)
        restartThread.start()   
        
    
    def StopGame(self,number):        
            print(number)
            
    def initPhotoDone(self,data):
        print(data)
        print('Init Photo done')
        self.GenerateMoveDone[self.curInt] = True    
        
        if self.curInt+1 ==self.playersNum:
            self.initDone =True
            if self.playerStatus[self.curInt-1][1]:
                self.robot.set_digital_out(2+self.curInt-1,True)
            else:
                self.robot.set_digital_out(2+self.curInt-1,False)
        self.curInt+=1
            
    def RestartOne(self):
        #self.playerStatus[0][0] = chess.Board()   
        self.playerStatus[0][4] = True
            
        self.isdone=False
       # t = 
        self.logs[0].append("Restart\n")
        self.Speaker("Перезапуск первого стола")
            
    def RestartTwo(self):
        #self.playerStatus[1][0] = chess.Board()       
        self.playerStatus[1][4] = True
        
        self.logs[1].append("Restart\n")
        self.Speaker("Перезапуск второго стола")
    
    def RestartThree(self):  
        #self.playerStatus[2][0] = chess.Board()     
        self.playerStatus[2][4] = True
        
        self.timer.start(0)        
        self.logs[2].append("Restart\n")
        self.Speaker("Перезапуск третьего стола")
            
    def PauseOne(self):
        if self.playerStatus[0][5]==False:
            self.playerStatus[0][5]=True
            self.buttonsPause[0].setText('Unpause')
            self.logs[0].append("Pause\n")
            self.Speaker("Поставлена пауза на первом игроке")
        elif self.playerStatus[0][5]==True:
            self.playerStatus[0][5]=False
            self.buttonsPause[0].setText('Pause')
            self.logs[0].append("Pause\n")
            self.Speaker("Игрок один Игра продолжается")
        
    def PauseTwo(self):
        if self.playerStatus[1][5]==False:
            self.playerStatus[1][5]=True
            self.buttonsPause[1].setText('Unpause')
            self.logs[1].append("Pause\n")
            self.Speaker("Поставлена пауза на втором игроке")
        elif self.playerStatus[1][5]==True:
            self.playerStatus[1][5]=False
            self.buttonsPause[1].setText('Pause')
            self.logs[1].append("Pause\n")
            self.Speaker("Игрок два Игра продолжается")
        
    def PauseThree(self):
        if self.playerStatus[2][5]==False:
            self.playerStatus[2][5]=True
            self.buttonsPause[2].setText('Unpause')
            self.logs[2].append("Pause\n")
            self.Speaker("Поставлена пауза на третьем игроке")
        elif self.playerStatus[2][5]==True:
            self.playerStatus[2][5]=False
            self.buttonsPause[2].setText('Pause')
            self.logs[2].append("Pause\n")
            self.Speaker("Игрок Три Игра продолжается")
                 
    def Speaker(self, text):     
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
        
    def InitPhoto(self):
        
        if self.initDone or self.playerStatus[self.curInt][1]==0:
            self.Loop()
            #print('init done')  
        elif self.initDone ==False and self.GenerateMoveDone[self.curInt]:
                
                makeFirstPhotoEvent = CheckBoard(self.curInt,self.playerStatus[self.curInt][0],self.robot,self.camera,1)
                makeFirstPhotoEvent.result[str].connect(self.initPhotoDone)
                makeFirstPhotoEvent.start()
                
        
    def ButtonPushed(self,player):
        self.CheckPermission[player]=True
    def checkButtons(self):
        print ('lets check button in game.py')
        if self.robot.get_digital_in(dataStructers.InButtonOne) == True:
            print ('Button for player one')
            self.CheckPermission[0]=True
        elif self.robot.get_digital_in(dataStructers.InButtonTwo) == True:
            print ('button for player two')
            self.CheckPermission[1]=True
        elif self.robot.get_digital_in(dataStructers.InButtonThree) == True:
            print ('button for player three')
            self.CheckPermission[2]=True  
    #def EmitSignal(self,event,signal, value):
    #    buttonCheckEvent = event
    #    if value == int:
    #        buttonCheckEvent.doneSignal[int].connect(signal)
    #    elif value == str:
    #        buttonCheckEvent.doneSignal[str].connect(signal)
    #    buttonCheckEvent.start()
    
    def GameLoop(self):
        
        self.playerStatus =[]
        self.engine = ChessEngine(False)
        boards = []
        #ButtonCheckEvent = ButtonCheck(self.robot)
        #ButtonCheckEvent.doneSignal[int].connect(self.ButtonPushed)
        #ButtonCheckEvent.start()
        #EmitSignal(ButtonCheck(self.robot),ButtonPushed, int)
        

        
        for i in range(3):
            
            '''
            playerStatus[i][j]
            i = player from 1 to 3
            j = 0-Current board
            j = 1 player Type: Ai or a human (true or 1 for human)
            j = 2 difficalty for robot ai
            j = 3 difficluty for player AI
            j = 4 gameOver status (True or false)
            j = 5 pause
            
            '''
            try:
                filename = 'player'+str(i)+'.txt'
                file = open(filename,'r')
                fen = file.read()
            except FileNotFoundError:
                fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            self.playerStatus.append([chess.Board(fen),self.players[i],self.difficulties[i],self.aiDifficulties[i],False,False])
            boards.append(chess.Board())  
            self.Draw(self.playerStatus[i][0],i)
        
        self.curInt = 0  
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.InitPhoto)
        self.timer.setInterval(300)
        self.timer.start(1)   
        
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.checkButtons)
        self.timer2.setInterval(300)
        self.timer2.start(1)
        
            
                    
            
            
        #print('playersStats',self.playerStatus)
#         
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.Loop)
#         self.timer.setInterval(300)
#         self.timer.start(1) 
#         
    
           
            
    
    
                


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
       
    game = MainGame(False,3)
    
    game.GameLoop()
    
    sys.exit(app.exec_())

    
