import cv2
import numpy as np
import dataStructers
from PIL import Image
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import time
import chess
from UtilityFucntions import *
from chessAi import *
from distutils.log import debug
import urx
from skimage.measure import compare_ssim
from locale import currency
from PyQt5.uic.Compiler import indenter
from game import MainGame


class ButtonCheck(QThread):
    """
    Just cheking buttons pushed
    """
    doneSignal = pyqtSignal(int)

    def __init__(self, robot):

        super().__init__()
        self.robot = robot

    def __del__(self):

        if self.isRunning():
            self.wait()

    def checkButtons(self):
        if self.robot.get_digital_in(dataStructers.InButtonOne) == True:
            doneSignal.emit(0)
        if self.robot.get_digital_in(dataStructers.InButtonTwo) == True:
            doneSignal.emit(1)
        if self.robot.get_digital_in(dataStructers.InButtonThree) == True:
            doneSignal.emit(2)

    def run(self):
        while True:
            time.sleep(0.5)
            self.checkButtons()


class GameLoop(QThread):
    # print('thread object')
    """
    Input: Board, Difficulty, Engine
    This is game loop thread
    """
    dataSignal = pyqtSignal(str)
    doneSignal = pyqtSignal(int)

    def __init__(self, board, difficlulty, engine, player):

        super().__init__()
        self.board = board
        self.difficlulty = difficlulty
        self.player = player

        self.engine = engine
        # print(' Game thread init done')

    def __del__(self):

        if self.isRunning():
            self.wait()

    def gameLoopThread(self, debug):

        move = self.engine.GenerateMove(self.board, self.difficlulty)
        # print('this is best move',move)
        # self.board.push(move)
        self.dataSignal.emit(move)
        time.sleep(1)
        # return(self.board)
        if debug:
            print('Game loop thread Done')

    def run(self):

        board = self.gameLoopThread(False)
        self.doneSignal.emit(self.player)


