import os
import re
import socket
import time
import sys
import paramiko
import threading
import atexit
from getpass import getpass

# sudo apt-get install python3-paramiko
# sudo apt install xautomation

global ssh_obj
global closingApplication

numSamples = 100
zeroRoundTrip = False
droprates = [0, 10, 40]

print()
print('Number of samples', numSamples)

if not os.path.exists('fullyAutomatedLogs'):
	os.makedirs('fullyAutomatedLogs')

# Send a command to the linux terminal
def terminal(cmd):
	return os.popen(cmd).read()

# Send a command to the linux terminal
def resilient_terminal(cmd):
	try:
		return os.popen(cmd).read()
	except KeyboardInterrupt():
		pass

def call_ssh(cmd):
	#print('Calling ', cmd)
	ssh_stdin, ssh_stdout, ssh_stderr = ssh_obj.exec_command(cmd)
	outlines = ssh_stdout.readlines()
	response = ''.join(outlines)
	#print('Ending ', cmd)
	return response


def clearFilters():
	terminal(f'sudo tc qdisc del dev {interface} root netem > /dev/null 2>&1')

def applyFilters(droprate):
	if droprate != 0:
		terminal(f'sudo tc qdisc add dev {interface} root netem loss {droprate}%')

def networkDelimeter(serverIP):
	terminal(f'nc -vz {serverIP} 4433 >/dev/null 2>/dev/null')


threads = []

# Run a fuction in parallel to other code
class Task(threading.Thread):
	def __init__(self, name, function, *args):
		assert isinstance(name, str), 'Argument "name" is not a string'
		assert callable(function), 'Argument "function" is not callable'
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()

		self.setName(name)
		self.function = function
		self.args = args

	def run(self):
		self.function(*self.args)
		self._stop_event.set()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

# Creates a new thread and starts it
def create_task(name, function, *args):
	if len(threads) >= 200:
		# Remove the first 10 threads if it exceeds 200, to balance it out
		for i in range(10):
			threads[i].stop()
			del threads[i]
	task = Task(name, function, *args)
	threads.append(task)
	task.start()
	return task

# This function is ran when the script is stopped
def on_close():
	global closingApplication
	closingApplication = True
	print('Stopping active threads')

	stopServerSSH(serverIP)
	for thread in threads:
		thread.stop()
	stopTcpdump()
	
	print()
	print('Goodbye.')

atexit.register(on_close) # Make on_close() run when the script terminates

def getTcpdumpProcessID():
	output = terminal('ps -A | grep tcpdump')
	output = output.strip().split(' ')
	if len(output) == 0 or output[0] == '': return None
	pid = int(output[0])
	return pid

def stopTcpdump():
	pid = getTcpdumpProcessID()
	if pid != None:
		print('Stopping TCPDUMP...')
		call_ssh(f'sudo pkill -f tcpdump')

def startTcpdump(interface, algorithm, zeroRoundTrip):
	stopTcpdump()
	myCmd = f'python3 experiment_run_tcpdump.py {interface} {algorithm} {zeroRoundTrip} {numSamples}'
	print(myCmd)
	create_task('tcpdump', resilient_terminal, myCmd)

def startCPUlogger():
	print('Starting CPU logger...')
	myCmd = f'python3 experiment_log_cpu.py'
	print(myCmd)
	create_task('cpu logger', resilient_terminal, myCmd)


def getServerProcessID(serverIP):
	output = call_ssh('ps -A | grep bssl')
	output = output.strip().split(' ')
	if len(output) == 0 or output[0] == '': return None
	pid = int(output[0])
	return pid

def stopServerSSH(serverIP):
	pid = getServerProcessID(serverIP)
	if pid != None:
		print('Stopping server...')
		call_ssh(f'kill {pid}')
		#call_ssh(f'sudo pkill -f bssl')

def restartServerSSH(algorithm, serverIP):
	stopServerSSH(serverIP)
	print('Starting server...')
	output = call_ssh(f'python3 ~/oqs/boringssl/QUIC-project/experiment_droprate_server.py {algorithm} </dev/null &>/dev/null &')
	print()
	print('Server started! Waiting 5 seconds to be certain...')
	time.sleep(5)

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

bssl_dir = os.path.expanduser('~/oqs/boringssl/build/tool/bssl')

print()
print('PLEASE NOTE: To stop this application, trigger a core dump by using the sequence CTRL+[1 through 9].')
print()

client_ip = getIP()
print(f'Client IP: {client_ip}')
serverIP = input('Please enter the server IP: ')

ssh_port = 22
ssh_username = input('Enter server username: ')
ssh_password = getpass('Enter server password: ')
print('Server username:', ssh_username)
print('Server password:', ssh_password)
print()


interface = get_interfaces()

print('Connecting to SSH...')
ssh_obj = paramiko.SSHClient()
ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_obj.connect(serverIP, ssh_port, ssh_username, ssh_password)

startCPUlogger()

algorithms = ['rsa', 'dilithium2', 'dilithium3', 'dilithium5', 'falcon512', 'falcon1024'] #, 'rsa3072_dilithium2', 'rsa3072_dilithium3', 'rsa3072_falcon512', 'p256_dilithium2', 'p256_dilithium3', 'p256_dilithium4', 'p256_falcon512']

stopServerSSH(serverIP)
stopTcpdump()

numLoops = 0
closingApplication = False
while not closingApplication:
	try:
		for algorithm in algorithms:
			print(f'Using algorithm: "{algorithm}"')
			startTcpdump(interface, algorithm, zeroRoundTrip)
			time.sleep(1)

			cert_dir = os.path.expanduser(f'~/oqs/boringssl/QUIC-project/{algorithm}/key_CA.pem')
			myCmd=f'{bssl_dir} client -connect {serverIP}:44330 -root-certs {cert_dir}'

			# Full command:
			# ~/oqs/boringssl/build/tool/bssl client -connect 10.0.2.8:44330 -root-certs ~/oqs/boringssl/QUIC-project/rsa/key_CA.pem

			print('Starting...')

			clearFilters()
			networkDelimeter(serverIP)
			networkDelimeter(serverIP)
			networkDelimeter(serverIP)
			restartServerSSH(algorithm, serverIP)

			for droprate in droprates:
				print(f'Testing delay: {droprate}')
				samples = numSamples
				while samples > 0:

					try:
						clearFilters()
						networkDelimeter(serverIP)
						applyFilters(droprate)

						# Connect
						print('Starting client')

						terminal(myCmd)
						time.sleep(1)

						# Use xte to control user input --> send message
						#terminal("bash -c \"xte 'str AAAAAAAA' 'key Return'\" &")
						#terminal("xte 'str AAAAAAAA' 'key Return'")
						terminal("xte 'str AAAAAAAA' 'sleep 0.1' 'key Return' 'sleep 0.5' 'keydown Control_L' 'key C' 'keyup Control_L'")

						# Disconnect
						#print('Stopping client')
						#terminal("xte 'keydown Control_L' 'key C' 'keyup Control_L'")

					except KeyboardInterrupt:
						terminal("xte 'keyup Control_L'")


					samples -=1
				print('Waiting 3 minutes before starting next droprate test...')
				time.sleep(120)
			time.sleep(120)
			stopTcpdump()
		
		numLoops += 1
		print('Number of times through each algorithm:', numLoops)
	except KeyboardInterrupt():
		sys.exit()


print()
print('Experiment completed.')
