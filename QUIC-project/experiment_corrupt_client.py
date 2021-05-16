import os
import re
import socket
import time

numSamples = 1000
zeroRoundTrip = True
corrupt = [0, 10, 40]

# Send a command to the linux terminal
def terminal(cmd):
	#print(cmd)
	return os.popen(cmd).read()

def clearFilters():
	terminal(f'sudo tc qdisc del dev {interface} root netem')

def applyFilters(percent):
	if percent != 0:
		terminal(f'sudo tc qdisc add dev {interface} root netem corrupt {percent}%')

def networkDelimeter(serverIP):
	terminal(f'nc -vz {serverIP} 4433 >/dev/null 2>/dev/null')

def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	return s.getsockname()[0]

# Return an array of networking interfaces
def get_interfaces():
	raw = terminal('ip link show')
	interfaces = re.findall(r'[0-9]+: ([^:]+): ', raw)
	interfaces.remove('lo')

	interface = ''
	if len(interfaces) == 0:
		print(terminal('ifconfig'))
		print()
		print('No networking interfaces were found.')
		sys.exit()

	elif len(interfaces) == 1:
		interface = interfaces[0]

	else:
		for i in range(0, len(interfaces)):
			print(f'{i + 1} : {interfaces[i]}')
		selection = -1
		while selection < 1 or selection > len(interfaces):
			try:
				selection = int(input(f'Please select an interface (1 to {len(interfaces)}): '))
			except: pass
		interface = interfaces[selection - 1]
		print()
	return interface

lsquic_dir = os.path.expanduser('~/oqs/lsquic')

client_ip = getIP()
print(f'Client IP: {client_ip}')
serverIP = input('Please enter the server IP: ')
interface = get_interfaces()

try:
	os.remove('0rttTest.txt')
except: pass

if zeroRoundTrip:
	myCmd= f'{lsquic_dir}/build/bin/./http_client -0 0rttTest.txt -H www.example.com -s {serverIP}:4433 -p /'
else:
	myCmd= f'{lsquic_dir}/build/bin/./http_client -H www.example.com -s {serverIP}:4433 -p /'



for percent in corrupt:
	print(f'Testing delay: {percent}')
	samples = numSamples
	while samples > 0:

		clearFilters()
		networkDelimeter(serverIP)
		applyFilters(percent)

		os.system(myCmd)
		samples -=1
	print('Waiting 3 minutes before starting next corruption% test...')
	time.sleep(180)

print()
print('Experiment completed.')