class CheckBoard(QThread):
    ''' This is the thread, that inspects player board with vision.
    depending of difrencies it will return result in string to main thread
    string: with first symbol 0, means move is done other sumbols encoding move in chessAi.py style
    first symbol 1 means no move done
    code 2 means something gone wrong '''
    result = pyqtSignal(str)

    def __init__(self, player, playerBoard, robot, camera, mode):
        super().__init__()
        self.mode = mode
        self.camera = camera
        self.playerBoard = playerBoard
        self.robot = robot
        self.player = player
        self.vel = dataStructers.vel
        self.acc = dataStructers.acc
        self.same = False
        print('Thread init', 'mode is ', mode)
        if self.player == 0:
            self.refPt = dataStructers.playerOneRfPt
            print(self.refPt)
        elif self.player == 1:
            self.refPt = dataStructers.playerTwoRfPt
        elif self.player == 2:
            self.refPt = dataStructers.playerThreeRfPt

    def MoveToZero(self, side):
        '''

        Get curren robot position and then check if robot is away from Playerboard

        '''

        if side == 1:

            if self.player == 0:
                print('move to photo Player 1')
                # self.robot.movej(dataStructers.playerOneJPose, self.acc, self.vel)
                # curPose = self.robot.getj().copy()
                # curPose[4]-=3.14159
                # self.robot.movej(curPose, self.acc, self.vel)
                # curPose[5]+=2.6
                # self.robot.movej(curPose, self.acc, self.vel)
                self.robot.movej(dataStructers.playerOneCamChessboard, self.acc, self.vel)

            if self.player == 1:
                print('move to photo Player 2')
                # self.robot.movej(dataStructers.playerTwoJPose, self.acc, self.vel)
                self.robot.movej(dataStructers.playerTwoCamChessboard, self.acc, self.vel)

            if self.player == 2:
                print('move to photo Player 3')
                # self.robot.movej(dataStructers.playerThreeJPose, self.acc, self.vel)
                self.robot.movej(dataStructers.playerThreeCamChessboard, self.acc, self.vel)

        if side == 2:

            if self.player == 0:
                print('go back Player 1')
                # curPose = self.robot.getj().copy()
                # curPose[5]-=2.6
                # self.robot.movej(curPose, 0.8, 0.8)
                # curPose[4]+=3.14159
                # self.robot.movej(curPose, 0.8, 0.8)
                self.robot.movej(dataStructers.playerOneJPose, self.acc, self.vel)

            if self.player == 1:
                print('go back Player 2')
                self.robot.movej(dataStructers.playerTwoJPose, self.acc, self.vel)
                # self.robot.movej(dataStructers.playerTwoCamChessboard, self.acc, self.vel)

            if self.player == 2:
                print('go back Player 3')
                self.robot.movej(dataStructers.playerThreeJPose, self.acc, self.vel)
                # self.robot.movej(dataStructers.playerThreeCamChessboard, self.acc, self.vel)

    def __del__(self):

        if self.isRunning():
            self.wait()

    def MakePhoto(self, param):
        '''
        If this is a game start, makes a photo of prepeared board
        '''
        self.robot.set_digital_out(dataStructers.led_flash, True)
        time.sleep(1)
        ret, image = self.camera.read()
        ret, image = self.camera.read()

        self.robot.set_digital_out(dataStructers.led_flash, False)

        image = image[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]

        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.GaussianBlur(image, (3, 3), 0)

        if param == 0:
            path = 'images/base' + str(self.player) + '.bmp'
            self.robot.set_digital_out(2 + self.player, True)
        elif param == 1:
            path = 'images/pl1' + str(self.player) + '.bmp'
        elif param == 2:
            path = 'images/pl2' + str(self.player) + '.bmp'
        cv2.imwrite(path, image)

    def CheckWithDiff(self, squaresToCheck):

        """  If some possible moves are present, it need to be checked.
        returns squares fromchecked, that are equal to square without figure
        """

        if self.player == 0:
            base = cv2.imread("images/cb1.bmp")
        if self.player == 1:
            base = cv2.imread("images/cb2.bmp")
        if self.player == 2:
            base = cv2.imread("images/cb3.bmp")

        current = self.current.copy()
        current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        current = current[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)

        base = cv2.GaussianBlur(base, (3, 3), 0)
        base = cv2.GaussianBlur(base, (3, 3), 0)
        base = cv2.GaussianBlur(base, (3, 3), 0)
        base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(base, current, full=True)
        diff = (diff * 255).astype("uint8")

        ret, thresh = cv2.threshold(diff, 180, 255, cv2.THRESH_BINARY_INV)
        #         thresh = cv2.threshold(diff, 0, 255,
        #                                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        #
        boardList = Picture2List(thresh)
        histDiffs = [i for i in range(len(squaresToCheck))]
        w, h = self.diff.shape
        w = int(w / 16)
        h = int(h / 16)
        factor = w * h

        histDiffs = [i for i in range(64)]
        for i in squaresToCheck:
            hist = cv2.calcHist([boardList[i]], [0], None, [256], [0, 256])
            if int(hist[0]) > factor * 0.5:
                histDiffs[i] = 1
            else:
                histDiffs[i] = 0

        # print('this is move in Vision',square2Uci(squares[0])+square2Uci(squares[1]))
        print('This is squares, that are equal to square without fugure', histDiffs)
        return (histDiffs)

    def CheckBoard(self):

        '''
        Return squares where was some moves
        '''
        self.robot.set_digital_out(dataStructers.led_flash, True)
        time.sleep(1)
        ret, self.current = self.camera.read()
        ret, self.current = self.camera.read()

        self.robot.set_digital_out(dataStructers.led_flash, False)
        current = self.current[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]

        turn = BoardTurnNumber(self.playerBoard)
        # print('turn in check',turn)

        if turn == 1:
            path = 'images/base' + str(self.player) + '.bmp'
        else:
            path = 'images/pl1' + str(self.player) + '.bmp'
        base = cv2.imread(path)
        # print('[part of base',base[0:5,0:5])
        current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
        base = cv2.GaussianBlur(base, (3, 3), 0)
        base = cv2.GaussianBlur(base, (3, 3), 0)

        #         cv2.imshow('current',current)
        #         cv2.imshow('base',base)
        #         cv2.waitKey(0)

        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)

        self.cur = current
        (score, diff) = compare_ssim(base, current, full=True)
        self.diff = (diff * 254).astype("uint8")

        cv2.imwrite('aa.bmp', self.diff)

        # cv2.waitKey(0)
        # ret, thresh = cv2.threshold(self.diff,150,255,cv2.THRESH_BINARY_INV)
        thresh = cv2.threshold(self.diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # cv2.imshow('diff',diff)
        # cv2.imshow('thresh',thresh)
        # cv2.waitKey(0)

        boardList = Picture2List(thresh)
        # for i in range(10):
        #    cv2.imshow('thresh',boardList[i])
        #    cv2.waitKey(0)

        # print(boardList[10])

        histWhites = [i for i in range(64)]
        w, h = current.shape
        w = int(w / 16)
        h = int(h / 16)
        factor = w * h
        param = 0.6
        while True:
            histWhites = [i for i in range(64)]
            for i in range(len(boardList)):
                hist = cv2.calcHist([boardList[i]], [0], None, [256], [0, 256])
                if int(hist[255]) > factor * param:
                    histWhites[i] = 1
                else:
                    histWhites[i] = 0
            squares = []
            for i in range(len(histWhites)):
                if histWhites[i] == 1:
                    squares.append(i)
            if len(squares) > 1 or param == 0.1:
                break
            else:
                param -= 0.1

        # print('this is move in Vision',square2Uci(squares[0])+square2Uci(squares[1]))
        # print(squares)
        return (squares)

    def CheckStartPosition(self):

        '''
        Checks if current board is same as base
        '''
        print('im here to check board')
        self.robot.set_digital_out(dataStructers.led_flash, True)

        ret, self.current = self.camera.read()
        ret, self.current = self.camera.read()

        self.robot.set_digital_out(dataStructers.led_flash, False)
        current = self.current[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]

        path = 'images/base' + str(self.player) + '.bmp'
        base = cv2.imread(path)

        current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
        base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)

        base = cv2.GaussianBlur(base, (3, 3), 0)
        base = cv2.GaussianBlur(base, (3, 3), 0)

        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)
        current = cv2.GaussianBlur(current, (3, 3), 0)

        (score, diff) = compare_ssim(base, current, full=True)
        diff = (diff * 255).astype("uint8")
        cv2.imwrite('tdif.bmp', diff)

        # cv2.waitKey(0)
        # ret, thresh = cv2.threshold(self.diff,150,255,cv2.THRESH_BINARY_INV)
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        diffHist = cv2.calcHist([thresh], [0], None, [256], [0, 256])
        cv2.imwrite('a1.bmp', thresh)
        w, h = diffHist.shape
        if diffHist[0] >= w * h * 0.7:
            self.same = True
        else:
            self.same = False

    def run(self):

        print(' RUn method')
        if self.mode == 1:
            print('go to photo')
            self.MoveToZero(1)
            self.MakePhoto(0)
            # self.MoveToZero(2)
            print('Photo done, emitting sygnal')
            self.result.emit('done')
        elif self.mode == 3:
            self.MoveToZero(1)
            self.MakePhoto(1)
            print('photo reDone')

        elif self.mode == 4:
            print('lets check')
            self.CheckStartPosition()
            print('this is same', self.same)
            print('position checked')

        elif self.mode == 2:
            self.MoveToZero(1)
            moveList = self.CheckBoard()
            print('gained list', moveList)

            if len(moveList) > 9:
                print('No move Done')
                data = '0' + str(self.player)
                self.result.emit(data)

            else:
                moves = []
                moveFrom = self.CheckWithDiff(moveList)
                print('This is white Square ', moveFrom)
                for i in range(len(moveList)):
                    for j in range(len(moveList)):

                        posibleMove = square2Uci(moveList[i]) + square2Uci(moveList[j])
                        posibleMove = chess.Move.from_uci(posibleMove)
                        if posibleMove in self.playerBoard.legal_moves:
                            self.robot.set_digital_out(dataStructers.led_red, False)
                            moves.append(posibleMove)
                            print('this is possible Move', posibleMove)
                        else:
                            self.robot.set_digital_out(dataStructers.led_red, True)

                print('This is moves ', moves)
                if len(moves) == 0:
                    self.robot.set_digital_out(dataStructers.led_red, True)
                    print('No move Done')
                    data = '0' + str(self.player)
                    self.result.emit(data)


                elif len(moves) == 1:
                    self.move = moves[0]
                    self.resultMove = moves[0]
                    data = '1' + str(self.player) + str(moves[0].from_square) + "-" + str(moves[0].to_square)
                    print('this is result move', self.move)
                    self.robot.set_digital_out(dataStructers.led_red, False)
                    self.MakePhoto(1)
                    # self.MoveToZero(2)

                    self.result.emit(data)





                elif len(moves) == 4:
                    if (moveList[1] - 1 == moveList[0]) and (moveList[2] - 2 == moveList[0]) and (
                            moveList[3] - 3 == moveList[0]):
                        print("castling")
                        for i in moves:
                            if self.playerBoard.is_castling(i):
                                data = '1' + str(self.player) + str(i.from_square) + "-" + str(i.to_square)
                                self.MoveToZero(1)
                                self.MakePhoto(1)
                                # self.MoveToZero(2)
                                self.result.emit(data)
                                self.resultMove = i
                                self.robot.set_digital_out(dataStructers.led_red, False)
                                break
                    elif (moveList[0] + 2 == moveList[1]) and (moveList[2] - 1 == moveList[1]) and (
                            moveList[3] - 2 == moveList[1]):
                        print("castling")
                        for i in moves:
                            if self.playerBoard.is_castling(i):
                                data = '1' + str(self.player) + str(i.from_square) + "-" + str(i.to_square)
                                self.MoveToZero(1)
                                self.MakePhoto(1)
                                # self.MoveToZero(2)
                                self.resultMove = i
                                self.result.emit(data)
                                self.robot.set_digital_out(dataStructers.led_red, False)
                                break
                else:
                    # result = self.CheckWithDiff(moveList)
                    # if result !='Error':
                    #    data = '1'+str(self.player)+str(result.from_square)+"-"+str(result.to_square)
                    #    self.MakePhoto(1)
                    #    self.resultMove= i
                    #    self.result.emit(data)
                    #   print('gained result from 2nd check')
                    data = "2" + str(self.player) + "Something gone Wrong try to fix it"
                    self.robot.set_digital_out(dataStructers.led_red, True)
                    self.result.emit(data)

        self.robot.set_digital_out(1, False)


