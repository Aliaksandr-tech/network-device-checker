import socket
import threading
import paramiko
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ssh_server")

host_key = paramiko.RSAKey.generate(2048)

class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.command = None

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

    def check_channel_exec_request(self, channel, command):
        self.command = command.decode('utf-8')
        logger.info(f"Exec command requested: {self.command}")
        return True

def handle_connection(client_sock, client_addr):
    logger.info(f"Handling connection from {client_addr}")
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(host_key)

    server = SimpleSSHServer()
    try:
        transport.start_server(server=server)
    except paramiko.SSHException as e:
        logger.error(f"SSH negotiation failed: {e}")
        transport.close()
        return

    chan = transport.accept(20)
    if chan is None:
        logger.error("No channel")
        transport.close()
        return

    # Ожидаем, пока будет выполнена exec-команда
    while not server.command:
        if not transport.is_active():
            logger.error("Transport inactive before command")
            chan.close()
            transport.close()
            return
        server.event.wait(1)

    command = server.command
    logger.info(f"Executing command: {command}")

    if command == "echo 'Hello SSH!'":
        response = "Hello SSH!\n"
    else:
        response = f"Executing: {command}\nResult: '{command}' executed successfully\n"

    chan.sendall(response.encode())
    chan.send_exit_status(0)
    chan.shutdown_write()
    chan.close()
    transport.close()
    logger.info(f"Connection closed for {client_addr}")

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
