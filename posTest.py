import urx
robot = urx.Robot('192.168.0.20',use_rt=True)
bp = [0.06247713789343834, -1.3788560072528284, -1.4557679335223597, -1.8129733244525355,
                  1.5375521183013916, -14.963260126098085]
def ReturnCoords(square):
        tick = 0
        res=[0,0]
        for x in range(8):
            for y in range(8):
                if tick ==square:
                    res[1]=x
                    res[0]=y

                
                tick+=1    
        
        return(res)
 
res = ReturnCoords(63)
pose = [0.5168048997404283, -0.19765654043880324, 0.15717285895768296, -1.5161983055312727,
                  -0.6114065139181427, 0.605553368599755]
robot.movej(bp,vel =0.4,acc=0.4)
a= input('press enter to continue')
for i in range(56,64):
    res = ReturnCoords(i)
    p = pose.copy()
    deltaX = 0.04
    deltaY = 0.04

    p[0]=p[0] - deltaX*res[1]
    p[1]=p[1] + deltaY*res[0]
    robot.movej(bp, vel=0.4, acc=0.4)
    robot.movel(p,vel =0.4,acc=0.4)
