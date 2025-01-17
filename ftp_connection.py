from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP

def run_ftp_server():
    # Instantiate an authorizer object to manage authentication
    authorizer = DummyAuthorizer()

    # Add user permission
    # Arguments: user, password, directory, permission
    # 'elradfmw' gives full permissions (read/write) on the given directory
    authorizer.add_user("user", "password", "C:\Ftp", perm="elradfmw")

    # Create an FTP handler instance to handle FTP requests
    handler = FTPHandler
    handler.authorizer = authorizer

    # Create the FTP server
    server = FTPServer(("0.0.0.0", 21), handler)  # Listen on all interfaces on port 21
    print("FTP server started on port 21...")

    # Start the server
    server.serve_forever()



def upload_file():
    # Connect to the FTP server
    ftp = FTP()
    ftp.connect('127.0.0.1', 21)  # Replace with your server's IP and port if needed
    ftp.login('user', 'password')  # Login with the username and password you set

    # Path to the file you want to upload
    local_file = 'path/to/local/file.txt'  # Change this to the path of your file
    remote_file = 'file.txt'  # Remote file name on the server

    # Open the local file and upload it
    with open(local_file, 'rb') as f:
        ftp.storbinary(f"STOR {remote_file}", f)

    print(f"File '{local_file}' uploaded successfully.")

    # Close the FTP connection
    ftp.quit()



def download_file():
    # Connect to the FTP server
    ftp = FTP()
    ftp.connect('127.0.0.1', 21)  # Replace with your server's IP and port if needed
    ftp.login('user', 'password')  # Login with the username and password you set

    # Path to the remote file you want to download
    remote_file = 'file.txt'  # Name of the file on the server
    local_file = 'path/to/local/save/location/file.txt'  # Path to save the downloaded file locally

    # Open a local file to save the downloaded file
    with open(local_file, 'wb') as f:
        ftp.retrbinary(f"RETR {remote_file}", f.write)

    print(f"File '{remote_file}' downloaded successfully.")

    # Close the FTP connection
    ftp.quit()
