import os 

bssl_dir = os.path.expanduser('~/oqs/boringssl/build/tool/bssl')
cert = os.path.expanduser('~/oqs/boringssl/new_certs')

myCmd = f'{bssl_dir} server -cert {cert}/rsa/key_crt.pem -key {cert}/rsa/key_srv.pem -accept 44330'

os.system(myCmd)