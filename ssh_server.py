import paramiko
import socket
import threading
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ssh_server")

# Генерируем ключ хоста (RSA 2048 бит)
host_key = paramiko.RSAKey.generate(2048)

class SimpleSSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Проверяем логин и пароль
        if username == "testuser" and password == "testpassword":
            logger.info(f"Successful authentication for {username}")
            return paramiko.AUTH_SUCCESSFUL
        logger.warning(f"Failed authentication for {username}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def run_ssh_server(port=2222):
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(100)
    logger.info(f"SSH server started on port {port}")

    while True:
        client_socket, client_addr = server_socket.accept()
        logger.info(f"Connection from {client_addr}")

        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(host_key)
            server = SimpleSSHServer()
            transport.start_server(server=server)

            # Ожидаем, пока не будет установлен канал
            channel = transport.accept(20)
            if channel is None:
                logger.error("SSH channel negotiation failed.")
                transport.close()
                continue

            # Отправляем приветственное сообщение
            channel.send("Welcome to the test SSH server!\n")
            channel.send("This is a test server for your Django project.\n")

            # Простой интерактивный цикл (опционально)
            while not channel.closed:
                if channel.recv_ready():
                    data = channel.recv(1024).decode('utf-8')
                    if data.strip() == 'exit':
                        channel.close()
                        break
                    # Эхо-ответ
                    channel.send(f"You sent: {data}")

            transport.close()

        except Exception as e:
            logger.error(f"SSH server error: {str(e)}")
            try:
                transport.close()
            except:
                pass

if __name__ == "__main__":
    run_ssh_server(port=2222)