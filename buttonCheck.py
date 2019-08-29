import urx
import time
import os
robot = urx.Robot('192.168.0.20', use_rt=True)

state1 =False
state2= False
state3= False
file = open('status.txt','w')
file.write('000')
file.close()
def check_button():
    check1 = robot.get_digital_in(2)
    check2 = robot.get_digital_in(3)
    check3 = robot.get_digital_in(4)
    if check1 ==True:
        print('Button1  at ',time.ctime(time.time()))
        file = open('status.txt','r')
        data = file.read()
        if len(data)==3:
            some = '1'+data[1]+data[2] 
        else:
            some= '100'
        #print('data',data)
        #print('some is ',some)
        file.close()
        file = open('status.txt','w')
        file.write(some)
        file.close()
    
    if check2 == True:
        print('Button2 at ',time.ctime(time.time()) )
        file = open('status.txt','r')
        data = file.read()
        if len(data)==3:
            some=data[0]+'1'+data[2]
        else:
            some='010'
        #print(some)
        file.close()
        file = open('status.txt','w')
        file.write(some)
        file.close()
    
    if check3 == True:
        print('Button3 at ',time.ctime(time.time()))
        file = open('status.txt','r')
        data = file.read()
        if len(data)==3:
            some=data[0]+data[1]+'1'
        else:
            some='001'
        #print(some)
        file.close()
        file = open('status.txt','w')
        file.write(some)
        file.close()
    
    
i = 0
print(os.getcwd())
while True:
        check_button()
        i+=1
        if i==10000:
            print('Check tick at ',time.ctime(time.time()))
            i=0
