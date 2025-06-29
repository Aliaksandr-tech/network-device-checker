import socket
import paramiko
import threading
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ssh_server")

# Генерация ключа
host_key = paramiko.RSAKey.generate(2048)


class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        logger.info(f"Auth attempt: {username}/{password}")
        if username == "testuser" and password == "testpassword":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"


def handle_connection(client_sock, client_addr):
    try:
        logger.info(f"Handling connection from {client_addr}")

        transport = paramiko.Transport(client_sock)
        transport.add_server_key(host_key)
        transport.set_subsystem_handler("sftp", paramiko.SFTPServer, paramiko.SFTPServer)

        server = SimpleSSHServer()
        try:
            transport.start_server(server=server)
            chan = transport.accept(20)
            if chan is None:
                logger.error("No channel")
                transport.close()
                return

        except paramiko.SSHException as e:
            logger.error(f"SSH negotiation failed: {str(e)}")
            return

        # Wait for auth
        chan = transport.accept(20)
        if chan is None:
            logger.error("No channel")
            transport.close()
            return
        chan.get_pty(term='xterm', width=80, height=24)
        # Send welcome message
        chan.send("\r\nWelcome to SSH Test Server!\r\n")
        chan.send("This is a test server for Django project\r\n\r\n")
        chan.send("Welcome to SSH Test Server!\r\n")
        chan.send("Connection established successfully.\r\n")
        chan.close()

        # Simple command handling
        try:
            while True:
                chan.send("\r\n$ ")
                command = ""
                while not command.endswith("\r"):
                    char = chan.recv(1).decode()
                    if char == "\r":
                        break
                    command += char

                command = command.strip()
                if not command:
                    continue

                logger.info(f"Received command: {command}")

                if command.lower() == "exit":
                    chan.send("Goodbye!\r\n")
                    break

                # Execute command
                chan.send(f"Executing: {command}\r\n")
                chan.send(f"Result: '{command}' executed successfully\r\n")

        except Exception as e:
            logger.error(f"Command handling error: {str(e)}")

        chan.close()
        transport.close()
        logger.info(f"Connection closed for {client_addr}")

    except Exception as e:
        logger.error(f"Connection handler error: {str(e)}")
        try:
            transport.close()
        except:
            pass


def run_server(port=2224):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    sock.listen(5)
    logger.info(f"SSH server started on 127.0.0.1:{port}")

    try:
        while True:
            client_sock, client_addr = sock.accept()
            logger.info(f"New connection from {client_addr[0]}:{client_addr[1]}")
            thread = threading.Thread(
                target=handle_connection,
                args=(client_sock, client_addr),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        sock.close()


if __name__ == "__main__":
    run_server(port=2224)