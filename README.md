
# CNT 5106 - Computer Networks - Project 1

## Implementation of FTP client and server

This project consists of a simple FTP server and client that can handle basic file transfer operations such as uploading and downloading files. 



## Authors

**Name**: Balasai Srikanth Ganti

**UFID** : 5251-6075



## Running the Server

To run the server, execute the following command in cmd prompt:
- `python FTPServer.py`


## Running the Client

To run the Client, execute the following command in cmd promt :
- `python FTPClient.py <port>`

Here the port number is mentioned as **5106**

### Commands

The server listens for client connections and handles each client session in a separate thread. It supports the following commands:

- `get <filename>`: Downloads a file from the server.
- `upload <filename>`: Uploads a file to the server.
- `quit`: Exits Server connection and terminates both Client and Server.

### Notes
- The server creates a new file with a new prefix for uploaded files to avoid overwriting existing files.
- The client creates a new file with a new prefix for downloaded files.
- Both the server and client use a chunk size of 1024 bytes for file transfer.






