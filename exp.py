import threading 
from script import keyPressed, buffer_words
import re
import time
from functools import partial
from pynput import keyboard

stop_event = threading.Event()
buffer_local= []

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
    
    #listner.stop()
    buffer_local = buffer_words
    #print(buffer_words)

if __name__ == "__main__":
    FILE_PATH = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"

    t1 = threading.Thread(target=keyboard_logger_pathed_without_timer, name='logger', args=(FILE_PATH,))

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