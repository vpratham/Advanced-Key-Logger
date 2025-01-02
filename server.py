import socket
from key import HOST,PORT

target = '' #file path of your locally stored file

def start_ftp_server(host, port, target):
    """
    RECIEVES A FILE FROM A CLIENT ON PORT, STORES IT AT TARGET FILE LOCATION ON THE SERVER

    Arguments:
        host (str): Server IP address
        port (int): Port used by the server
        target (str): File path where the files are stored
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(1)

    try:
        while True:
            client_socket, client_addr = server_socket.accept()

            with client_socket:
                with open(target, 'a') as file:
                    while True:
                        data = client_socket.recv(1024).decode('utf-8')
                        if not data or data == "END":
                            break
                        file.write(data)
                    print("File recieved")
                    client_socket.sendall(b"1")
    except KeyboardInterrupt:
        print("Server shutting down")
        server_socket.close()
    except Exception as e:
        print("Error has occured")
        print(e)
    finally:
        server_socket.close()

start_ftp_server(HOST, PORT, target)