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
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establising connection with server address and port no
client_socket.connect(("127.0.0.1", 4444))

p = pyaudio.PyAudio()

# output set to true so that client receives the audio FROM server (as specified in the assignment) 
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

while True:
    # Calculate md5sum
    md5um_length_data = client_socket.recv(4)

    # conditional check to break the loop if length not received
    if not md5um_length_data:
        break

    # unpacking the length back to 32 (int) from 4-byte unsigned int format {32 character - 32 bytes as hexdigest converted it into 32 characters}
    md5sum_length = struct.unpack('!I', md5um_length_data)[0]

    # Receive the checksum data
    md5sum_data = client_socket.recv(md5sum_length)

    # File data received per frame 1024 bytes (i.e Chunk size)
    # But we multiply by channels to account for left and right sources if stereo audio
    # and multiply by 2 because audio is in 16-bit unsigned integer form. 16-bit unsigned int takes 2 bytes of data, hence we xply by 2
    soundData = client_socket.recv(CHUNK * CHANNELS * 2)

    # calculating checksum on received sound data
    received_md5sum = md5_verification(soundData)

    # comparing the md5sums and only then outputing the audio
    if received_md5sum == md5sum_data.decode():
        print("Checksum Validated")
        stream.write(soundData, CHUNK)
    
    else:
        print("Data corruption detected. Ignoring the packet.")

client_socket.close()