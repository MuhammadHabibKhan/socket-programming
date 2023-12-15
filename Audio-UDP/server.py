# Server Side Code

import pyaudio
import socket
import hashlib
import struct

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def md5_verification(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum

# receiving client address and port number from initial connection

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(("127.0.0.1", 4444))

message, clientAddress = udp.recvfrom(1024)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK,
                )

while True:

    audioData = stream.read(CHUNK)

    # md5sum = md5_verification(audioData)
    # md5sum_binary = md5sum.encode()
    # md5sum_length = len(md5sum_binary)
    # print(md5sum_length)
    # md5sum_length_binary = struct.pack('!I', md5sum_length)

    # udp.sendto(md5sum_length_binary + md5sum_binary + audioData, (clientAddress))

    udp.sendto(audioData, (clientAddress))

udp.close()