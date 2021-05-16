import os
import socket

print('Server has started.')

def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 1))
	return s.getsockname()[0]

alg = 'Dilithium2'#input("Enter alg for server: ")
lsquic_dir = os.path.expanduser('~/oqs/lsquic')
ip = getIP()
print(f'The server IP is {ip}')

if alg == "Dilithium2":
	myCmd =  f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/Dilithium2/key_crt.pem,{lsquic_dir}/certs/Dilithium2/key_srv.pem -s {ip}:4433 -g -j'
	os.system(myCmd)

if alg == "Dilithium3":
	myCmd = f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/Dilithium3/key_crt.pem,{lsquic_dir}/certs/Dilithium3/key_srv.pem -s {ip}:4433'
	os.system(myCmd)

if alg == "Dilithium4":
	myCmd = f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/Dilithium4/key_crt.pem,{lsquic_dir}/certs/Dilithium4/key_srv.pem -s {ip}:4433'
	os.system(myCmd)
	
if alg =="Falcon512":
	myCmd = f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/falcon512/key_crt.pem,{lsquic_dir}/certs/falcon512/key_srv.pem -s {ip}:4433'
	os.system(myCmd)

if alg == "Falcon1024":
	myCmd = f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/falcon1024/key_crt.pem,{lsquic_dir}/certs/falcon1024/key_srv.pem -s {ip}:4433'
	os.system(myCmd)

if alg == "rsa":
	myCmd = f'{lsquic_dir}/build/bin/./research_server -c www.example.com,{lsquic_dir}/certs/rsa/key_crt.pem,{lsquic_dir}/certs/rsa/key_srv.pem -s {ip}:4433'
	os.system(myCmd)

print('Success')