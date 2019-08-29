import chess, sys
import urx
from PyQt5.QtWidgets import QWidget, QApplication
from pip._vendor.distlib import database

class MainGame(QWidget):
    "'it` a game class"''
    def __init__(self):
        super().__init__()

    def Move(self, board, string):
        move=chess.Move.from_uci(string)
        board.push(move)
        print(board,"\n")
    
    def findPosFigureFromSquare(self, figure, board):
        dataBoard = self.board2Struct(board)
        dataBaseBoard = self.board2Struct(chess.Board())
        for i in range(len(self.listOfNecessaryChanges)):
            if figure == dataBoard[self.listOfNecessaryChanges[i]]:
                if dataBoard[self.listOfNecessaryChanges[i]] != dataBaseBoard[self.listOfNecessaryChanges[i]]: 
                    print(self.listOfNecessaryChanges[i])
                    #from_square
                    return(self.listOfNecessaryChanges[i])
                    break
                
    def findPosFigureToSquare(self, figure, board):
        dataBoard = self.board2Struct(board)
        dataBaseBoard = self.board2Struct(chess.Board())
        for i in range(len(self.listOfNecessaryChanges)):
            if dataBoard[self.listOfNecessaryChanges[i]] == '0':
                if dataBoard[self.listOfNecessaryChanges[i]] != dataBaseBoard[self.listOfNecessaryChanges[i]]:
                    if figure == dataBaseBoard[self.listOfNecessaryChanges[i]]:
                        print(self.listOfNecessaryChanges[i])
                        #to_square
                        return(self.listOfNecessaryChanges[i])
                        break
            else:
                
                self.MoveToSpace(board, self.listOfNecessaryChanges[i])            
                dataBoard = self.board2Struct(board) 
                
                if dataBoard[self.listOfNecessaryChanges[i]] != dataBaseBoard[self.listOfNecessaryChanges[i]]:
                    
                    #self.CheckBoardFigure(board)
                    self.CheckBoardFreeSpace(board)
                    #self.AnalyzeBoard(board)
        
                    if figure == dataBaseBoard[self.listOfNecessaryChanges[i]]:
                        print(self.listOfNecessaryChanges[i])
                        #to square
                        return(self.listOfNecessaryChanges[i])
                        break
    
    def AnalyzeBoard(self, board):
        dataBoard = self.board2Struct(board)
        dataBaseBoard = self.board2Struct(chess.Board())
        for i in range(len(self.listOfNecessaryChanges)):
            if dataBoard[self.listOfNecessaryChanges[i]] == 0:
                print("Figures, number:", dataBaseBoard[self.listOfNecessaryChanges[i]] + ",",  self.listOfNecessaryChanges[i])
        
        #print(dataBoard[square])
        
    def CheckBoardFreeSpace(self, board):
        self.listFreeSpace = []
        dataBoard = self.board2Struct(board)
        
        for i in range(64):
            if dataBoard[i] == 0:
                self.listFreeSpace.append(i)
        print("List where there are empty squares", self.listFreeSpace)
        
    def CheckBoardFigure(self, board):
        self.listOfNecessaryChanges = []
        self.listOfNotNecessaryChanges = []
        
        for i in range(64):    
            if self.CheckPosFigure(board, i) == False:
                self.listOfNecessaryChanges.append(i)
            else:
                self.listOfNotNecessaryChanges.append(i)
                
        print("A list that does not require changes", self.listOfNotNecessaryChanges)
        print("A list that do require changes", self.listOfNecessaryChanges)
    
    def CheckPosFigure(self, board, square):
        baseBoard = chess.Board()
        dataBoard = self.board2Struct(board)
        dataBaseBoard = self.board2Struct(baseBoard)
        if dataBoard[square] == dataBaseBoard[square]:
            return True
        else:
            return False
        
        
    def board2Struct(self, board):
        stringBoard = self.board2String(board)
        dataBoard = self.stringBoard2Struct(stringBoard, debug=False)
        return dataBoard
    
    def board2String(self, board):
        stringBoard  = board.fen(board)
        return(stringBoard[0:stringBoard.find(" ")])
    
    def stringBoard2Struct(self, stringBoard,debug=False):
        
        ''' convert String board to a list type '''
        data = [i for i in range(64)]
        
        tick = 0
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
    
    def PosToSquareText(self, pos):
        if pos==0:
            return('a1')
        if pos==1:
            return('b1')
        if pos==2:
            return('c1')
        if pos==3:
            return('d1')
        if pos==4:
            return('e1')
        if pos==5:
            return('f1')
        if pos==6:
            return('g1')
        if pos==7:
            return('h1')
        if pos==8:
            return('a2')
        if pos==9:
            return('b2')
        if pos==10:
            return('c2')
        if pos==11:
            return('d2')
        if pos==12:
            return('e2')
        if pos==13:
            return('f2')
        if pos==14:
            return('g2')
        if pos==15:
            return('h2')
        if pos==16:
            return('a3')
        if pos==17:
            return('b3')
        if pos==18:
            return('c3')
        if pos==19:
            return('d3')
        if pos==20:
            return('e3')
        if pos==21:
            return('f3')
        if pos==22:
            return('g3')
        if pos==23:
            return('h3')
        if pos==24:
            return('a4')
        if pos==25:
            return('b4')
        if pos==26:
            return('c4')
        if pos==27:
            return('d4')
        if pos==28:
            return('e4')
        if pos==29:
            return('f4')
        if pos==30:
            return('g4')
        if pos==31:
            return('h4')
        if pos==32:
            return('a5')
        if pos==33:
            return('b5')
        if pos==34:
            return('c5')
        if pos==35:
            return('d5')
        if pos==36:
            return('e5')
        if pos==37:
            return('f5')
        if pos==38:
            return('g5')
        if pos==39:
            return('h5')
        if pos==40:
            return('a6')
        if pos==41:
            return('b6')
        if pos==42:
            return('c6')
        if pos==43:
            return('d6')
        if pos==44:
            return('e6')
        if pos==45:
            return('f6')
        if pos==46:
            return('g6')
        if pos==47:
            return('h6')
        if pos==48:
            return('a7')
        if pos==49:
            return('b7')
        if pos==50:
            return('c7')
        if pos==51:
            return('d7')
        if pos==52:
            return('e7')
        if pos==53:
            return('f7')
        if pos==54:
            return('g7')
        if pos==55:
            return('h7')
        if pos==56:
            return('a8')
        if pos==57:
            return('b8')
        if pos==58:
            return('c8')
        if pos==59:
            return('d8')
        if pos==60:
            return('e8')
        if pos==61:
            return('f8')
        if pos==62:
            return('g8')
        if pos==63:
            return('h8')
    
    def MoveToSpace(self, board, from_square):
        self.CheckBoardFigure(board)
        self.CheckBoardFreeSpace(board)
        self.AnalyzeBoard(board)
        
        to_square = self.listFreeSpace[0]
        print("from", from_square, "to empty", to_square)
        self.Move(b, self.PosToSquareText(from_square) + self.PosToSquareText(to_square))
    
    def MoveSortBack(self, board, figure):    
        
        self.CheckBoardFigure(board)
        self.CheckBoardFreeSpace(board)
        self.AnalyzeBoard(board)
        if self.listOfNecessaryChanges != []:
            from_square = self.findPosFigureFromSquare(figure, board)
            to_square = self.findPosFigureToSquare(figure, board)
            if from_square != None and to_square != None:
                print("from", from_square, "to", to_square)
                self.Move(board, self.PosToSquareText(from_square) + self.PosToSquareText(to_square))
        else:
            print('STOP')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
       
    game = MainGame()
    
    
    b=chess.Board()
    print(b)
    game.Move(b, "b1a3")
    game.Move(b, "a7a6")
    game.Move(b, "a1b1")
    game.Move(b, "b7b5")
    game.Move(b, "f1h3")
    game.Move(b, "a6a5")
    game.Move(b, "e1f1")

    
    game.MoveSortBack(b, 'N')
    game.MoveSortBack(b, 'B')
    game.MoveSortBack(b, 'p')
    game.MoveSortBack(b, 'p')

    
    #game.MoveSortBack(b, 'N')
    #game.MoveSortBack(b, 'p')
    #game.MoveSortBack(b, 'N')
    #game.MoveSortBack(b, 'p')
    #game.MoveSortBack(b, 'P')
    #game.MoveSortBack(b, 'p')
    #game.MoveSortBack(b, 'P')
    #game.MoveSortBack(b, 'n')
    #game.MoveSortBack(b, 'P')
    #game.MoveSortBack(b, 'n')
    
    sys.exit(app.exec_())

        