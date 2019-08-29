import cv2
import time
import dataStructers
import threading

class CamWork():
    def __init__(self):
        print('PhotoMaker')
    def MakePhotoBoard(self, cam, namephoto):
        # self.robot.set_digital_out(dataStructers.led_flash, True)
        time.sleep(1)
        ret, image = cam.read()
        ret, image = cam.read()

        # self.robot.set_digital_out(dataStructers.led_flash, False)

        # image = image[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]

        image = cv2.GaussianBlur(image, (3, 3), 0)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        path = 'images/' + str(namephoto) + str(1) + '.bmp'

        cv2.imwrite(path, image)
        return 0
    def MakePhotoTest(self, cam):

        ret, frame = cam.read()
        refPt = dataStructers.playerTwoRfPt
        frame = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imwrite('ts.png', frame)
