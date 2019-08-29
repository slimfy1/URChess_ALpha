import cv2
import numpy as np
import dataStructers
from PIL import Image
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import time
import chess

def ButtonLed(GenerateMoveDone, robot):
    if GenerateMoveDone[0]==True:
        self.robot.set_digital_out(1, True)
    else:
        self.robot.set_digital_our(1, False)
    
        
def FindPosiblePromotion(board,calledPromotionFigure):
    
    stringBoard = Board2String(board)
    if calledPromotionFigure in ('q','Q'):
        if stringBoard.find(calledPromotionFigure)==-1:
                
            return (calledPromotionFigure)
    else:
        if calledPromotionFigure in ('R','N','B'):
            for i in ('R','B','N'):
                if stringBoard.find(i)<2:
                    return(i)
        for i in ('r','b','n'):
                if stringBoard.find(i)<2:
                    return(i)
                    
                
    


def square2Uci(number):
    ''' Returns square in letter+number style(e2) from a number of squre'''
    return(dataStructers.boardStructure[number])

def GetLPlayerPose(player,figure):
    
    if figure in ['P','R','K','Q','N','B']:
        side = 'W'
    elif figure in ['p','r','k','q','n','b']:
        side = 'B'
    if player ==0:
        if side =='w' or side =='W':
            return(dataStructers.figuresDropOneWhite)
        if side =='b' or side =='B':
            return(dataStructers.figuresDropOneBlack)
    elif player ==1:
        if side =='w' or side =='W':
            return(dataStructers.figuresDropTwoWhite)
        if side =='b' or side =='B':
            return(dataStructers.figuresDropTwoBlack)
    elif player ==2:
        if side =='w' or side =='W':
            return(dataStructers.figuresDropThreeWhite)
        if side =='b' or side =='B':
            return(dataStructers.figuresDropThreeBlack)
    
def BoardTurnNumber(board):
    ''' Returns a turn number from gameBoard'''
    strinboard = board.fen()
    base = int(strinboard[strinboard.rfind(' '):len(strinboard)])
    turn = BoardTurn(board)
    if turn=='w':
        base= base*2-1
    elif turn =='b' :
        base = base*2
    
    return(base)

def Board2String(board):
    ''' Returns moving side White or Black'''
    stringBoard  = board.fen()
    #print(stringBoard)
    return(stringBoard[0:stringBoard.find(" ")])

def BoardTurn(board):
    ''' Returns a chessboard in string format'''
    stringBoard  = board.fen()
    return(stringBoard[stringBoard.find(" ")+1])

def Picture2List(cropedImage,sizeFactor=False):

    ''' convert String board to a list type '''
    
    data = [i for i in range(64)]
    #cropedImage =cv2.cvtColor(cropedImage,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('img',cropedImage)
    tick =0
    w,h= cropedImage.shape
    w= int(w/8)
    h= int(h/8)
    wc = int(w/2)
    hc = int(h/2)
    if sizeFactor:
        pass
    else:
        sizeFactor = int(wc/2)
    
    
    for x in range(8):
            base = 56-(8*x)
            
            for y in range(8):
                tick =base+y
                data[tick]= cropedImage[(wc-(wc-sizeFactor))+w*x:(wc+(wc-sizeFactor))+w*x,
                                        (hc-(hc-sizeFactor))+h*y:(hc+(hc-sizeFactor))+h*y]
                
                
                                
    return(data)     

def stringBoard2Struct(stringBoard,debug=False):
    
    ''' convert String board to a list type '''
    data = [i for i in range(64)]
    
    tick =0
    stringPos = 0
    ticksTofig = 0
    status = True
    
    for x in range(8):
            base = 56-(8*x)
            
            for y in range(8):
                tick =base+y
                
                try:
                    if (stringBoard[stringPos] == "/" or stringBoard[stringPos] == "~" )and stringPos<=len(stringBoard):
                        stringPos+=1
                    
                    try:
                        if status:
                            ticksTofig = int(stringBoard[stringPos])
                        if debug:    
                            print('this is ticks to fig: ',ticksTofig)
                    except ValueError:
                            pass
                         
                except IndexError:
                    pass
                
                #print(tick)
                
                if ticksTofig==0:
                            pass
                            data[tick]=stringBoard[stringPos]
                else:
                            pass
                            ticksTofig-=1
                            data[tick]= 0
                            status = False
                
                   
                        
                #tick += 1
                if debug:
                    print ('this is tick: ',tick)
               
                    if stringPos<=len(stringBoard):
                        try:
                            print('this is stringletter: ',stringBoard[stringPos])
                        
                        except IndexError:
                            pass
                if ticksTofig==0:
                    stringPos+=1
                    status = True
                
    return(data)           

def FindPosiblePromotion(board,calledPromotionFigure):
    stringBoard = Board2String(board)
    struct = stringBoard2Struct(stringBoard)
    l1 = ('Q','R','B','N')
    l2 = ('q','r','b','n')
    print("174")
    '''
    check white or black and set start from called function
    '''
    
    t = 0
    
    
    while t<= len(l1)-1:
        
        if calledPromotionFigure in l1:
    
            target = l1[t]
        else:
            target = l2[t]
    
        
        result = 0
    
        if target in ('q','Q'):
            if struct.count(target)==0:
                
                result =target
        else:
            if target in ('R','N','B'):
                for i in ('R','B','N'):
                    if struct.count(target)<2:
                    
                        result = i
            else:
                for i in ('r','b','n'):
                    if struct.count(target)<2:
                        result = i
        if result:
            print("dsaf",target)
            return(target)
        else:
            t+=1
    if result==0 and t==3:
        return('f31r')
        print(target)
    

