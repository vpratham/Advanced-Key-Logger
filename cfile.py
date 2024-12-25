#experimenting code modules
import os


#TODO: move this information to a more secure file
#error flag
flag = False
filename = os.getlogin() + ".txt"
dirname = ".cnfig"

def setupFiles(path):
    '''
    print(path)
    files = [f for f in os.listdir(path)]
    for file in files:
        print(file)
    '''

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