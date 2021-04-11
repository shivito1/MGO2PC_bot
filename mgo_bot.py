import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
import win32gui
import pyautogui
from time import strftime


class mgobot:
    def __init__(self):
        self.toplist, self.winlist = [], []
        self.debuging = True
        self.fromfile = True
        self.in_game_boundaries = [  # BGR
            ([0, 179, 105], [38, 255, 167]),  # green
            ([198, 199, 198], [255, 255, 255]),  # white
            ([59, 126, 137], [91, 170, 255]),  # orange
            ([188, 124, 115], [255, 200, 180]),  # blue player text
            ([134, 155, 81], [255, 162, 133]), # blue player name
            ([87, 105, 136], [125, 141, 255])  # red player name
        ]

        self.screen_text = {}
        self.curent_color = ''

        # boundaries = [
        #    ([17, 15, 100], [50, 56, 200]),
        #    ([86, 31, 4], [220, 88, 50]),
        #    ([25, 146, 190], [62, 174, 250]),
        #    ([103, 86, 65], [145, 133, 128])
        # ]

        # self.cv2_from_file()
        # self.np_array()
        self.cv2_from_screen()

    # time.sleep(3)

    def resize_cv2(self, img):
        scale_percent = 60  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    def save_full(self, image):
        image = cv2.cvtColor(np.array(image),
                             cv2.COLOR_RGB2BGR)
        #cv2.imwrite("FULL_screen " + strftime("%H-%M-%S") + ".png", image)
        return image

    def cv2_from_screen(self):
        pytesseract.pytesseract.tesseract_cmd = r"L:\Program Files\Tesseract-OCR\tesseract.exe"

        def enum_cb(hwnd, results):
            if 'FPS:' in win32gui.GetWindowText(hwnd):  # FPS:
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
                self.winlist.append(hwnd)

        win32gui.EnumWindows(enum_cb, None)
        win32gui.EnumWindows(enum_cb, None)
        win32gui.SetForegroundWindow(self.winlist[0])

        image = pyautogui.screenshot()

        if self.fromfile:
            image = cv2.imread("FULL_screen 18-29-45.png")
        else:
            image = cv2.cvtColor(np.array(image.crop(box=[0, 800, 1500, 1080])),
                             cv2.COLOR_RGB2BGR)  # COLOR_RGB2BGR and COLOR_BGR2GRAY
        #if self.debuging:
        #    image = self.save_full(image)

        # image = cv2.imread("test3.png")
        # image = image[700:1200, 0:1900]

        for (lower, upper) in self.in_game_boundaries:

            if lower == self.in_game_boundaries[0][0]:
                self.curent_color = 'green'
            elif lower == self.in_game_boundaries[1][0]:
                self.curent_color = 'white'
            elif lower == self.in_game_boundaries[2][0]:
                self.curent_color = 'orange'
            elif lower == self.in_game_boundaries[3][0]:
                self.curent_color = 'blue'
            elif lower == self.in_game_boundaries[4][0]:
                self.curent_color = 'blue name'
            elif lower == self.in_game_boundaries[5][0]:
                self.curent_color = 'red name'

            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)

            if self.curent_color == 'green':
                self.screen_text["green"] = output
                if self.debuging:
                    cv2.imshow("green", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)
                text = pytesseract.image_to_string(output, lang='eng')
                print("green: " + str(text.split('\n')))
            elif self.curent_color == 'white':
                self.screen_text["white"] = output
                if self.debuging:
                    cv2.imshow("white", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)
                text = pytesseract.image_to_string(output, lang='eng')
                print("white: " + str(text.split('\n')))

            elif self.curent_color == 'orange':
                print(lower,upper)
                lower = np.array(self.in_game_boundaries[1][0], dtype="uint8")
                upper = np.array(self.in_game_boundaries[1][1], dtype="uint8")
                mask2 = cv2.inRange(image, lower, upper)
                mask1 = cv2.bitwise_or(mask,mask2)
                output = cv2.bitwise_and(image, image, mask=mask1)
                #self.screen_text["orange"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("orange: " + str(text.split('\n')))
                if self.debuging:
                    cv2.imshow("orange", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)
                # show the images
            elif self.curent_color == 'blue':
                self.screen_text["orange"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("blue: " + str(text.split('\n')))
                # show the images
                if self.debuging:
                    cv2.imshow("blue", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)
            elif self.curent_color == 'blue name':
                self.screen_text["orange"] = output
                text = pytesseract.image_to_string(output, lang='eng')
                print("blue name: " + str(text.split('\n')))
                # show the images
                if self.debuging:
                    cv2.imshow("blue name", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)
            elif self.curent_color == 'red name':
                self.screen_text["red name"] = output
                lower = np.array(self.in_game_boundaries[2][0], dtype="uint8")
                upper = np.array(self.in_game_boundaries[2][1], dtype="uint8")
                mask2 = cv2.inRange(image, lower, upper)
                mask1 = cv2.bitwise_or(mask,mask2)
                output = cv2.bitwise_and(image, image, mask=mask1)
                text = pytesseract.image_to_string(output, lang='eng')
                print("red name: " + str(text.split('\n')))
                # show the images
                if self.debuging:
                    cv2.imshow("red name", np.hstack([self.resize_cv2(image), self.resize_cv2(output)]))
                    cv2.waitKey(0)

            # show the images
            # cv2.imshow("images", np.hstack([image, output]))
            # cv2.waitKey(0)

        # show image
        # cv2.imshow("screen", image)
        # cv2.waitKey(0)
        cv2.imwrite("screen " + strftime("%H-%M-%S") +".png",image)


mgobot()
