import os 

bssl_dir = os.path.expanduser('~/oqs/boringssl/build/tool/bssl')
cert = os.path.expanduser('~/oqs/boringssl/new_certs')

myCmd=f'{bssl_dir} client -connect 10.0.0.157:44330 -root-certs {cert}/dilithium2/key_CA.pem'
os.system(myCmd)