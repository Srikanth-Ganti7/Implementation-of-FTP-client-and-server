# Description: A simple FTP server that can handle 'get' and 'upload' commands from a client.
# The server listens for client connections and handles each client session in a separate thread.
# The server can handle multiple clients simultaneously.

# Importing required libraries
import socket
import os

# Constants
CHUNK_SIZE = 1024
FILE_END_MARKER = b'ENDED'

# Function to send file to the client
def send_file(connection, file_path):
    with open(file_path, 'rb') as file:
        data_chunk = file.read(CHUNK_SIZE)
        while data_chunk:
            connection.send(data_chunk)
            data_chunk = file.read(CHUNK_SIZE)
    connection.send(FILE_END_MARKER)

# Function to receive file from the client
def receive_file(connection, file_path):
    with open(file_path, 'wb') as file:
        while True:
            data_chunk = connection.recv(CHUNK_SIZE)
            if data_chunk.endswith(FILE_END_MARKER):
                data_chunk = data_chunk[:-len(FILE_END_MARKER)]
                file.write(data_chunk)
                break
            file.write(data_chunk)

# Function to handle the 'get' command
def handle_get(connection, command):
    file_path = command.split()[1]
    if os.path.exists(file_path):
        connection.send(b'BEGIN')
        send_file(connection, file_path)
    else:
        connection.send(b'ERROR: File does not exist.')

# Function to handle the 'upload' command
def handle_upload(connection, command):
    file_path = "new" + command.split()[1]
    connection.send(b'READY')
    receive_file(connection, file_path)
    print(f'File {file_path} uploaded successfully.')

# Function to handle unknown commands
def handle_unknown(connection, _):
    connection.send(b'ERROR: Unknown command.')

# Function to handle the client session
def client_session(connection):
    command_handlers = {
        'get': handle_get,
        'upload': handle_upload,
    }
    
    quit_received = False
    while True:
        client_command = connection.recv(CHUNK_SIZE).decode()
        if not client_command:  # Check for empty byte string indicating client disconnection
            print("Client disconnected, closing connection.")
            break

        action = client_command.split()[0].lower()
        if action == "quit":
            print("Quit command received, closing client connection.")
            quit_received = True
            break

        handler = command_handlers.get(action, handle_unknown)
        handler(connection, client_command)

    connection.close()
    return quit_received

# Function to run the server
def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f'Server is running on port {port}')

    # Accept client connections
    try:
        while True:
            client_connection, _ = server_socket.accept()
            if client_session(client_connection):
                print("Quit command received from a client, shutting down server.")
                break
    # Gracefully handle server shutdown
    finally:
        server_socket.close()
        print("Server has been shut down.")

# Main function
if __name__ == '__main__':
    run_server(5106)
