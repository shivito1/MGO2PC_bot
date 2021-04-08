import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import win32gui
import pyautogui
import time


class mgobot:
    def __init__(self):
        self.toplist, self.winlist = [], []
        self.boundaries = [  # BGR
            ([0, 179, 105], [38, 255, 167]),  #green
            ([150, 150, 150], [255, 255, 255]),  #white
            ([59, 108, 137], [91, 170, 255]),  #orange
            ([188, 124, 115], [254, 196, 166])  #blue player text
        ]

        self.screen_text = {}
        self.curent_color = ''

        #boundaries = [
        #    ([17, 15, 100], [50, 56, 200]),
        #    ([86, 31, 4], [220, 88, 50]),
        #    ([25, 146, 190], [62, 174, 250]),
        #    ([103, 86, 65], [145, 133, 128])
        #]

        #self.cv2_from_file()
        #self.np_array()
        self.cv2_from_screen()

    # time.sleep(3)

    def cv2_from_screen(self):
        pytesseract.pytesseract.tesseract_cmd = r"L:\Program Files\Tesseract-OCR\tesseract.exe"
        def enum_cb(hwnd, results):
            if 'FPS:' in win32gui.GetWindowText(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
                self.winlist.append(hwnd)

        win32gui.EnumWindows(enum_cb, None)
        win32gui.EnumWindows(enum_cb, None)
        win32gui.SetForegroundWindow(self.winlist[0])

        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image.crop(box=[0, 800, 1500, 1080])), cv2.COLOR_RGB2BGR) #COLOR_RGB2BGR and COLOR_BGR2GRAY

        #image = cv2.imread("test3.png")
        #image = image[700:1200, 0:1900]



        for (lower, upper) in self.boundaries:
            if lower == [0, 179, 105]:
                self.curent_color = 'green'
            elif lower == [233, 233, 233]:
                self.curent_color = 'white'
            elif lower == [59, 108, 137]:
                self.curent_color = 'orange'
            elif lower == [188, 124, 115]:
                self.curent_color = 'blue'


            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)

            if self.curent_color == 'green':
                self.screen_text["green"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("cv2: " + str(text.split('\n')))
            elif self.curent_color == 'white':
                self.screen_text["white"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("cv2: " + str(text.split('\n')))
            elif self.curent_color == 'orange':
                self.screen_text["orange"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("cv2: " + str(text.split('\n')))

                cv2.imshow("images", output)
                cv2.waitKey(0)
                # show the images
            elif self.curent_color == 'blue':
                self.screen_text["orange"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("cv2: " + str(text.split('\n')))
                # show the images
                cv2.imshow("images", output)
                cv2.waitKey(0)

            # show the images
            #cv2.imshow("images", np.hstack([image, output]))
            #cv2.waitKey(0)

        #show image
        #cv2.imshow("screen", image)
        #cv2.waitKey(0)


mgobot()
