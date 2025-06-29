import paramiko


def cli_auth(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ip,
            port=port,
            username=username,
            password=password,
            timeout=10,
            look_for_keys=False,  # не искать ключи
            allow_agent=False,  # не использовать SSH-агент
        )

        # Выполняем тестовую команду
        stdin, stdout, stderr = ssh.exec_command('echo "Hello from SSH Server!"')
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        ssh.close()

        if error:
            return False, f"SSH error: {error}"
        return True, output

    except Exception as e:
        return False, f"SSH connection failed: {str(e)}"