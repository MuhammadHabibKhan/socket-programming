# Socket Programming

* Read these instructions to make sure the files work correctly and as intended *

## Pre-Requisites:

1) Python 3
2) Pip

## Instructions

------------------------------------------------------------
### FILE TRANSFER - WITH ERROR CHECKING AND HANDLING
------------------------------------------------------------

1) The files for regular file transfer programs are stored in the sub-folder "File-TCP"
2) As the name suggests, it is made using TCP sockets
3) The test file is an mp4 file present in the sub-folder named "chamber.mp4"
4) The file will be stored in the same sub-folder as "received-chamber.mp4" after the transfer

Follow these steps to ensure the code runs correctly

[1] Open the sub-folder "File-TCP" in your IDE or type "cd file-tcp" in terminal to switch to it if in main folder
[2] Create a new terminal in your IDE
[3] Type "python server.py" to fire up the server first. Successful run will be indicated by a message
[4] Repeat steps [1] and [2]
[5] Type "python client.py" in the terminal to start the file transfer. Successful file transfer will be indicated by a message

Note: Make sure that no other services are running on the specified host name and port number combination. Change accordingly

---------------------------------------------------------------------------------
### LIVE AUDIO TRANSFER - FROM SERVER TO CLIENT - WITH ERROR CHECKING AND HANDLING
---------------------------------------------------------------------------------

Note: While typically audio broadcasts are sent using UDP sockets, the additional requirement of handling and checking error prompted me to add md5sum checking here as well
to ensure files were being transferred correctly. However, while doing so, the UDP did not allow to send the audio Data along with md5sum data, possibly because of the limit on UDP.
The following error was encountered "OSError: [WinError 10040] A message sent on a datagram socket was larger than the internal message buffer or some other network limit, or the 
buffer used to receive a datagram into was smaller than the datagram itself". That meant I may need to fragment the data since UDP does not support it. 

Instead I ended up using TCP along with additional md5sum checking for better handling of data to send the audio. This lead to increased overhead but a lossless and secure transmission of audio.
I have included both solutions, with sub-folders "Audio-TCP" and "Audio-UDP". The UDP one does not implement any checking and the code for md5sum is currently commented out. 
The instructions here are only for TCP solution however it will be mostly same to run them. 

-> The solution is present in the sub-folder "Audio-TCP"
-> Install PyAudio - Type "pip install PyAudio" in terminal to install 
-> Ensure that you have a working microphone on your system

Follow these steps to ensure the code runs correctly

[1] Open the sub-folder "Audio-TCP" in your IDE or type "cd audio-tcp" in terminal to switch to it if in main folder
[2] Create a new terminal in your IDE 
[3] Type "python server.py" to fire up the server first. Successful run will be indicated by a message
[4] Repeat steps [1] and [2]
[5] Type "python client.py" in the terminal to start the live audio broadcast
[6] Speak into your microphone and hear it through your speakers

# Recommendations: 
- Sit in a quiet room. Use headphones to avoid audio playback loop between your microphone and speakers. 
- Do not attach/detach your microphone and audio output devices in the middle of transmission.  