class DrawThread(QThread):
    # print('thread object')
    """
    this class is constructing chess picture with figures
    depending on chess.board status

    trying
    """

    def __init__(self, board, player):
        super().__init__()
        self.board = board
        self.player = player

    def __del__(self):
        if self.isRunning():
            self.wait()

    def DrawBoardPic(self, stringBoard, debug=False):
        # print("let`s run function")
        picStruct = {'r': 'images/Chess_rdt60.png',
                     'n': 'images/Chess_ndt60.png',
                     'b': 'images/Chess_bdt60.png',
                     'q': 'images/Chess_qdt60.png',
                     'k': 'images/Chess_kdt60.png',
                     'p': 'images/Chess_pdt60.png',
                     'R': 'images/Chess_rlt60.png',
                     'N': 'images/Chess_nlt60.png',
                     'B': 'images/Chess_blt60.png',
                     'Q': 'images/Chess_qlt60.png',
                     'K': 'images/Chess_klt60.png',
                     'P': 'images/Chess_plt60.png'}

        fontWhite = cv2.imread("images/white_square.png")
        fontBlack = cv2.imread("images/brown_square.png")
        boardPic = np.zeros((400, 400, 3), dtype=np.uint8)
        tick = 0
        stringPos = 0
        ticksTofig = 0
        status = True
        # print('starting tocreate pic')
        for x in range(8):
            for y in range(8):
                try:
                    if (stringBoard[stringPos] == "/" or stringBoard[stringPos] == "~") and stringPos <= len(
                            stringBoard):
                        stringPos += 1

                    try:
                        if status:
                            ticksTofig = int(stringBoard[stringPos])
                        if debug:
                            print('this is ticks to fig: ', ticksTofig)
                    except ValueError:
                        pass

                except IndexError:
                    pass

                if x % 2 == 0:
                    if tick % 2 == 0:
                        if ticksTofig == 0:

                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = AddWithMask("images/white_square.png",
                                                                                           picStruct[
                                                                                               stringBoard[stringPos]])

                        else:
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = fontWhite
                            status = False
                            ticksTofig = ticksTofig - 1

                    else:
                        if ticksTofig == 0:
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = AddWithMask("images/brown_square.png",
                                                                                           picStruct[
                                                                                               stringBoard[stringPos]])

                        else:
                            fb = fontBlack[:, :, ::-1]
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = fb
                            ticksTofig = ticksTofig - 1
                            status = False

                else:

                    if tick % 2 == 0:

                        if ticksTofig == 0:
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = AddWithMask("images/brown_square.png",
                                                                                           picStruct[
                                                                                               stringBoard[stringPos]])

                        else:
                            fb = fontBlack[:, :, ::-1]
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = fb
                            ticksTofig = ticksTofig - 1
                            status = False

                    else:

                        if ticksTofig == 0:
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = AddWithMask("images/white_square.png",
                                                                                           picStruct[
                                                                                               stringBoard[stringPos]])
                        else:
                            boardPic[50 * x:50 + 50 * x, 50 * y:50 + 50 * y] = fontWhite
                            ticksTofig = ticksTofig - 1
                            status = False

                tick += 1
                if debug:
                    print('this is tick: ', tick)

                    if stringPos <= len(stringBoard):
                        try:
                            print('this is stringletter: ', stringBoard[stringPos])

                        except IndexError:
                            pass
                if ticksTofig == 0:
                    stringPos += 1
                    status = True

        return (boardPic)
        cv2.imwrite('images/tmp0.png', boardPic)

    def run(self):
        # print('run draw in thread')
        # print(self.stringBoard)
        stringBoard = Board2String(self.board)
        pic = DrawBoardPic(stringBoard, False)

        string = 'images/tmp' + str(self.player) + '.png'
        cv2.imwrite(string, pic)