def DrawBoardPic(stringBoard,debug=False):
        ''' This fucntion generates a temerary image of a player board from a string'''
        #print("let`s run function")
        picStruct = {'r':'images/Chess_rdt60.png',
                     'n':'images/Chess_ndt60.png',
                     'b':'images/Chess_bdt60.png',
                     'q':'images/Chess_qdt60.png',
                     'k':'images/Chess_kdt60.png',
                     'p':'images/Chess_pdt60.png',
                     'R':'images/Chess_rlt60.png',
                     'N':'images/Chess_nlt60.png',
                     'B':'images/Chess_blt60.png',
                     'Q':'images/Chess_qlt60.png',
                     'K':'images/Chess_klt60.png',
                     'P':'images/Chess_plt60.png'}
    
        fontWhite = cv2.imread("images/white_square.png")
        fontBlack = cv2.imread("images/brown_square.png")  
        boardPic = np.zeros((400,400,3),dtype=np.uint8)
        tick =0
        stringPos = 0
        ticksTofig = 0
        status = True
        #print('starting tocreate pic')
        for x in range(8):
            for y in range(8):
                try:
                    if stringBoard[stringPos] == "/" and stringPos<=len(stringBoard):
                        stringPos+=1
                    
                    try:
                        if status:
                            ticksTofig = int(stringBoard[stringPos])
                        if debug:    
                            print('this is ticks to fig: ',ticksTofig)
                    except ValueError:
                            pass
                         
                except IndexError:
                    pass
                
                
                if x%2 == 0:
                    if tick %2==0:
                        if ticksTofig==0:
                            
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = AddWithMask("images/white_square.png",picStruct[stringBoard[stringPos]])
                            
                        else:
                            boardPic[50*x:50+50*x,50*y:50+50*y] = fontWhite
                            status = False
                            ticksTofig =ticksTofig-1
                
                    else:
                        if ticksTofig==0:
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = AddWithMask("images/brown_square.png",picStruct[stringBoard[stringPos]])
                            
                        else:
                            fb = fontBlack[:, :, ::-1]
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = fb
                            ticksTofig =ticksTofig-1
                            status = False
                    
                else:
                
                    if tick %2==0:
                        
                    
                        if ticksTofig==0:
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = AddWithMask("images/brown_square.png",picStruct[stringBoard[stringPos]])
                            
                        else:
                            fb = fontBlack[:, :, ::-1]
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = fb
                            ticksTofig =ticksTofig-1
                            status = False
                
                    else:
                    
                        if ticksTofig==0:
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = AddWithMask("images/white_square.png",picStruct[stringBoard[stringPos]])
                        else:
                            boardPic[50*x:50+50*x,50*y:50+50*y]  = fontWhite
                            ticksTofig =ticksTofig-1
                            status = False
                        
                tick += 1
                if debug:
                    print ('this is tick: ',tick)
               
                    if stringPos<=len(stringBoard):
                        try:
                            print('this is stringletter: ',stringBoard[stringPos])
                        
                        except IndexError:
                            pass
                if ticksTofig==0:
                    stringPos+=1
                    status = True
                
        return(boardPic)           
        cv2.imwrite('images/tmp0.png',boardPic)
       
def AddWithMask (pic1,pic2,debug=False):
    
    pic1 = Image.open(pic1)
    pic2 = Image.open(pic2).convert("RGBA")
    pic1 = pic1.resize((50,50))
    pic2 = pic2.resize((50,50))
    res = Image.composite(pic2, pic1, pic2)
    #res.show()
    resCv= np.array(res)
    resCv = resCv[:, :, ::-1].copy()
    if debug:
        cv2.imshow('result',resCv)
        cv2.waitKey(0)
    return(res)      
class FakeRobot():
    '''
    in case if need to check something with no connection to realRobot 
    It have all used functions
    '''
    def __init__(self,some,use_rt):
        print('FakeRobot Initiliased')
        
    def movej(self,pose,acc,vel):
        pass
        #print("Fake MoveJ with pose",pose, ' acc=',acc,' vel=',vel)
    def movel(self,pose,acc,vel):
        pass
        #print("Fake MoveL with pose",pose, ' acc=',acc,' vel=',vel)
    def movep(self,pose,acc,vel):
        pass
        #print("Fake MoveP with pose",pose, ' acc=',acc,' vel=',vel)
    def getl(self):
        #print('Fake getL')
        return([1,1,1,1,1,1])
    def getj(self):
        #print('Fake getJ')
        return([1,1,1,1,1,1])
    
    def set_digital_out(self,port,state):
        pass
        #print('Setting Fake Port=',port,' on state ',state)
    def get_digital_in(self,port):
        return(True)
        

if __name__ == '__main__':
    #import chess
    #board = chess.Board()
    #strBoard= Board2String(board)
    #print (strBoard)
    #print(board.fen())
    #print('this is turn',BoardTurn(board))
    #print(BoardTurn(board))
    #bard = (Board2String(board))
    #print(board)
    #fenBoard = "rnbqkbnr/1ppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR"
    #pic = DrawBoardPic(fenBoard+"  ")
    #cv2.imshow('Image',pic)
    #cv2.waitKey(0)
    
    #AddWithMask(cv2.imread("images/brown_square.png"), cv2.resize(cv2.imread('images/Chess_bdt60.png'),(50,50)))
    #AddWithMask("images/white_square.png", "images/Chess_plt60.png")
    #AddWithMask("images/brown_square.png", "images/Chess_plt60.png")
    
    #print(stringBoard2Struct(Board2String(board),False))    
    img = cv2.imread ("images/tmp0.png")
    data = Picture2List(img,6)
    for i in data:
        cv2.imshow('piece',i)
        cv2.waitKey(0)  
    