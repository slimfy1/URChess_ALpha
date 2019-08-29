#*11
playerOneJPose=[0.06250110268592834, -1.3788560072528284, -1.455707852040426, -1.813021485005514, 1.537528157234192, -14.963200044616151]
#*12
playerOneLPose = [0.5168048997404283, -0.19765654043880324, 0.15717285895768296, -1.5161983055312727,
                  -0.6114065139181427, 0.605553368599755]
#*13
playerOneCamChessboard = [0.061709772795438766, -1.4918177763568323, -1.3571980635272425, -1.826545540486471,
                          4.6884613037109375, -15.02872009275763]
#*14
figuresDropOneWhite=[0.1861768565361682, -0.32863803630359206, 0.1384878586137026, -1.5693289503287187, -0.08543661378669606, 0.13886674008435468]
#*15
figuresDropOneBlack=[0.3403337034900543, 0.18878766983783568, 0.13904898291709147, -1.165164103710859, -1.2994962624154998, 1.3212073449254302]
#*16
playerOneRfPt = [(81, 0), (559, 482)]
#*21
playerTwoJPose = [1.7280391454696655, -1.7693150679217737, -1.3033002058612269, -1.5822327772723597, 1.6234678030014038,
                  12.780832075068744]
# *22
playerTwoLPose = [0.13578511989768058, 0.4972266962853855, 0.06800807424053061, -1.6145611338886563,
                  -0.012389117405658113, 0.01022507253364818]
#*23
playerTwoCamChessboard = [0.061757709830999374, -1.4918420950519007, -1.3572104612933558, -1.826533619557516,
                          4.6884613037109375, -15.028684091552186]
#*24
figuresDropTwoWhite = [1, 3, 1, 8, 1, 1]
#*25
figuresDropTwoBlack = [5, 3, 1, 2, 8, 1]
#*26
playerTwoRfPt = [(73, 0), (562, 478)]
#*31
playerThreeJPose = [1, 3, 1, 1, 1, 5]
#*32
playerThreeLPose = [1, 3, 1, 1, 1, 1]
#*33
playerThreeCamChessboard = [0.06173374131321907, -1.4918058554278772, -1.357234303151266, -1.826545540486471,
                            4.688449382781982, -15.02872009275763]
#*34
figuresDropThreeWhite = [1, 3, 1, 8, 8, 1]
#*35
figuresDropThreeBlack = [1111111, 3, 1, 2, 8, 1]
#*36
playerThreeRfPt = [(74, 2), (562, 475)]

#*SSS
camId = 0

import cv2

picStruct = {'r': cv2.imread('images/Chess_tile_rd.png'),
             'n': cv2.imread('images/Chess_tile_nd.png'),
             'b': cv2.imread('images/Chess_tile_bd.png'),
             'q': cv2.imread('images/Chess_tile_qd.png'),
             'k': cv2.imread('images/Chess_tile_kd.png'),
             'p': cv2.imread('images/Chess_tile_pd.png'),
             'R': cv2.imread('images/Chess_tile_rl.png'),
             'N': cv2.imread('images/Chess_tile_nl.png'),
             'B': cv2.imread('images/Chess_tile_bl.png'),
             'Q': cv2.imread('images/Chess_tile_ql.png'),
             'K': cv2.imread('images/Chess_tile_kl.png'),
             'P': cv2.imread('images/Chess_tile_pl.png')}

figureGripStruc = {'r': 0.000, 'n': 0.000, 'b': 0.0, 'k': 0.00, 'q': 0.00, 'p': 0.000,
                   'R': 0.000, 'N': 0.000, 'B': 0.0, 'K': 0.00, 'Q': 0.00, 'P': 0.000}

figuresDropWhitePos = {'R1': [-1, 0], 'R2': [-1, 1], 'N1': [-1, 2], 'N2': [-1, 3], 'B1': [-1, 4], 'B2': [-1, 5], 'Q': [-1, 6],
                       'K': [-1, 7],
                       'P1': [0, 0], 'P2': [0, 1], 'P3': [0, 2], 'P4': [0, 3], 'P5': [0, 4], 'P6': [0, 5], 'P7': [0, 6],
                       'P8': [0, 7]}

figuresDropBlackPos = {'r1': [-2, 0], 'r2': [-2, 1], 'n1': [-2, 2], 'n2': [-2, 3], 'b1': [-3, 0], 'b2': [-3, 1],
                       'q': [-3, 2], 'k': [-3, 3],
                       'p1': [0, 0], 'p2': [0, 1], 'p3': [0, 2], 'p4': [0, 3], 'p5': [-1, 0], 'p6': [-1, 1],
                       'p7': [-1, 2], 'p8': [-1, 3]}

chessboard_squareX = 0.04
chessboard_squareY = 0.04

dropboard_squareX = 0.038
dropboard_squareY = 0.038

# robot speed
vel = 0.8
acc = 0.8
# robot sleep after move
sleep = 0.2

# inputs
InButtonOne = 2
InButtonTwo = 3
InButtonThree = 4

# outputs
OutGrip = 0
led_flash = 1
OutButtonOne = 2
OutButtonTwo = 3
OutButtonThree = 4
led_blue = 5
led_red = 6
# last free slot output 7


playerOneJleftLimit = 2.721442937850952
playerOneJrightLimit = 1.3371856212615967

playerTwoJleftLimit = 2.721442937850952
playerTwoJrightLimit = 1.3371856212615967

playerThreeJleftLimit = 2.721442937850952
playerThreeJrightLimit = 1.3371856212615967

boardStructure = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                  'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                  'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                  'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                  'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                  'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                  'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                  'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

picStruct = {'r': cv2.resize(cv2.imread('images/Chess_tile_rd.png'), (50, 50)),
             'n': cv2.resize(cv2.imread('images/Chess_tile_nd.png'), (50, 50)),
             'b': cv2.resize(cv2.imread('images/Chess_tile_bd.png'), (50, 50)),
             'q': cv2.resize(cv2.imread('images/Chess_tile_qd.png'), (50, 50)),
             'k': cv2.resize(cv2.imread('images/Chess_tile_kd.png'), (50, 50)),
             'p': cv2.resize(cv2.imread('images/Chess_tile_pd.png'), (50, 50)),
             'R': cv2.resize(cv2.imread('images/Chess_tile_rl.png'), (50, 50)),
             'N': cv2.resize(cv2.imread('images/Chess_tile_nl.png'), (50, 50)),
             'B': cv2.resize(cv2.imread('images/Chess_tile_bl.png'), (50, 50)),
             'Q': cv2.resize(cv2.imread('images/Chess_tile_ql.png'), (50, 50)),
             'K': cv2.resize(cv2.imread('images/Chess_tile_kl.png'), (50, 50)),
             'P': cv2.resize(cv2.imread('images/Chess_tile_pl.png'), (50, 50))}
