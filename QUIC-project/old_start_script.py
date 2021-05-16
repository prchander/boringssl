import threading
import atexit # When the script terminates
import fcntl
import hashlib
import json
import os
import random
import re
import socket
import struct
import sys
import time
import datetime

# Don't run START.py in sudo
# However, tcpdump requires sudo
# So run a sudo command before running python3 START.py

threads = []


def pause_until_next_minute():
	minute = datetime.datetime.now().minute
	print(f'Waiting until minute: { minute + 1 }')
	while minute == datetime.datetime.now().minute:
		time.sleep(0.001)
	print('Starting...')


# Send commands to the Linux terminal
def terminal(cmd):
	return os.popen(cmd).read()

# Run a fuction in parallel to other code
class Task(threading.Thread):
	def __init__(self, sendThreadAsFirstArg, name, function, *args):
		assert isinstance(name, str), 'Argument "name" is not a string'
		assert callable(function), 'Argument "function" is not callable'
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()

		self.setName(name)
		self.function = function
		self.args = args
		self.send_thread = sendThreadAsFirstArg

	def __str__(self):
		return f'Task({self.name})'

	def run(self):
		if self.send_thread: self.function(self, *self.args)
		else: self.function(*self.args)

		self._stop_event.set()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

# Creates a new thread and starts it
def create_task(sendThreadAsFirstArg, name, function, *args):
	if len(threads) >= 200:
		# Remove the first 10 threads if it exceeds 200, to balance it out
		for i in range(10):
			threads[i].stop()
			del threads[i]
	task = Task(sendThreadAsFirstArg, name, function, *args)
	threads.append(task)
	task.start()
	return task

# Remove any threads that are stopped
def purge_stopped_threads():
	active_threads = []
	for thread in threads:
		if not thread.stopped():
			active_threads.append(thread)
	threads = active_threads

# This function is ran when the script is stopped
def on_close():
	global closingApplication
	closingApplication = True
	print('Stopping active threads')
	for thread in threads:
		thread.stop()
	print('Goodbye.')

atexit.register(on_close) # Make on_close() run when the script terminates

client_thread = create_task(False, 'Server', terminal, 'python3 server.py')

create_task(False, 'Combined_Logger_Wireshark', terminal, 'python3 Combined_Logger_Wireshark.py')
create_task(False, 'Combined_Logger', terminal, 'python3 Combined_Logger.py')

time.sleep(5)
create_task(False, 'Client', terminal, 'python3 client.py')

#pause_until_next_minute()

# Wait for all threads to end before ending the main thread
while(True):
	for thread in threads:
		#print(f'    {thread.name}: {not thread.stopped()}')
		if thread.name == 'Client' and thread.stopped():
			print('DONE')
			on_close()
			sys.exit()

	print('Still running!')
	time.sleep(10)