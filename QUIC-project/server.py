import os 

bssl_dir = os.path.expanduser('~/oqs/boringssl/build/tool/bssl')
cert = os.path.expanduser('~/oqs/boringssl/new_certs/')

#myCmd = f'{bssl_dir} server -cert {cert}/dilithium2/key_crt.pem -key {cert}/dilithium2/key_srv.pem -accept 44330'
myCmd = f'{bssl_dir} server -cert {cert}rainbowVclassic/key_crt.pem -key {cert}rainbowVclassic/key_srv.pem -accept 44330'
os.system(myCmd)