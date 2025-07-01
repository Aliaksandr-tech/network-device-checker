import paramiko


def cli_auth(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            ip,
            port=port,
            username=username,
            password=password,
            timeout=10,
            look_for_keys=False,
            allow_agent=False
        )

        # Используем exec_command вместо интерактивного сеанса
        stdin, stdout, stderr = ssh.exec_command("echo 'SSH connection successful!'")
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        ssh.close()

        if error:
            return False, f"Error output: {error}"
        else:
            return True, f"Command output: {output}"

    except Exception as e:
        return False, f"SSH error: {str(e)}"

