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

figuresDropWhitePos = {'R1': [0, 0], 'R2': [0, 1], 'N1': [0, 2], 'N2': [0, 3], 'B1': [0, 4], 'B2': [0, 5], 'Q': [0, 6],
                       'K': [0, 7],
                       'P1': [1, 0], 'P2': [1, 1], 'P3': [1, 2], 'P4': [1, 3], 'P5': [1, 4], 'P6': [1, 5], 'P7': [1, 6],
                       'P8': [1, 7]}

figuresDropBlackPos = {'r1': [-2, 0], 'r2': [-2, 1], 'n1': [-2, 2], 'n2': [-2, 3], 'b1': [-3, 0], 'b2': [-3, 1],
                       'q': [-3, 2], 'k': [-3, 3],
                       'p1': [0, 0], 'p2': [0, 1], 'p3': [0, 2], 'p4': [0, 3], 'p5': [-1, 0], 'p6': [-1, 1],
                       'p7': [-1, 2], 'p8': [-1, 3]}

figuresDropOneWhite = [0.1803992965863879, -0.24103107843579283, 0.010095170447183596, -1.1901454611120088,
                       1.2234782140544342, -1.1693563955965807]
figuresDropOneBlack = [-0.21597283924858426, 0.26416288347244926, 0.0098859621479227, -1.547018221144725,
                       -0.015171225231969778, 0.06229965686551571]

figuresDropTwoWhite = [0.21194604764270986, 0.17933591723351736, 0.010593156974211093, -1.5469985144064247,
                       -0.015042821734070701, 0.062454168316649836]
figuresDropTwoBlack = [-0.21551539833003064, 0.265199432728618, 0.00937194000189756, -1.5624574502433242,
                       -0.0005707219235816822, 0.029614678196443107]

figuresDropThreeWhite = [-0.21405490280611295, 0.1808141713425461, 0.010151664326446569, -1.1929833974907087,
                         -1.2459011403951272, 1.2237401982694514]
figuresDropThreeBlack = [-0.2470889183393554, -0.24900607946606718, 0.010793673646478458, -1.19316045157206,
                         -1.2458697546777115, 1.2236598502553007]

playerOneRfPt = [(81, 0), (559, 482)]
playerTwoRfPt = [(73, 0), (562, 478)]
playerThreeRfPt = [(74, 2), (562, 475)]

# playerOneCamChessboard = [0.09675389528274536, -1.3994048277484339, -1.4052794615374964, -1.9647515455829065, -1.5906232039081019, 3.0755436420440674]
playerOneCamChessboard = [0.051998429000377655, -1.4629328886615198, -1.3594406286822718, -1.8476293722735804,
                          -1.5865219275103968, 3.1161179542541504]
playerTwoCamChessboard = [1.7413198947906494, -1.4539602438556116, -1.3791049162494105, -1.8529604117022913,
                          -1.5898192564593714, 2.988967180252075]
playerThreeCamChessboard = [3.4338903427124023, -1.3611272017108362, -1.4523032347308558, -1.8463237921344202,
                            -1.5878532568561, 2.871652603149414]

# playerOneJPose =  [0.08900909125804901, -1.6477697531329554, -1.4908612410174769, -1.5547736326800745, 1.5817259550094604, 0.1801697164773941]
# playerOneLPose =  [0.45314738468687216, -0.16881999501108105, 0.023660661182472925, -1.1208433377154408, 1.2477971095137799, -1.2876061373162973]
playerOneJPose = [0.22582100331783295, -1.7258575598346155, -1.5538619200335901, -1.4542248884784144,
                  1.5804448127746582, 0.16899892687797546]
playerOneLPose = [0.487037554002419, -0.16685695558083755, 0.024884598232941382, -1.190231936493991, 1.2234888500986458,
                  -1.16938632424535]

playerTwoJPose = [1.8050403594970703, -1.6614320913897913, -1.4907053152667444, -1.5547612349139612, 1.5818578004837036,
                  0.180193692445755]
playerTwoLPose = [0.1360108931457255, 0.49127108362763816, 0.02511524607939311, -1.5478544763053146,
                  0.028105508454135814, 0.02052021929791296]

playerThreeJPose = [3.5324156284332275, -1.6254108587848108, -1.3376057783709925, -1.739281956349508,
                    1.5746710300445557, 0.44801902770996094]
playerThreeLPose = [-0.47850726183062003, 0.10288212931684357, 0.026080669286643682, -1.198481042137421,
                    -1.1828496935312154, 1.2353622068411627]

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
