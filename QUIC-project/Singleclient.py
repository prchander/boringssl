import os
import socket

def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	return s.getsockname()[0]

bssl_dir = os.path.expanduser('~/oqs/boringssl/build/tool/bssl')
cert_dir = os.path.expanduser('~/oqs/boringssl/QUIC-project/rsa/key_CA.pem')

print(f'Certificate Directory: {cert_dir}')
n = 1

client_ip = getIP()
print(f'Client IP: {client_ip}')
print(f'Number of samples: ', n)
serverIP = input('Please enter the server IP: ')

myCmd=f'{bssl_dir} client -connect {serverIP}:44330 -root-certs {cert_dir}'


while n>0:
    os.system(myCmd)
    n -= 1