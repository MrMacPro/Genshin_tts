from ocr import ocr
import os

CACHE_DIR = "./cache/"

def write(flag):
    with open(CACHE_DIR + "dialogue_detector.txt", "w") as f:
        f.write("T" if flag else "F")

if not os.path.exists(CACHE_DIR + "dialogue_detector.txt"):
    with open(CACHE_DIR + "dialogue_detector.txt", "w") as f:
        f.write("F")

while True:
    try:
        write(ocr("GenshinImpact", "check_dialogue", 0.05, 0.03, 0.08, 0.06)[0] == "自动")
    except:
        write(False)