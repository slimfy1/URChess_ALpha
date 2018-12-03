import sys
import time

import urx
import cv2
from PyQt5.Qt import QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QGridLayout
from CamPhoto import *
import dataStructers
import threading
from InitAll import ConnectionList


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class InitScreenRobot(QDialog):
    def __init__(self, robot):
        super().__init__()

#         try:
#             while True:
#                 done = self.connect2Robot()
#                 if type(done)!='None':
#                     break
#         except TimeoutException:
#             pass
        self.baseOne = 0
        self.baseTwo = 0
        self.baseThree = 0
        self.JOne = 0
        self.JTwo = 0
        self.JThree = 0
        self.DropWOne = 0
        self.DropWTwo = 0
        self.DropWThree = 0
        self.DropBOne = 0
        self.DropBTwo = 0
        self.DropBThree = 0
        self.camOne = 0
        self.camTwo = 0
        self.camThree = 0

        self.robot = robot
        print("robot:", self.robot)    
        self.initUI()
        
    def click_and_crop(self, event, x, y):
        
        temp = self.image.copy()

        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True
 
    # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
        # draw a rectangle around the region of interest
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)
            roi = temp[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
            cv2.imshow("Selected Roi", roi)
            cv2.waitKey(0)
            #print(self.refPt)
            self.status = True

    def ReturnCoords(self, square):
        tick = 0
        res=[0,0]
        for x in range(8):
            for y in range(8):
                if tick ==square:
                    res[1]=x
                    res[0]=y
                
                tick+=1    
        
        return res

    def Roi(self, param, cam):
        
        self.status = False
        self.refPt = []
        self.cropping = True
        while True:
            ret, self.image = cam.read()
            img = self.image.copy()
            w,h,z = img.shape
            cv2.line(img,(0,int(w/2)),(h,int(w/2)),(255,0,0),2)
            cv2.line(img,(int(h/2),0),(int(h/2),w),(255,0,0),2)
            cv2.imshow('Correct camera pose',img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):
                break

        clone = self.image.copy()

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        
        cv2.imshow('image',self.image)
        cv2.waitKey(0)
        
        
        if len(self.refPt)==2:
            #print('refPt',self.refPt)
            refPt = self.refPt
            roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            w,h,z = roi.shape
            cv2.line(roi,(0,int(w/2)),(w,int(w/2)),(255,0,0),5)
            cv2.line(roi,(int(h/2),0),(int(h/2),h),(255,0,0),5)
            roi = cv2.resize(roi,(264,264))
            cv2.imwrite('images/tmpRoi'+ str(self.roiPlayer) +'.png',roi)
            if param ==1:
                self.roi.setPixmap(QPixmap("images/tmpRoi"+ str(self.roiPlayer) +".png"))
            
                if self.roiPlayer == 1:
                    self.playerOneRfPt = self.refPt
                    self.playerOneChessboard = self.robot.getj()
                elif self.roiPlayer == 2:
                    self.playerTwoRfPt = self.refPt
                    self.playerTwoChessboard = self.robot.getj()
                elif self.roiPlayer == 3:
                    self.playerThreeRfPt = self.refPt
                    self.playerThreeChessboard = self.robot.getj()
                
                self.coordinates = self.robot.getl()
                self.eventText.append("Player " + str(self.roiPlayer) + "\n")
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append('images/tmpRoi'+ str(self.roiPlayer) +'.png saved\n')
            
                #self.doneBtn.setEnabled(True)
                self.backBtn.setEnabled(True)
            elif param ==2:
                if self.roiPlayer ==1:
                    cv2.imwrite('images/cb1'+ str(self.roiPlayer) +'.bmp',roi)
                if self.roiPlayer ==2:
                    cv2.imwrite('images/cb2'+ str(self.roiPlayer) +'.bmp',roi)
                if self.roiPlayer ==3:
                    cv2.imwrite('images/cb3'+ str(self.roiPlayer) +'.bmp',roi)
    
    def initUI(self):
        grid = QGridLayout()
        
        
        lblOne = QLabel("Correct one",self)
        lblTwo = QLabel("Correct two",self)
        lblThree = QLabel("Correct three",self)
        grid.addWidget(lblOne,0,0)
        grid.addWidget(lblTwo,0,1)
        grid.addWidget(lblThree,0,2)
        
        btnOneMain = QPushButton('Base One pose',self)
        btnOneMain.resize(100,50)
        btnOneMain.clicked.connect(self.BaseOneGet)
        grid.addWidget(btnOneMain,1,0)
        
        btnOneJ = QPushButton('J One',self)
        btnOneJ.resize(100,50)
        btnOneJ.clicked.connect(self.JOneGet)
        grid.addWidget(btnOneJ,2,0)
        
        btnOneDropW = QPushButton('Drop One White',self)
        btnOneDropW.resize(100,50)
        btnOneDropW.clicked.connect(self.DropWOneGet)
        grid.addWidget(btnOneDropW,3,0)
        
        btnOneDropB = QPushButton('Drop One Black',self)
        btnOneDropB.resize(100,50)
        btnOneDropB.clicked.connect(self.DropBOneGet)
        grid.addWidget(btnOneDropB,4,0)
        
        btnOneCam = QPushButton('Cam One',self)
        btnOneCam.resize(100,50)
        btnOneCam.clicked.connect(self.CamOneGet)
        grid.addWidget(btnOneCam,5,0)
        
        btnTwoMain = QPushButton('Base Two pose',self)
        btnTwoMain.resize(100,50)
        btnTwoMain.clicked.connect(self.BaseTwoGet)
        grid.addWidget(btnTwoMain,1,1)
        
        btnTwoJ = QPushButton('J Two',self)
        btnTwoJ.resize(100,50)
        btnTwoJ.clicked.connect(self.JTwoGet)
        grid.addWidget(btnTwoJ,2,1)
        
        btnTwoDropW = QPushButton('Drop Two White ',self)
        btnTwoDropW.resize(100,50)
        btnTwoDropW.clicked.connect(self.DropWTwoGet)
        grid.addWidget(btnTwoDropW,3,1)
        
        btnTwoDropB = QPushButton('Drop Two Black ',self)
        btnTwoDropB.resize(100,50)
        btnTwoDropB.clicked.connect(self.DropBTwoGet)
        grid.addWidget(btnTwoDropB,4,1)
        
        btnTwoCam = QPushButton('Cam Two',self)
        btnTwoCam.resize(100,50)
        btnTwoCam.clicked.connect(self.CamTwoGet)
        grid.addWidget(btnTwoCam,5,1)
        
        btnThreeMain = QPushButton('Base Three',self)
        btnThreeMain.resize(100,50)
        btnThreeMain.clicked.connect(self.BaseThreeGet)
        grid.addWidget(btnThreeMain,1,2)
        
        btnThreeJ = QPushButton('J Three',self)
        btnThreeJ.resize(100,50)
        btnThreeJ.clicked.connect(self.JThreeGet)
        grid.addWidget(btnThreeJ,2,2)
        
        btnThreeDropW = QPushButton('Drop Three White ',self)
        btnThreeDropW.resize(100,50)
        btnThreeDropW.clicked.connect(self.DropWThreeGet)
        grid.addWidget(btnThreeDropW,3,2)
        
        btnThreeDropB = QPushButton('Drop Three Black',self)
        btnThreeDropB.resize(100,50)
        btnThreeDropB.clicked.connect(self.DropBThreeGet)
        grid.addWidget(btnThreeDropB,4,2)
        
        btnThreeCam = QPushButton('Cam Three',self)
        btnThreeCam.resize(100,50)
        btnThreeCam.clicked.connect(self.CamThreeGet)
        grid.addWidget(btnThreeCam,5,2)
        
        
        lblGoTo = QLabel("GoTo buttons",self)
        grid.addWidget(lblGoTo,6,1)
        
        btnOneMainGT = QPushButton('GoTo Base one',self)
        btnOneMainGT.resize(100,50)
        btnOneMainGT.clicked.connect(self.GTbaseOne)
        grid.addWidget(btnOneMainGT,7,0)
        
        btnOneJGT = QPushButton('GoTo J One',self)
        btnOneJGT.resize(100,50)
        btnOneJGT.clicked.connect(self.GTJOne)
        grid.addWidget(btnOneJGT,8,0)
        
        btnOneDropGT = QPushButton('GoTo Drop One ',self)
        btnOneDropGT.resize(100,50)
        btnOneDropGT.clicked.connect(self.GTDropOne)
        grid.addWidget(btnOneDropGT,9,0)
        
        btnOneCamGT = QPushButton('GoTo Cam Two',self)
        btnOneCamGT.resize(100,50)
        btnOneCamGT.clicked.connect(self.GTnumbOne)
        grid.addWidget(btnOneCamGT,10,0)
        
        btnTwoMainGT = QPushButton('GT Base Two pose',self)
        btnTwoMainGT.resize(100,50)
        btnTwoMainGT.clicked.connect(self.GTbaseTwo)
        grid.addWidget(btnTwoMainGT,7,1)
        
        btnTwoJGT = QPushButton('GT J Two',self)
        btnTwoJGT.resize(100,50)
        btnTwoJGT.clicked.connect(self.GTJTwo)
        grid.addWidget(btnTwoJGT,8,1)
        
        btnTwoDropGT = QPushButton('GT Drop Two ',self)
        btnTwoDropGT.resize(100,50)
        btnTwoDropGT.clicked.connect(self.GTDropTwo)
        grid.addWidget(btnTwoDropGT,9,1)
        
        btnTwoCamGT = QPushButton('GT Cam Two',self)
        btnTwoCamGT.resize(100,50)
        btnTwoCamGT.clicked.connect(self.GTnumbTwo)
        grid.addWidget(btnTwoCamGT,10,1)
        
        btnThreeMainGT = QPushButton('GT Base Three',self)
        btnThreeMainGT.resize(100,50)
        btnThreeMainGT.clicked.connect(self.GTbaseThree)
        grid.addWidget(btnThreeMainGT,7,2)
        
        btnThreeJGT = QPushButton('GT J Three',self)
        btnThreeJGT.resize(100,50)
        btnThreeJGT.clicked.connect(self.GTJThree)
        grid.addWidget(btnThreeJGT,8,2)
        
        btnThreeDropGT = QPushButton('GT Drop Three ',self)
        btnThreeDropGT.resize(100,50)
        btnThreeDropGT.clicked.connect(self.GTDropThree)
        grid.addWidget(btnThreeDropGT,9,2)
        
        btnThreeCamGT = QPushButton('GTCam Three',self)
        btnThreeCamGT.resize(100,50)
        btnThreeCamGT.clicked.connect(self.GTnumbTr)
        grid.addWidget(btnThreeCamGT,10,2)
        
        lblCOne = QLabel("Tests",self)
        
        grid.addWidget(lblCOne,11,1)
        
        
        #hbox= QHBoxLayout(self) GetPhotoOne
        
        btnGetPhotoOne = QPushButton('Get Photo 1',self)
        btnGetPhotoOne.resize(100,50)
        btnGetPhotoOne.clicked.connect(self.GetPhoto)
        grid.addWidget(btnGetPhotoOne,12,0)
        
        btnGetPhotoTwo = QPushButton('Get Photo 2',self)
        btnGetPhotoTwo.resize(100,50)
        btnGetPhotoTwo.clicked.connect(self.GetPhoto)
        grid.addWidget(btnGetPhotoTwo,12,1)
        
        btnGetPhotoThree = QPushButton('Get Photo 3',self)
        btnGetPhotoThree.resize(100,50)
        btnGetPhotoThree.clicked.connect(self.GetPhoto)
        grid.addWidget(btnGetPhotoThree,12,2)
        
        
        
        btnTestBoardOne = QPushButton('Test board one',self)
        btnTestBoardOne.resize(100,50)
        btnTestBoardOne.clicked.connect(self.TestBoardOne)
        grid.addWidget(btnTestBoardOne,13,0)
        
        btnTestBoardTwo = QPushButton('Test board two',self)
        btnTestBoardTwo.resize(100,50)
        btnTestBoardTwo.clicked.connect(self.TestBoardTwo)
        grid.addWidget(btnTestBoardTwo,13,1)
        
        btnTestBoardThree = QPushButton('Test board three',self)
        btnTestBoardThree.resize(100,50)
        btnTestBoardThree.clicked.connect(self.TestBoardThree)
        grid.addWidget(btnTestBoardThree,13,2)

        freeDrive = QPushButton('Run freedrive ', self)
        freeDrive.resize(100, 50)
        freeDrive.clicked.connect(self.set_freeDrive)
        grid.addWidget(freeDrive, 14, 0)

        self.Screen = QLabel(self)
        self.Screen.resize(400,400)
        self.Screen.setPixmap(QPixmap("images/base0.bmp"))
        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.Screen)
        #vbox.addLayout(hbox)
        
        self.setLayout(vbox) 
        self.show()

    def set_freeDrive(self):
        self.robot.set_freedrive(True)

    def WriteData(self,lbl1,lbl2,data,param):
        #print('write data')
        lst = {1:"playerOneJPose",2:"playerOneLPose",3:"playerOneCamChessboard", 4:"figuresDropOneWhite",5: "figuresDropOneBlack",6:"playerOneRfPt",7:"playerTwoJPose",8:"playerTwoLPose",
            9:"playerTwoCamChessboard",10:"figuresDropTwoWhite",11:"figuresDropTwoBlack",12:"playerTwoRfPt",13:"playerThreeJPose",14:"playerThreeLPose",
            15:"playerThreeCamChessboard", 16:"figuresDropThreeWhite", 17:"figuresDropThreeBlack", 18:"playerThreeRfPt"}
        file = open('dataStructers.py','r')
        #print(file)
        fileData = file.read()
        #print(fileData)
        firstPart=fileData[0:fileData.find(lbl1)+4]
        #print('first part',firstPart)
        secondPart = fileData[fileData.find(lbl2):len(fileData)]
        file.close()
        file = open('dataStructers.py','w')
        file.write(firstPart)
        file.write("\n"+lst[param]+ '=' + str(data) + "\n")
        file.write(secondPart)
        file.close
    
    def BaseOneGet(self):
        self.baseOne= self.robot.getl()
        #self.baseOne = [1,1,1,1,1,1]
        self.WriteData('#*12','#*13',self.baseOne,2)

    def BaseTwoGet(self):
        self.baseTwo= self.robot.getl()
        #self.baseTwo = [1,2,1,1,1,1]
        self.WriteData('#*22','#*23',self.baseTwo,8)
        
    def BaseThreeGet(self):
        self.baseThree= self.robot.getl()
        #self.baseThree =[1,3,1,1,1,1]
        self.WriteData('#*32','#*33',self.baseThree,14)
        
    def JOneGet(self):
        self.JOne= self.robot.getj()
        #self.JOne =[1,4,1,1,1,1]
        self.WriteData('#*11','#*12',self.JOne,1)

    def JTwoGet(self):
        self.JTwo= self.robot.getj()
        #self.JTwo =[1,3,2,1,1,1]
        self.WriteData('#*21','#*22',self.JTwo,7)
        
    def JThreeGet(self):
        self.JThree= self.robot.getj()
        #self.JThree =[1,3,1,1,1,5]
        self.WriteData('#*31','#*32',self.JThree,13)
    #    ==================================
    def DropWOneGet(self):
        self.DropWOne= self.robot.getl()
        #self.DropWOne =[7,3,1,1,1,1]
        self.WriteData('#*14','#*15',self.DropWOne,4)

    def DropWTwoGet(self):
        self.DropWTwo= self.robot.getl()
        #self.DropWTwo =[1,3,1,8,1,1]
        self.WriteData('#*24','#*25',self.DropWTwo,10)
        
    def DropWThreeGet(self):
        self.DropWThree= self.robot.getl()
        #self.DropWThree =[1,3,1,8,8,1]
        self.WriteData('#*34','#*35',self.DropWThree,16)
    # ==============================   
    def DropBOneGet(self):
        self.DropBOne= self.robot.getl()
        #self.DropBOne =[1,3,1,2,8,1]
        self.WriteData('#*15','#*16',self.DropBOne,5)

    def DropBTwoGet(self):
        self.DropBTwo= self.robot.getl()
        #self.DropBTwo =[5,3,1,2,8,1]
        self.WriteData('#*25','#*26',self.DropBTwo,11)
        
    def DropBThreeGet(self):
        self.DropBThree= self.robot.getl()
        #self.DropBThree =[1111111,3,1,2,8,1]
        self.WriteData('#*35','#*36',self.DropBThree,17)

    def CamOneGet(self):      
        self.camOne= self.robot.getj()
        #self.camOne =[1111111,3,0,2,0,222222]
        self.WriteData('#*13','#*14',self.camOne,3) 

    def CamTwoGet(self):      
        self.camTwo= self.robot.getj()
        #self.camTwo =[1111111,3,0,2,0,1]
        self.WriteData('#*23','#*24',self.camTwo,9) 
        
    def CamThreeGet(self):      
        self.camThree= self.robot.getj()
        #self.camThree =[1111111,3,'fffff',2,0,1]
        self.WriteData('#*33','#*34',self.camThree,15)
        
    def GTbaseOne(self):
        if self.baseOne ==0:
            self.robot.movel(dataStructers.playerOneLPose,acc=0.3,vel=0.3)
        else:
            self.robot.movel(self.baseOne,acc=0.3,vel=0.3)

    def GTbaseTwo(self):
        if self.baseTwo ==0:
            self.robot.movel(dataStructers.playerTwoLPose,acc=0.3,vel=0.3)
        else:
            self.robot.movel(self.baseTwo,acc=0.3,vel=0.3)

    def GTbaseThree(self):
        if self.baseThree ==0:
            self.robot.movel(dataStructers.playerThreeLPose,acc=0.3,vel=0.3)
        else:
            self.robot.movel(self.baseThree,acc=0.3,vel=0.3)

    def GTJOne(self):
        if self.JOne == 0:
            self.robot.movej(dataStructers.playerOneJPose,acc=0.3,vel=0.3)
        else:
            self.robot.movej(self.JOne,acc=0.3,vel=0.3)

    def GTJTwo(self):
        if self.JTwo ==0:
            self.robot.movej(dataStructers.playerTwoJPose,acc=0.3,vel=0.3)
        else:
            self.robot.movel(self.JTwo,acc=0.3,vel=0.3)

    def GTJThree(self):
        if self.JThree ==0:
            self.robot.movel(dataStructers.playerThreeJPose,acc=0.3,vel=0.3)
        else:
            self.robot.movel(self.JThree,acc=0.3,vel=0.3)  
             
    def GTDropOne(self):
        if self.DropWOne ==0:
            pose = dataStructers.figuresDropOneWhite
        else:
            pose = self.DropWOne
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        pose[2]-=0.08 
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        
        if self.DropBOne ==0:
            pose = dataStructers.figuresDropOneBlack
        else:
            pose = self.DropBOne
        
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        pose[2]-=0.08 
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
    
    def GTDropTwo(self):
        if self.DropWTwo ==0:
            pose = dataStructers.figuresDropTwoWhite
        else:
            pose = self.DropWTwo
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        pose[2]-=0.08 
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        
        if self.DropBTwo ==0:
            pose = dataStructers.figuresDropTwoBlack
        else:
            pose = self.DropBTwo
        
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        pose[2]-=0.08 
        self.robot.movel(pose,acc=0.3,vel=0.3) 
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
    
    def GTDropThree(self):
        if self.DropWThree ==0:
            pose = dataStructers.figuresDropThreeWhite
        else:
            pose = self.DropWThree
        pose[2]+=0.08
        self.robot.movel(pose, acc=0.3, vel=0.3)
        pose[2]-=0.08 
        self.robot.movel(pose, acc=0.3, vel=0.3)
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose, acc=0.3, vel=0.3)
        
        if self.DropBThree ==0:
            pose = dataStructers.figuresDropThreeBlack
        else:
            pose = self.DropBThree
        
        pose[2]+=0.08
        self.robot.movel(pose, acc=0.3, vel=0.3)
        pose[2]-=0.08 
        self.robot.movel(pose, acc=0.3, vel=0.3)
        time.sleep(2)
        pose[2]+=0.08
        self.robot.movel(pose,acc=0.3,vel=0.3) 
    
    def GTCam(self,gtnumb):
        if gtnumb == 1:
            if self.camOne == 0:
                self.robot.movej(dataStructers.playerOneCamChessboard, acc=0.3, vel=0.3)
            else:
                self.robot.movej(self.camOne, acc=0.3, vel=0.3)
        if gtnumb == 2:
            if self.camTwo == 0:
                self.robot.movej(dataStructers.playerTwoCamChessboard, acc=0.3, vel=0.3)
            else:
                self.robot.movej(self.camTwo, acc=0.3, vel=0.3)
        if gtnumb == 3:
            if self.camThree == 0:
                self.robot.movej(dataStructers.playerThreeCamChessboard, acc=0.3, vel=0.3)
            else:
                self.robot.movej(self.camThree, acc=0.3, vel=0.3)

    def GTnumbOne(self):
        gtnumb = int('1')
        self.GTCam(gtnumb)

    def GTnumbTwo(self):
        gtnumb = int('2')
        self.GTCam(gtnumb)

    def GTnumbTr(self):
        gtnumb = int('3')
        self.GTCam(gtnumb)

    def TestBoardOne(self):
        if self.baseOne ==0:
            pose = dataStructers.playerOneLPose
        else:
            pose = self.baseOne
            
        for i in range(63):
            res = self.ReturnCoords(i)
            p = pose.copy()
            deltaX = dataStructers.chessboard_squareX
            deltaY = dataStructers.chessboard_squareY
            p[0]=p[0] - deltaX*res[1]
            p[1]=p[1] + deltaY*res[0]
            self.robot.movel(p,vel =0.4,acc=0.4)
    
    def TestBoardTwo(self):
        if self.baseTwo ==0:
            pose = dataStructers.playerTwoLPose
        else:
            pose = self.baseTwo
            
        for i in range(63):
            res = self.ReturnCoords(i)
            p = pose.copy()
            deltaX = dataStructers.chessboard_squareX
            deltaY = dataStructers.chessboard_squareY
            p[0]=p[0] - deltaX*res[0]
            p[1]=p[1] - deltaY*res[1]
            self.robot.movel(p,vel =0.4,acc=0.4)

    def TestBoardThree(self):
        if self.baseThree ==0:
            pose = dataStructers.playerThreeLPose
        else:
            pose = self.baseThree
            
        for i in range(63):
            res = self.ReturnCoords(i)
            p = pose.copy()
            deltaX = dataStructers.chessboard_squareX
            deltaY = dataStructers.chessboard_squareY
            p[0]=p[0] + deltaX*res[1]
            p[1]=p[1] - deltaY*res[0]
            self.robot.movel(p,vel =0.4,acc=0.4)
    
    def GetPhoto(self):

        MakePt = CamWork()
        MakePt.MakePhotoBoard("ts")
        pix = QPixmap('ts.png')
        self.Screen.setPixmap(pix)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    robot =[]
    #robot = FakeRobot('ip', 1)
    #robot = urx.Robot("192.168.0.20", use_rt=True)
    robotcon = ConnectionList()
    robot = robotcon.connect2Robot()
    ex = InitScreenRobot(robot)

    sys.exit(app.exec_())
    #playerOneRfPt
