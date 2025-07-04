# скрипт для проверки работы ssh сервера
from devices.cli_auth import cli_auth

result, output = cli_auth('localhost', 2222, 'testuser', 'testpassword')
print("Success:", result)
print("Output:", output)

# альтернативный расширенный вариант

print("Script started")
import sys
print("Python version:", sys.version)

import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

import paramiko

def test_ssh_connection():
    print("=== Testing SSH connection ===")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print("Connecting to SSH server...")
        ssh.connect(
            '127.0.0.1',
            port=2224,  # убедись, что порт совпадает с портом сервера
            username='testuser',
            password='testpassword',
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        stdin, stdout, stderr = ssh.exec_command("echo 'Hello SSH!'")
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        print(f"Command output: {output}")
        print(f"Error output: {error}")

        ssh.close()

        if output == "Hello SSH!":
            print("SSH test PASSED")
        else:
            print("SSH test FAILED")

    except Exception as e:
        print(f"SSH Error: {str(e)}")
        print("SSH test FAILED")

# ⬇️ Вызов функции
if __name__ == "__main__":
    test_ssh_connection()