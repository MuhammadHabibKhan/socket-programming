# Client Side Code

import pyaudio
import socket
import struct
import hashlib

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def md5_verification(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum


# Initial message to establish connection to server

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = "Init"
udp.sendto(message.encode(),("127.0.0.1", 4444))

print(message)

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                output = True,
                frames_per_buffer = CHUNK,
                )

while True:
    # md5um_length_data = udp.recv(4)

    # if not md5um_length_data:
    #     break

    # md5sum_length = struct.unpack('!I', md5um_length_data)[0]

    # md5sum_data = udp.recv(md5sum_length)
    # soundData = udp.recv(CHUNK * CHANNELS * 2)
    # received_md5sum = md5_verification(soundData)

    # if received_md5sum == md5sum_data.decode():
    #     stream.write(soundData, CHUNK)
    
    # else:
    #     print("Data corruption detected. Ignoring the packet.")

    soundData, addr = udp.recvfrom(CHUNK * CHANNELS * 2)
    stream.write(soundData, CHUNK)

udp.close()