import os

# Send a command to the linux terminal
def terminal(cmd):
	#print(cmd)
	return os.popen(cmd).read()

def getTcpdumpProcessID():
	output = terminal('ps -A | grep tcpdump')
	output = output.strip().split(' ')
	if len(output) == 0 or output[0] == '': return None
	pid = int(output[0])
	return pid

def getServerProcessID():
	output = terminal('ps -A | grep bssl')
	output = output.strip().split(' ')
	if len(output) == 0 or output[0] == '': return None
	pid = int(output[0])
	return pid


tdp_dump_running = getTcpdumpProcessID()

if tdp_dump_running is not None:
	print('TCPDUMP: RUNNING')
else:
	print('TCPDUMP: STOPPED')

server_pid = getServerProcessID()
if server_pid is not None:
	print('BSSL SERVER: RUNNING')
else:
	print('BSSL SERVER: STOPPED')