class RoboWorker(QThread):
    ''' Thread that operates with robot to make a move'''
    doneSignal = pyqtSignal(int)
    restarSignal = pyqtSignal(int)

    def __init__(self, player, move, moveBoards, robot, Spechial, cam):
        super().__init__()
        self.player = player
        self.move = move
        self.moveBoards = moveBoards
        self.robot = robot
        self.acc = 0.6
        self.vel = 0.8
        self.Spechial = Spechial
        self.camera = cam
        self.valrs = False
        self.promotionTakeDrop = False
        self.robot.set_digital_out(2 + player, False)
        self.same = True
        if move[2] != '':
            self.Spechial = 5
        print('Player ', self.player, ' MoveTo ', self.move)
        # Spechial ==1: Castling Spechial==2 restart ALL Spechial=0 basic move

    def __del__(self):

        if self.isRunning():
            self.wait()

    def ReturnCoords(self, square):
        tick = 0
        res = [0, 0]
        for x in range(8):
            for y in range(8):
                if tick == square:
                    res[1] = x
                    res[0] = y

                tick += 1

        return (res)

    def MoveToZero(self):
        ''' Places robot to player board'''

        curPose = self.robot.getj()
        if self.player == 0:
            # if curPose[0] <=dataStructers.playerOneJleftLimit and curPose[0]>=dataStructers.playerOneJrightLimit:
            self.robot.movej(dataStructers.playerOneJPose, self.acc, self.vel)
        # else:
        # self.robot.movej(dataStructers.playerOneJPose, self.acc, self.vel)

        if self.player == 1:
            self.robot.movej(dataStructers.playerTwoJPose, self.acc, self.vel)

        if self.player == 2:
            self.robot.movej(dataStructers.playerThreeJPose, self.acc, self.vel)

    def Promotion(self):
        boardStruct = stringBoard2Struct(self.moveBoards[0].fen())
        from_square = self.ReturnCoords(self.move[0])
        figure = boardStruct[self.move[0]]

        self.MoveXY(from_square, self.player)
        self.GripFigure(figure, True)
        self.DropFigure(figure, stringBoard2Struct(self.moveBoards[0].fen()))

        figure = FindPosiblePromotion(self.moveBoards[0], self.move[2])
        if figure in ('q', 'Q'):
            key = figure

        else:
            if stringBoard2Struct(Board2String(self.moveBoards[0])).count(figure) == 0:
                key = figure + '2'
            else:
                key = figure + '1'

        current = self.robot.getl()

        position = GetLPlayerPose(self.player, figure).copy()
        if figure in ('Q', 'K', 'P', 'R', 'N', 'B'):
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]
            position[2] = current[2]
        else:
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]
            position[2] = current[2]

        self.robot.movel(position, self.acc, self.vel)
        self.promotionTakeDrop = True
        self.GripFigure(figure, True)
        self.promotionTakeDrop = False
        self.MoveXY(self.ReturnCoords(self.move[1]), self.player)

        self.GripFigure(figure[0], False)
        # position[2] = dataStructers.figuresDropOneWhite[2] + dataStructers.figureGripStruc[figure]
        # self.robot.movel (position, self.acc, self.vel)
        # self.robot.set_digital_out(dataStructers.OutGrip,False)
        # time.sleep(dataStructers.sleep)

        # position[2]+= 0.1
        # self.robot.movel (position, self.acc, self.vel)
        # time.sleep(dataStructers.sleep)
        # print("611")

    def MakeMove(self):
        ''' General move function'''

        print('this is move',self.move)

        boardStruct = stringBoard2Struct(self.moveBoards[0].fen())
        to_square = self.ReturnCoords(self.move[1])
        print('Move to square', to_square)
        figure = boardStruct[self.move[1]]
        # print('figure tha is needed to DRop ',figure)
        if figure:
            # ''' move from square to square'''

            self.MoveXY(to_square, self.player)
            self.GripFigure(figure, True)
            self.DropFigure(figure, stringBoard2Struct(self.moveBoards[0].fen()))

        from_square = self.ReturnCoords(self.move[0])
        # print('Move from square',from_square)
        boardStruct = stringBoard2Struct(self.moveBoards[0].fen())
        figure = boardStruct[self.move[0]]
        # print('moving figure is',figure)
        self.MoveXY(from_square, self.player)
        self.GripFigure(figure, True)
        self.MoveXY(to_square, self.player)
        self.GripFigure(figure, False)

    def DropFigure(self, figure, listBoard):

        '''
        Fuction that place beated figures in drops near board

        '''
        # print(figure)
        if figure in ['B', 'R', 'N', 'K', 'Q']:
            count = listBoard.count(figure)
            if count == 2:
                key = figure + "1"
            elif count == 1 and figure != 'Q':
                key = figure + '2'
            elif count == 1 and figure == 'Q':
                key = figure
            position = GetLPlayerPose(self.player, figure).copy()
            # z = dataStructers.figuresDropOneWhite.copy()
            # position[2]+= z[2] - dataStructers.figureGripStruc[figure]
            position[2] += 0.1
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]

            # print('position',position)
            self.robot.movel(position, self.acc, self.vel)
            # self.GripFigure(figure,False)

            position[2] = dataStructers.figuresDropOneWhite[2] + dataStructers.figureGripStruc[figure]
            self.robot.movel(position, self.acc, self.vel)
            self.robot.set_digital_out(dataStructers.OutGrip, False)
            time.sleep(dataStructers.sleep)

            position[2] += 0.1
            self.robot.movel(position, self.acc, self.vel)
            time.sleep(dataStructers.sleep)

        elif figure == 'P':
            tmp = ('8', '7', '6', '5', '4', '3', '2', '1')
            # print   ('this is count of Pawns on board',listBoard.count(figure))
            key = figure + tmp[listBoard.count(figure) - 1]
            # print('Drop key',key)
            position = GetLPlayerPose(self.player, figure).copy()
            # print('position',position)
            # print('coeficient',dataStructers.figuresDropWhitePos[key][0],'  ', dataStructers.figuresDropWhitePos[key][1])
            # z = dataStructers.figuresDropOneWhite.copy()
            # position[2]+= z[2] - dataStructers.figureGripStruc[figure]
            position[2] += 0.1
            # print('this is structure',dataStructers.figuresDropBlackPos)
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][1]

            # print('position',position)
            self.robot.movel(position, self.acc, self.vel)
            # self.GripFigure(figure,False)

            position[2] = dataStructers.figuresDropOneWhite[2] + dataStructers.figureGripStruc[figure]
            self.robot.movel(position, self.acc, self.vel)
            self.robot.set_digital_out(dataStructers.OutGrip, False)
            time.sleep(dataStructers.sleep)

            position[2] += 0.1
            self.robot.movel(position, self.acc, self.vel)
            time.sleep(dataStructers.sleep)


        elif figure in ['b', 'r', 'n', 'k', 'q']:
            count = listBoard.count(figure)
            if count == 2:
                key = figure + "1"
            elif count == 1 and figure != 'q':
                key = figure + '2'
            elif count == 1 and figure == 'q':
                key = figure
            position = GetLPlayerPose(self.player, figure).copy()
            # z = dataStructers.figuresDropOneBlack.copy()
            # position[2]+= z[2] - dataStructers.figureGripStruc[figure]
            position[2] += 0.1
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]

            # print('position',position)
            self.robot.movel(position, self.acc, self.vel)
            # self.GripFigure(figure,False)
            position[2] = dataStructers.figuresDropOneBlack[2] + dataStructers.figureGripStruc[figure]
            self.robot.movel(position, self.acc, self.vel)
            self.robot.set_digital_out(dataStructers.OutGrip, False)
            time.sleep(dataStructers.sleep)

            position[2] += 0.1
            self.robot.movel(position, self.acc, self.vel)
            time.sleep(dataStructers.sleep)


        elif figure == 'p':
            tmp = ('8', '7', '6', '5', '4', '3', '2', '1')
            key = figure + tmp[listBoard.count(figure) - 1]
            # print('Deop key',key)
            position = GetLPlayerPose(self.player, figure).copy()
            # print('position',position)
            # print('coeficient',dataStructers.figuresDropBlackPos[key][0],'  ', dataStructers.figuresDropBlackPos[key][1])
            # position[2] = position[2]+ dataStructers.figuresDropOneBlack[2]

            # z = dataStructers.figuresDropOneBlack.copy()
            # position[2]+= z[2] - dataStructers.figureGripStruc[figure]
            position[2] += 0.1
            if self.player == 0:

                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]

            elif self.player == 1:
                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]
            elif self.player == 2:
                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]

            # position[2]+= 0.1
            # position[0]+= dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][0]
            # position[1]+= dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][1]
            # print('position',position)
            self.robot.movel(position, self.acc, self.vel)
            # self.GripFigure(figure,False)
            position[2] = dataStructers.figuresDropOneBlack[2] + dataStructers.figureGripStruc[figure]
            self.robot.movel(position, self.acc, self.vel)
            self.robot.set_digital_out(dataStructers.OutGrip, False)
            time.sleep(dataStructers.sleep)

            position[2] += 0.1
            self.robot.movel(position, self.acc, self.vel)
            time.sleep(dataStructers.sleep)

    def MoveXY(self, square, player):

        '''
         moves robot to targeted square
        '''
       # print('player', player)

        pose = []
        if self.player == 0:
            pose = dataStructers.playerOneLPose
        elif self.player == 1:
            pose = dataStructers.playerTwoLPose
        elif self.player == 2:
            pose = dataStructers.playerThreeLPose
        poseToMove = pose.copy()
        if self.player == 0:
            poseToMove[0] = pose[0] - dataStructers.chessboard_squareX * square[1]
            poseToMove[1] = pose[1] + dataStructers.chessboard_squareY * square[0]
            # poseToMove[0] = pose[0] - dataStructers.chessboard_squareX*square[0]
            # poseToMove[1] = pose[1] - dataStructers.chessboard_squareY*square[1]

        elif self.player == 1:
            poseToMove[0] = pose[0] - dataStructers.chessboard_squareX * square[0]
            poseToMove[1] = pose[1] - dataStructers.chessboard_squareY * square[1]

        elif self.player == 2:
            poseToMove[0] = pose[0] + dataStructers.chessboard_squareX * square[1]
            poseToMove[1] = pose[1] - dataStructers.chessboard_squareY * square[0]

        poseToMove[2] = pose[2] + 0.09
        self.robot.movel(poseToMove, self.acc, self.vel)

    def GripFigure(self, figure, grip):

        ''' This function grips and drops figures
        if grip == True than pick figure
        else drops it '''
        if self.Spechial != 2 and self.Spechial != 6:
            if self.player == 0:
                z = dataStructers.playerOneLPose
            elif self.player == 1:
                z = dataStructers.playerTwoLPose
            elif self.player == 2:
                z = dataStructers.playerThreeLPose

            pose = self.robot.getl()
            defPose = pose.copy()
            if self.promotionTakeDrop == True:
                if figure in ['q', 'k', 'r', 'b', 'n', 'p']:
                    z = dataStructers.figuresDropOneBlack
                elif figure in ['Q', 'K', 'R', 'B', 'N', 'P']:
                    z = dataStructers.figuresDropOneWhite
            else:
                pass

            pose[2] = z[2] + dataStructers.figureGripStruc[figure]
            # - 0.06
            self.robot.movel(pose, self.acc, self.vel)
            # grip
            if grip:
               # print('762 z=', pose[2])
                self.robot.set_digital_out(dataStructers.OutGrip, True)
                time.sleep(dataStructers.sleep)
            else:
               # print('766 z=', pose[2])
                self.robot.set_digital_out(dataStructers.OutGrip, False)
                time.sleep(dataStructers.sleep)
            # pose[2] +=dataStructers.figureGripStruc[figure]
            self.robot.movel(defPose, self.acc, self.vel)

        elif self.Spechial == 2 or self.Spechial == 6:
            if grip:
                if self.valrs == True:
                    z = dataStructers.playerOneLPose.copy()
                else:
                    if figure in ['Q', 'K', 'R', 'B', 'N', 'P']:
                        z = dataStructers.figuresDropOneWhite.copy()
                    elif figure in ['q', 'k', 'r', 'b', 'n', 'p']:
                        z = dataStructers.figuresDropOneBlack.copy()
                pose = self.robot.getl()
                defPose = pose.copy()
                pose[2] = z[2] + dataStructers.figureGripStruc[figure]

                self.robot.movel(pose, self.acc, self.vel)
                self.robot.set_digital_out(dataStructers.OutGrip, True)
                #print('787 z=', pose[2])
                time.sleep(dataStructers.sleep)


            else:
                z = dataStructers.playerOneLPose.copy()
                pose = self.robot.getl()
                defPose = pose.copy()
                pose[2] = z[2] + dataStructers.figureGripStruc[figure]

                self.robot.movel(pose, self.acc, self.vel)
                self.robot.set_digital_out(dataStructers.OutGrip, False)
                #print('799 z=', pose[2])
                time.sleep(dataStructers.sleep)
        elif self.Spechial == 5:
            if figure in ['Q', 'K', 'R', 'B', 'N', 'P']:
                z = dataStructers.figuresDropOneWhite.copy()
            elif figure in ['q', 'k', 'r', 'b', 'n', 'p']:
                z = dataStructers.figuresDropOneBlack.copy()

        # pose[2] +=dataStructers.figureGripStruc[figure]
        self.robot.movel(defPose, self.acc, self.vel)

    def CastlingMove(self):
        '''
        This function makes a castling move

        '''
        from_square = self.ReturnCoords(self.move[0])
        to_square = self.ReturnCoords(self.move[1])
        boardStruct = stringBoard2Struct(self.moveBoards[0].fen())
        figure = boardStruct[self.move[0]]
        self.MoveXY(from_square, self.player)
        self.GripFigure(figure, True)
        self.MoveXY(to_square, self.player)
        self.GripFigure(figure, False)

        if self.move[1] - self.move[0] > 0:
            for i in range(1, 2):
                figure = boardStruct[self.move[1] + i]
                if figure == 'R' or figure == 'r':
                    from_square = self.ReturnCoords(self.move[1] + i)
                    to_square = self.ReturnCoords(self.move[1] - 1)
                    break
            self.MoveXY(from_square, self.player)
            self.GripFigure(figure, True)
            self.MoveXY(to_square, self.player)
            self.GripFigure(figure, False)
        else:
            for i in (-1, -2):
                figure = boardStruct[self.move[1] + i]
                if figure == 'R' or figure == 'r':
                    from_square = self.ReturnCoords(self.move[1] + i)
                    to_square = self.ReturnCoords(self.move[1] + 1)
                    break
            self.MoveXY(from_square, self.player)
            self.GripFigure(figure, True)
            self.MoveXY(to_square, self.player)
            self.GripFigure(figure, False)
        # self.doneSignal.emit()

    def RestartSmart(self):

        defaultBoard = chess.Board()
        _defBoardList = stringBoard2Struct(Board2String(defaultBoard), False)
        # print('Default boardlist',_defBoardList)
        endGameBoard = self.moveBoards[0]
        _endgameBoardList = stringBoard2Struct(Board2String(endGameBoard), False)
        # print('EndGame Board',_endgameBoardList)
        _currentBoardList = _endgameBoardList.copy()
        while True:
            counter = 0
            for i in range(64):

                if _currentBoardList[i] == 0 and _defBoardList[i] != 0:

                    figureOnBoard = [_defBoardList[i], _currentBoardList.count(_defBoardList[i])]
                    # print(figureOnBoard)

                    if figureOnBoard[1] == 0:
                        # print('Solutution 1')
                        # if no such figures on board
                        self.valrs = False
                        if figureOnBoard[0] == 'p' or figureOnBoard[0] == 'P':
                            key = figureOnBoard[0] + '8'

                        elif figureOnBoard[0] in ('r', 'R', 'n', 'N', 'b', 'B'):
                            key = figureOnBoard[0] + '2'
                        elif figureOnBoard[0] in ('q', 'Q', 'K', 'k'):
                            key = figureOnBoard[0]
                        current = self.robot.getl()

                        position = GetLPlayerPose(self.player, figureOnBoard[0]).copy()
                        if figureOnBoard[0] in ('Q', 'K', 'P', 'R', 'N', 'B'):
                            if self.player == 0:
                                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][
                                    0]
                                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][
                                    1]

                            elif self.player == 1:
                                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][
                                    0]
                                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][
                                    1]
                            elif self.player == 2:
                                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropWhitePos[key][
                                    0]
                                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropWhitePos[key][
                                    1]
                            position[2] = current[2]
                        else:
                            if self.player == 0:

                                position[1] -= dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][
                                    0]
                                position[0] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][
                                    1]

                            elif self.player == 1:
                                position[0] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][
                                    0]
                                position[1] += dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][
                                    1]
                            elif self.player == 2:
                                position[1] += dataStructers.dropboard_squareX * dataStructers.figuresDropBlackPos[key][
                                    0]
                                position[0] -= dataStructers.dropboard_squareY * dataStructers.figuresDropBlackPos[key][
                                    1]
                            position[2] = current[2]

                        # print("884 valrs")
                        self.robot.movel(position, self.acc, self.vel)
                        self.GripFigure(figureOnBoard[0], True)
                        self.MoveXY(self.ReturnCoords(i), self.player)

                        self.GripFigure(figureOnBoard[0], False)

                        # print(' Place figure from drop')
                        _currentBoardList[i] = figureOnBoard[0]
                        counter += 1


                    else:
                        # if there are such figures on board
                        # print('solution 2')
                        tmp = 0
                        index = -1
                        for j in range(figureOnBoard[1]):
                            index = _currentBoardList.index(figureOnBoard[0], index + 1)
                            # print('JIter is',j,' | Iteration',i,' | figure is',figureOnBoard[0],'| index ',index)

                            if _defBoardList[index] == figureOnBoard[0]:
                                tmp += 1
                                # print('One of figures on board placed right')

                            elif _defBoardList[index] != figureOnBoard[0]:

                                # print('Figure ',index,'Placed wrong Move it to right spot')
                                self.valrs = True
                                # print("912 valrs")
                                self.MoveXY(self.ReturnCoords(index), self.player)
                                self.GripFigure(figureOnBoard[0], True)
                                self.MoveXY(self.ReturnCoords(i), self.player)
                                self.GripFigure(figureOnBoard[0], False)

                                _currentBoardList[index] = 0
                                _currentBoardList[i] = figureOnBoard[0]
                                self.valrs = False

                                break

                            if tmp == figureOnBoard[1]:
                                # print('All figures on board ar in right place< but we need some more from drop')
                                if figureOnBoard[0] in ('r', 'n', 'b', 'R', 'N', 'B'):
                                    pk = '1'
                                elif figureOnBoard[0] in ('p', 'P'):
                                    pk = str(8 - tmp)
                                elif figureOnBoard[0] in ('k', 'K', 'q', 'Q'):
                                    pk = ''
                                # print(figureOnBoard[0]+pk)
                                key = figureOnBoard[0] + pk

                                current = self.robot.getl()
                                position = GetLPlayerPose(self.player, figureOnBoard[0]).copy()
                                if figureOnBoard[0] in ('Q', 'K', 'P', 'R', 'N', 'B'):
                                    if self.player == 0:
                                        position[1] -= dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropWhitePos[key][0]
                                        position[0] += dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropWhitePos[key][1]

                                    elif self.player == 1:
                                        position[0] += dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropWhitePos[key][0]
                                        position[1] += dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropWhitePos[key][1]
                                    elif self.player == 2:
                                        position[1] += dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropWhitePos[key][0]
                                        position[0] -= dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropWhitePos[key][1]
                                    position[2] = current[2]
                                else:
                                    if self.player == 0:

                                        position[1] -= dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropBlackPos[key][0]
                                        position[0] += dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropBlackPos[key][1]

                                    elif self.player == 1:
                                        position[0] += dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropBlackPos[key][0]
                                        position[1] += dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropBlackPos[key][1]
                                    elif self.player == 2:
                                        position[1] += dataStructers.dropboard_squareX * \
                                                       dataStructers.figuresDropBlackPos[key][0]
                                        position[0] -= dataStructers.dropboard_squareY * \
                                                       dataStructers.figuresDropBlackPos[key][1]
                                    position[2] = current[2]
                                self.robot.movel(position, self.acc, self.vel)
                                self.GripFigure(figureOnBoard[0], True)
                                self.MoveXY(self.ReturnCoords(i), self.player)
                                self.GripFigure(figureOnBoard[0], False)

                                _currentBoardList[i] = figureOnBoard[0]
                                counter += 1






                elif _currentBoardList[i] != _defBoardList[i] and _defBoardList[i] != 0:
                    # if wrong figure placed than place it to closest empty square
                    # print('On this place must be other figure')
                    if _currentBoardList[i] in ('R', 'N', 'B', 'Q', 'P', 'K'):
                        # if white figures
                        # print("replace wrong figure")
                        toPlaceSquare = _currentBoardList.index(0, 16)

                        self.valrs = True
                        self.MoveXY(self.ReturnCoords(i), self.player)
                        self.GripFigure(_currentBoardList[i], True)
                        self.MoveXY(self.ReturnCoords(toPlaceSquare), self.player)
                        self.GripFigure(_currentBoardList[i], False)
                        self.valrs = False

                        _currentBoardList[toPlaceSquare] = _currentBoardList[i]
                        _currentBoardList[i] = 0

                    else:
                        # if black figures
                        c = _currentBoardList.copy()
                        c.reverse()
                        toPlaceSquare = c.index(0, 16)
                        toPlaceSquare = 63 - toPlaceSquare

                        self.valrs = True
                        self.MoveXY(self.ReturnCoords(i), self.player)
                        self.GripFigure(_currentBoardList[i], True)
                        self.MoveXY(self.ReturnCoords(toPlaceSquare), self.player)
                        self.GripFigure(_currentBoardList[i], False)
                        self.valrs = False

                        _currentBoardList[toPlaceSquare] = _currentBoardList[i]
                        _currentBoardList[i] = 0

                elif _currentBoardList[i] == _defBoardList[i]:
                    # if figure is on a right place< then all K
                    counter += 1
                    # print(counter)
                # print(_currentBoardList)
            if counter == 64:
                # print(_endgameBoardList)
                # print(_currentBoardList)

                if self.Spechial == 6:
                    makePhoto = CheckBoard(self.player, self.moveBoards[1], self.robot, self.camera, 3)
                    makePhoto.MoveToZero(1)
                    makePhoto.MakePhoto(0)
                    #print("neponyatno")
                    # makePhoto.MoveToZero(2)
                self.restarSignal.emit(self.player)
                break

    def Restart(self):
        ''' this function restart the game, placing all figures back on board'''
        defaultBoard = chess.Board()
        defBoardlist = stringBoard2Struct(Board2String(defaultBoard), False)
        # print(defBoardlist)
        listOfPlaced = []
        for i in range(16):

            figure = defBoardlist[i]
            # print('White figures',figure)
            count = listOfPlaced.count(figure)
            if figure != 'Q' and figure != 'K':
                key = figure + str(count + 1)
                position = dataStructers.figuresDropOneWhite.copy()
                position[0] += dataStructers.chessboard_square * dataStructers.figuresDropWhitePos[key][0]
                position[1] += dataStructers.chessboard_square * dataStructers.figuresDropWhitePos[key][1]
                self.robot.movel(position, self.acc, self.vel)
                self.GripFigure(figure, True)
                listOfPlaced.append(figure)
                square = self.ReturnCoords(i)
                self.MoveXY(square, self.player)
                self.GripFigure(figure, False)
            #                 while self.robot.is_running():
            #                     time.sleep(dataStructers.sleep)
            if figure == 'Q' or figure == 'K':
                key = figure
                position = dataStructers.figuresDropOneWhite.copy()
                position[0] += dataStructers.chessboard_square * dataStructers.figuresDropWhitePos[key][0]
                position[1] += dataStructers.chessboard_square * dataStructers.figuresDropWhitePos[key][1]
                self.robot.movel(position, self.acc, self.vel)
                self.GripFigure(figure, True)
                listOfPlaced.append(figure)
                #                 while self.robot.is_running():
                #                     time.sleep(dataStructers.sleep)
                square = self.ReturnCoords(i)
                self.MoveXY(square, self.player)
                self.GripFigure(figure, False)

        for i in range(48, 63, 1):

            figure = defBoardlist[i]
            #print('Black figure', figure)
            count = listOfPlaced.count(figure)
            if figure != 'q' and figure != 'k':
                key = figure + str(count + 1)
                position = dataStructers.figuresDropOneWhite.copy()
                position[0] += dataStructers.chessboard_square * dataStructers.figuresDropBlackPos[key][0]
                position[1] += dataStructers.chessboard_square * dataStructers.figuresDropBlackPos[key][1]
                self.robot.movel(position, self.acc, self.vel)
                self.GripFigure(figure, True)
                listOfPlaced.append(figure)
                #                 while self.robot.is_running():
                #                     time.sleep(dataStructers.sleep)
                square = self.ReturnCoords(i)
                self.MoveXY(square, self.player)
                self.GripFigure(figure, False)
            if figure == 'q' or figure == 'k':
                key = figure
                position = dataStructers.figuresDropOneWhite.copy()
                position[0] += dataStructers.chessboard_square * dataStructers.figuresDropBlackPos[key][0]
                position[1] += dataStructers.chessboard_square * dataStructers.figuresDropBlackPos[key][1]
                self.robot.movel(position, self.acc, self.vel)
                self.GripFigure(figure, True)
                listOfPlaced.append(figure)
                #                 while self.robot.is_running():
                #                     time.sleep(dataStructers.sleep)
                square = self.ReturnCoords(i)
                self.MoveXY(square, self.player)
                self.GripFigure(figure, False)

    def run(self):

        print('MoveThread', self.move)

        #self.MoveToZero()
        if self.Spechial == 0:
            self.MoveToZero()
            self.MakeMove()
            if BoardTurn(self.moveBoards[1]) == 'w':
                makePhoto = CheckBoard(self.player, self.moveBoards[1], self.robot, self.camera, 3)

                print('MakeMove() w, special == 0')
                makePhoto.MoveToZero(1)
                makePhoto.MakePhoto(1)
                makePhoto.MakePhoto(2)
                # makePhoto.MoveToZero(2)
                # print('22')
            self.robot.set_digital_out(2 + self.player, True)
        elif self.Spechial == 1:
            self.CastlingMove()
            self.MoveToZero()
            if BoardTurn(self.moveBoards[1]) == 'w':
                makePhoto = CheckBoard(self.player, self.moveBoards[1], self.robot, self.camera, 3)

                print('CastlingMove() w, special == 1')
                makePhoto.MoveToZero(1)
                makePhoto.MakePhoto(1)
                makePhoto.MakePhoto(2)
                # makePhoto.MoveToZero(2)
            self.MoveToZero()
            self.robot.set_digital_out(2 + self.player, True)
        elif self.Spechial == 2 or self.Spechial == 6:
            # print('restart started')
            # checkBoard = CheckBoard(self.player,self.moveBoards[1],self.robot,self.camera,4)
            # checkBoard.CheckStartPosition()
            # if checkBoard.same == False:
            self.RestartSmart()
            self.MoveToZero()
        elif self.Spechial == 3:
            self.MakeMove()
            #self.MoveToZero()
        elif self.Spechial == 4:
            self.CastlingMove()
            self.MoveToZero()
            if BoardTurn(self.moveBoards[1]) == 'w':
                makePhoto = CheckBoard(self.player, self.moveBoards[1], self.robot, self.camera, 3)

                print('CastlingMove() w, special == 4')
                makePhoto.MoveToZero(1)
                
        elif self.Spechial == 5:
            self.Promotion()
            self.MoveToZero()
            if BoardTurn(self.moveBoards[1]) == 'w':
                makePhoto = CheckBoard(self.player, self.moveBoards[1], self.robot, self.camera, 3)

                print('Promotion() w, special == 5')
                makePhoto.MoveToZero(1)
                makePhoto.MakePhoto(1)
                makePhoto.MakePhoto(2)

        self.doneSignal.emit(self.player)


