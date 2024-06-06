import psutil
import os
from read_lib import read_lib
import ngender
from ocr import ocr
import difflib
import threading

CACHE_DIR = "./cache/"

PAIMON_VOICE = "zh-CN-XiaoxiaoNeural"
FEMALE_VOICE = "zh-CN-XiaoxiaoNeural"
MALE_VOICE = "zh-CN-YunxiNeural"

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def solve_text(text):
    result = text.replace(" ", "")
    return result

def check_process_running():
    for process in psutil.process_iter():
        if process.name() == "GenshinImpact.exe":
            print(f"Detected:{process.name()}")
            return True
    return False

def in_dialogue():
    try:
        return ocr("GenshinImpact", "check_dialogue", 0.05, 0.03, 0.08, 0.06)[0] == "自动"
    except:
        return False

def get_dialogue():
    name = ocr("GenshinImpact", "get_name", 0, 0.78, 1, 0.84)[0]
    dialogue = ocr("GenshinImpact", "get_dialogue", 0, 0.84, 1, 0.97)
    dialogue = "".join(dialogue)
    dialogue = solve_text(dialogue)
    dialogue = dialogue.replace("EZ4ZSH", "旅行者")
    print(name +":"+ dialogue)
    return name, dialogue
    
def person_to_voice(person):
    def check_gender(person):
        d = read_lib()
        if person in d.keys():
            return d[person]
        else:
            return "男" if ngender.guess(person)[0] == "male" else "女"
        
    if person == "派蒙":
        return PAIMON_VOICE
    if check_gender(person) == "女":
        return FEMALE_VOICE
    else:
        return MALE_VOICE

last_text = ""
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

while True:
    try:
        if check_process_running():
            print("Running...")
            if in_dialogue():
                print("In dialogue...")
                person, text = get_dialogue()
                if string_similar(text, last_text) < 0.9 and text.endswith(('.', '!', '?', '。', '！', '？', "…")):
                    os.system(f"edge-tts --rate=+10% --text '{text}' --voice {person_to_voice(person)} --write-media {CACHE_DIR}voice.wav")
                    os.system("mpv " + CACHE_DIR + "voice.wav")
                    os.remove(CACHE_DIR + "voice.wav")
                    last_text = text
    except KeyboardInterrupt:
        for file_name in os.listdir(CACHE_DIR):
            os.remove(CACHE_DIR + file_name)
        exit()
    except:
        pass