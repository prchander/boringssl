import os
import socket
import time
import datetime

print('Client has started.')

def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	return s.getsockname()[0]

def pause_until_next_minute():
	minute = datetime.datetime.now().minute
	print(f'Waiting until minute: { minute + 1 }')
	while minute == datetime.datetime.now().minute:
		time.sleep(0.001)
	print('Starting...')

#pause_until_next_minute()
#time.sleep(1)
print(f'Client IP: {getIP()}')

numSamples = 1
serverIP = input('Enter the server IP address: ') #getIP() #'10.0.0.235'

lsquic_dir = os.path.expanduser('~/oqs/lsquic')
myCmd = f'{lsquic_dir}/build/./research_client -H www.example.com -s {serverIP}:4433 -g -j'

startTime = time.time()

for i in range(numSamples):
	os.system(myCmd)

endTime = time.time()

print ("Time Taken: ")
print (endTime - startTime)