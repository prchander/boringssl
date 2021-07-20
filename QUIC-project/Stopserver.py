import os

# Send a command to the linux terminal
def terminal(cmd):
	#print(cmd)
	return os.popen(cmd).read()

def getServerProcessID():
	output = terminal('ps -A | grep bssl')
	output = output.strip().split(' ')
	if len(output) == 0 or output[0] == '': return None
	pid = int(output[0])
	return pid

def stopServer():
	pid = getServerProcessID()
	if pid != None:
		print('Stopping server...')
		terminal(f'kill {pid}')

stopServer()