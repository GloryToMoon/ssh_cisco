import paramiko
import time
import random
import os
import sys

def get_login():
	file = open('addresses.txt' ,'r')
	addresses = file.read().split('\n')
	addresses.pop()
	file.close()
	password=False
	if os.path.exists('password.txt'):
		file=open('password.txt', 'r')
		password=file.read().split('\n')[0]
		file.close()
	return [addresses, password]

def ssh_change_pass(host, secret, newpass):
	client =paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=host,username='admin', password=secret, port=22 )

	chan = client.invoke_shell()
	time.sleep(1)
	chan.send('conf t\n no username admin priv 15\n username admin priv 15 secret ' + newpass  + '\n wr \n')
	time.sleep(3)
	client.close()

def gen_pass():
	alphabet=('1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*QWERTYUIOPASDFGHJKLZXCVBNM')
	len=random.randint(12,16)
	password=""
	for i in range(0, len):
		password+=alphabet[random.randint(0,len(alphabet)-1)]
	return password

if __name__ == '__main__':
	while True:
		check = False
		if check == False and time.strftime('%H') == '8':
			password=gen_pass()
			print password
			login=get_login()
			if login[1] == False:
				sys.exit(1)
				print ('Create a file password.txt, stupid ass')
			hosts=login[0]
			for host in hosts:
				ssh_change_pass(host, login[1], password)
			file=open('password.txt', 'w')
			file.write(password)
			file.close()
			check=True
		elif check == True and time.strftime('%H') != '8':
			check = False
		time.sleep('60')
