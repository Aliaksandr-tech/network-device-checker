print("Script started")
import sys
print("Python version:", sys.version)

import paramiko

def test_ssh_connection():
    print("=== Testing SSH connection ===")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print("Connecting to SSH server...")
        ssh.connect(
            '127.0.0.1',
            port=2222,
            username='testuser',
            password='testpassword',
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        # Используем простую команду вместо интерактивного сеанса
        stdin, stdout, stderr = ssh.exec_command("echo 'Hello SSH!'")
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        print(f"Command output: {output}")
        print(f"Error output: {error}")

        ssh.close()

        if output == "Hello SSH!":
            print("SSH test PASSED")
            return True
        else:
            print("SSH test FAILED")
            return False

    except Exception as e:
        print(f"SSH Error: {str(e)}")
        print("SSH test FAILED")
        return False