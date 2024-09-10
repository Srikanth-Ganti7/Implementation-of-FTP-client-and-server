# Description: This is a simple FTP client program that can upload and download files from the server.
# The client program connects to the server and sends commands to upload or download files.



# Importing required libraries
import socket
import sys

# Function to upload file to the server
def upload_file(client_socket, filename):
    client_socket.send(f'upload {filename}'.encode())
    response = client_socket.recv(1024)
    if response == b'READY':
        with open(filename, 'rb') as f:
            chunk = f.read(1024)
            while chunk:
                client_socket.send(chunk)
                chunk = f.read(1024)
        client_socket.send(b'ENDED')
    else:
        print('Upload failed')

# Function to download file from the server
def download_file(client_socket, filename):
    client_socket.send(f'get {filename}'.encode())
    response = client_socket.recv(1024)
    if response == b'BEGIN':
        with open(f'new{filename}', 'wb') as f:
            while True:
                chunk = client_socket.recv(1024)
                if chunk.endswith(b'ENDED'):
                    chunk = chunk[:-5]
                    f.write(chunk)
                    break
                f.write(chunk)
        print(f'File {filename} has been successfully downloaded.')  # Print statement after successful download
    elif response == b'ERROR':
        print(f'File {filename} is not available on the server.')  # Print statement when file not found


# Main function
def main():
    if len(sys.argv) < 2:
        print("Missing port number or Incorect FIlename: FTPclient <port>")
        return
    
    port = int(sys.argv[1])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    
    while True:
        command = input("Enter command (upload <filename> / get <filename> / quit): ")
        # Get user input
        if command.startswith("upload"):
            _, filename = command.split()
            upload_file(client_socket, filename)
        elif command.startswith("get"):
            _, filename = command.split()
            download_file(client_socket, filename)
        # elif command == "quit":
        #     break
            
        elif command == "quit":
            client_socket.send(command.encode())  # Send 'quit' to the server
            break  # Exit the loop

        else:
            print("Invalid command. Please use 'upload <filename>', 'download <filename>', or 'quit'.")

    client_socket.close()

if __name__ == '__main__':
    main()