class TimeDelay(QThread):
    def __init__(self, t):
        super().__init__()
        self.time = t

    def __del__(self):
        if self.isRunning():
            self.wait()

    def run(self):
        time.sleep(self.time)


if __name__ == '__main__':
    # testBoard = chess.Board()
    # engine = ChessEngine(False)

    # game = GameLoop(testBoard,100,engine)
    # game.gameLoopThread(True)

    #     robot = urx.Robot("192.168.1.20", use_rt=True)

    pose = [1.8060463666915894, -1.7235668341266077, -0.8052786032306116, -2.277634922658102, -1.5196850935565394,
            3.566532850265503]

    board = chess.Board()

    robot = []
    '''
#     rm= RoboWorker(0,[5,12],[board,board],robot,2)
#     rm.run()
    camera =cv2.VideoCapture(0)
    vision = CheckBoard(1,board,robot,camera,2)

    print(board)
    a = input('Reset board')

    '''
    cam = cv2.VideoCapture(0)
    vision = CheckBoard(0, board, robot, cam, 0)
    vision.MakePhoto(0)
    '''
    robot.movej(pose,acc=0.4,vel=0.4)
    while board.is_game_over()==False:

        a = input('make a move')

        vision.run()
        try:
            move = vision.resultMove

            board.push(move)
            print(board)
            vision = CheckBoard(1,board,robot,camera,2)
        except AttributeError:
            print('Error with move')
        robot.movej(pose,acc=0.4,vel=0.4)
    '''
    # vision.CheckBoard()
    # vision.MakePhoto(1)
    # robot=FakeRobot("192.168.1.20", use_rt=True)
    # board = chess.Board('2r2rk1/pp1b1ppp/5n2/n1b5/4P3/P1N2N2/1PB2PPP/R1B2RK1 b - - 0 16')
    # t = RoboWorker(0,[],[board,board],robot,1)
    # t.RestartSmart()


