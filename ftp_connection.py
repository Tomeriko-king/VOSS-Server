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





