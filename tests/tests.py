# скрипт для проверки работы ssh сервера
from devices.cli_auth import cli_auth

result, output = cli_auth('localhost', 2222, 'testuser', 'testpassword')
print("Success:", result)
print("Output:", output)