import socket, sys, subprocess
from multiprocessing import Process

def printInput(s):
	while True:
		line = s.recv(1024)
		if line:
			line = line.decode().rstrip()
			if line[:8] == 'terminal':
				try:
					output = subprocess.check_output(line[9:], shell=True)
					s.send(output)
				except:
					print('invalid command!')
			else:
				print(line)
		else:
			print('Connection broken')
			break

if __name__ == "__main__":
	connected = False
	print('python netcat emulator!!')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = input('Enter Host: ')
	port = int(input('Enter Port: '))

	try:
		s.connect((host,port))
		connected = True
	except:
		print('conenction failed')
	if connected:
		print('Connected!')
		proc = Process(target=printInput,args=(s,))
		proc.start()
		print('stdin now reading')
		stdin = sys.stdin
		while True:
			line = sys.stdin.readline()
			if connected and line:
				try:
					s.send((line).encode())
				except:
					print('bye')
					break
			else:
				print('bye')
				break