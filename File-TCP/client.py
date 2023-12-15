import socket
import hashlib
import struct


# Implementing MD5 digestion algorithm for the validation and verification of data sent as required in the instructions of assignment to ensure correct transfer of data files
# The hashlib.md5 function creates a hash value of our data which is then converted into hexadecimal using .hexdigest() for convenience. 
# just like the traditional checksum, we can compare the value of md5sum calculated at client and server side to validate data

def md5_verification(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum


def send_file(filename, host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # opening file in read-binary mode
        with open(filename, 'rb') as file:
            
            # sending datagrams each of size 1024 bytes or 1MB
            data = file.read(1024)

            while data:
                # Calculate md5sum
                checksum = md5_verification(data)
                # convert the md5sum to UTF-8 encoding (data in bytes)
                checksum_binary = checksum.encode()
                
                # Calculate the length of checksum in bytes
                checksum_length = len(checksum_binary)
                # packing the length of checksum in unsigned integer format of 4 bytes (hence why we recv(4) on server side for cheksum length)
                checksum_length_binary = struct.pack('!I', checksum_length) #
                
                # Send the length of checksum, the binary checksum, and the data
                client_socket.send(checksum_length_binary + checksum_binary + data)

                data = file.read(1024)

        print("File sent successfully, Monsieur")
    
    except Exception as e:
        print("Error:", str(e))
    
    finally:
        print("Client Connection closed")
        client_socket.close()

if __name__ == '__main__':

    host = 'localhost'
    port = 4545
    filename = "chamber.mp4"
    send_file(filename, host, port)