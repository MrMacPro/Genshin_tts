import easyocr
import win32gui
from PyQt5.QtWidgets import QApplication
import sys
import os

CACHE_DIR = "C:/Users/zshha/Documents/Genshin_tts/cache/"

def take_screenshot(process_name, corners: list, task_name):
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)

    hwnd = win32gui.FindWindow(None, process_name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()

    width = img.width()
    height = img.height()
    if corners[0] <= 1 and corners[1] <= 1 and corners[2] <= 1 and corners[3] <= 1:
        img = img.copy(int(corners[0]*width), int(corners[1]*height), int((corners[2]-corners[0])*width), int((corners[3]-corners[1])*height))
    elif corners[2] > 1 and corners[3] > 1:
        img = img.copy(corners[0], corners[1], corners[2]-corners[0], corners[3]-corners[1])

    file_name = CACHE_DIR + task_name + ".png"
    img.save(file_name)

    return file_name

def ocr(process_name, task_name, left_top, left_bottom, right_top, right_bottom, lang=['ch_sim', 'en']):
    file_name = take_screenshot(process_name, [left_top, left_bottom, right_top, right_bottom], task_name)
    reader = easyocr.Reader(lang)
    text = reader.readtext(file_name)
    os.remove(file_name)
    return [i[1] for i in text]