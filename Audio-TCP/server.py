import socket
import pyaudio
import struct
import hashlib


# A "chunk" is a block of audio data containing a fixed number of samples
# A "sample" refers to a single data point that represents the amplitude (loudness) of an audio signal at a specific point in time.
# Audio is continuously changing, and to capture it in digital form, it is discretized at regular intervals. Each of these intervals is called a "sample."
# I select a smaller chunk size to reduce latency since I already have a lot of overhead due to md5sum and TCP connection
CHUNK = 512

# Audio sent in the format of PyAudio's 16-bit unsigned integer format
FORMAT = pyaudio.paInt16

# Channels refer to the number of independent audio signals that are combined to create a sound. 
# 1 means mono audio (from a single source)
# 2 means stereo audio (meaning audio from left and right source will be distinguished) Need a stereo mic to work properly so I use mono here
CHANNELS = 1

# The sample rate (often measured in Hertz, or Hz) determines how many samples are taken per second.
# I keep the rate a bit high to account for the loss of quality with low chunk size but not too high (48000 or more) or I get increased latency
RATE = 44100

# Implementing MD5 digestion algorithm for the validation and verification of data sent as required in the instructions of assignment to ensure correct transfer of data files
# The hashlib.md5 function creates a hash value of our data which is then converted into hexadecimal using .hexdigest() for convenience. 
# just like the traditional checksum, we can compare the value of md5sum calculated at client and server side to validate data

def md5_verification(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum


# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding address and port number to server
server_socket.bind(("127.0.0.1", 4444))
# server can listen upto 1 client at max at a time 
server_socket.listen(1)

print("Server is listening on port 4444")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Connection from", client_address)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    
    # audio_data = stream.read(CHUNK)
    # client_socket.sendall(audio_data)

    # reading 1024 bytes or 1 MB Datagram from our audio Data
    audioData = stream.read(CHUNK)

    # calculating md5sum
    md5sum = md5_verification(audioData)

    # convert the md5sum to UTF-8 encoding (data in bytes)
    md5sum_binary = md5sum.encode()

    # Calculate the length of checksum in bytes (32 bytes since UTF-8 binary from hexadecimal representation is 32 characters or 32 bytes)
    md5sum_length = len(md5sum_binary)

    # packing the length of checksum in unsigned integer format of 4 bytes (hence why we recv(4) on server side for cheksum length)
    md5sum_length_binary = struct.pack('!I', md5sum_length)

    # Send the length of checksum, the binary checksum, and the data
    client_socket.send(md5sum_length_binary + md5sum_binary + audioData)

client_socket.close()
server_socket.close()