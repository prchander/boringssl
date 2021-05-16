import os 

print('Enter an experiment name:')
print('Examples:')
print('    dil2_drop_exp')
print('    rsa_corrupt_exp')
print()
expName = input(': ')
myCmd = f'sudo tcpdump -i any -w Logs/{expName}.pcap \'port 4433\''
os.system(myCmd)
