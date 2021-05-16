import datetime
import os 
import psutil
import time
import random
import string

def genNonce():
	length = 10
	return ''.join(random.choice(string.ascii_letters) for x in range(length))

print('Starting Logger...')

#def pause_until_next_minute():
#	minute = datetime.datetime.now().minute
#	print(f'Waiting until minute: { minute + 1 }')
#	while minute == datetime.datetime.now().minute:
#		time.sleep(0.001)
#	print('Starting...')

#openssl_dir = '/home/pi/openssl'
openssl_dir = os.path.expanduser('~/openssl')

def header():
	line = 'Timestamp,'
	line += 'Timestamp (Seconds),'
	line += 'CPU %,'
	line += 'CPU Frequency,'
	line += 'Virtual Memory %,'
	line += 'Virtual Memory,'
	line += 'Swap Memory %,'
	line += 'Swap Memory,'
	line += 'Disk Usage %,'
	line += 'Disk Usage,'
	return line

def log(file):
	cpu = psutil.cpu_percent()

	if psutil.cpu_freq() is not None: cpu_f = psutil.cpu_freq().current
	else: cpu_f = ''

	v_mem_p = psutil.virtual_memory().percent
	v_mem = psutil.virtual_memory().used
	s_mem_p = psutil.swap_memory().percent
	s_mem = psutil.swap_memory().used
	disk_usage_p = psutil.disk_usage('/').percent
	disk_usage = psutil.disk_usage('/').used

	now = datetime.datetime.now()
	time_end = (now - datetime.datetime(1970, 1, 1)).total_seconds()

	line = f'{now},{time_end},{cpu},{cpu_f},{v_mem_p},{v_mem},{s_mem_p},{s_mem},{disk_usage_p},{disk_usage},'
	file.write(line + '\n')

def run(file):
	count = 0
	try:
		while True:
			count += 1
			log(file)
			if count % 1000 == 0:
				print(f'Logged {count / 100} seconds')
			time.sleep(1)
	except KeyboardInterrupt:
		pass

nonce = genNonce()

fileName = f'fullyAutomatedLogs/LOGGED_CPU_ALL_{nonce}.csv'
file = open(fileName, 'w+')
file.write(header() + '\n')

run(file)
