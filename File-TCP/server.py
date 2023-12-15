import socket
import hashlib
import struct


# Implementing MD5 digestion algorithm for the validation and verification of data sent as required in the instructions of assignment to ensure correct transfer of data files
# The hashlib.md5 function creates a hash value of our data which is then converted into hexadecimal using .hexdigest() for convenience. 
# just like the traditional checksum, we can compare the value of md5sum calculated at client and server side to validate data

def md5_verification(data):

    checksum = hashlib.md5(data).hexdigest()
    return checksum


def receive_file(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # binding the host and port no to the server (provided through arguments)
        server_socket.bind((host, port))
        
        # server may listen upto 5 devices at once | current implementation causes server to hit finally and close the connection as soon as first client closes its connection
        server_socket.listen(5)
        print("Server is listening on port", port)

        # as soon as a client connects, we accept it and store its IP and port no
        client_socket, addr = server_socket.accept()
        print("Connection from", addr)

        # writing a file in binary mode name "chamber-received" (chamber is the name of original file)
        with open('chamber-received.mp4', 'wb') as file:
            
            while True:

                # Receive the length of checksum (as written in server side code, 4 bytes received as length sent in unsigned 4-byte format)
                checksum_length_data = client_socket.recv(4)
                
                # conditional check to break the loop if length not received
                if not checksum_length_data:
                    break
                
                # unpacking the length back to 32 (int) from 4-byte unsigned int format {32 character - 32 bytes as hexdigest converted it into 32 characters}
                checksum_length = struct.unpack('!I', checksum_length_data)[0] #
                
                # Receive the checksum data
                checksum_data = client_socket.recv(checksum_length)
                # File data received per frame in 1024 bytes of 1MB Datagrams
                file_data = client_socket.recv(1024)

                # Calculate checksum on received data
                received_checksum = md5_verification(file_data)

                # If server and client side md5sum matches then write our file else print corruption packet message
                if received_checksum == checksum_data.decode():
                    file.write(file_data)
                else:
                    print("Data corruption detected. Ignoring the packet.")
                    # break here? or TCP handles it by itself?

        print("File received successfully")

    except Exception as e:
        print("Error:", str(e))
    
    finally:
        print("Server Connection closed")
        server_socket.close()

if __name__ == '__main__':

    host = 'localhost'
    port = 4545
    receive_file(host, port)