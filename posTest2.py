import urx
robot = urx.Robot('192.168.0.20',use_rt=True)
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
poses = [-0.2137438495147, 0.18139090656430382, 0.005925980295499275, -1.1684165421177752, -1.2217935573773617, 1.2900015034666823]
pose = poses.copy()
robot.movel(poses,vel =0.4,acc=0.4)
deltaX = 0.034
deltaY = 0.034
for i in ((0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2)):
    pose[0]=poses[0] - deltaX*i[1]
    pose[1]=poses[1] + deltaY*i[0]
    robot.movel(pose,vel =0.4,acc=0.4)
    
    a= input('press enter to continue')



