import os
openssl_dir = os.path.expanduser('~/openssl')

myCmd = f'{openssl_dir}/apps/openssl req -x509 -new -newkey rsa:3072 -keyout /home/pi/openssl/lsquic/rsa/key_CA.key -out /home/pi/openssl/lsquic/rsa/key_CA.pem -pkeyopt rsa_keygen_bits:3072 -nodes -subj "/CN=oqstest CA" -days 365 -config {openssl_dir}/apps/openssl.cnf'
os.system(myCmd)
myCmd = f'{openssl_dir}/apps/openssl genpkey -algorithm rsa -out /home/pi/openssl/lsquic/rsa/key_srv.pem -pkeyopt rsa_keygen_bits:3072'
os.system(myCmd)
myCmd = f'{openssl_dir}/apps/openssl req -new -key /home/pi/openssl/lsquic/rsa/key_srv.pem -out /home/pi/openssl/lsquic/rsa/key_srv.csr -nodes -pkeyopt rsa_keygen_bits:3072 -subj \'/CN=oqstest server\' -config {openssl_dir}/apps/openssl.cnf'
os.system(myCmd)
myCmd = f'{openssl_dir}/apps/openssl x509 -req -in /home/pi/openssl/lsquic/rsa/key_srv.csr -out /home/pi/openssl/lsquic/rsa/key_crt.pem -CA /home/pi/openssl/lsquic/rsa/key_CA.pem -CAkey /home/pi/openssl/lsquic/rsa/key_CA.key -CAcreateserial -days 365'
os.system(myCmd)





