import paramiko
from django.conf import settings

def cli_auth(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command('display version')  # Пример команды для Huawei
        output = stdout.read().decode()
        ssh.close()
        return True, output
    except Exception as e:
        return False, str(e)