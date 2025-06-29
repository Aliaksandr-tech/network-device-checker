import requests
from django.shortcuts import render,get_object_or_404, redirect
from .models import Device, Documentation, AuthData, Feature
from .forms import DeviceSearchForm
from django.http import Http404, JsonResponse
from ping3 import ping
from django.views.decorators.http import require_GET
from docs.pdf_parser import extract_auth_data_from_pdf
from .selenium_login import try_web_login
from django.utils import timezone
from .cli_auth import cli_auth



def device_search(request):
    if request.method == 'POST':
        form = DeviceSearchForm(request.POST)
        if form.is_valid():
            model_name = form.cleaned_data['model']
            try:
                device = Device.objects.get(model__iexact=model_name)
                # если устройство найдено, можно показать детали или перенаправить
                return redirect('device_detail', device_id=device.id)
            except Device.DoesNotExist:
                # если нет — предложить добавить
                return render(request, 'devices/device_not_found.html', {'model': model_name})
    else:
        form = DeviceSearchForm()
    return render(request, 'devices/device_search.html', {'form': form})

def device_detail(request, device_id):
    device = Device.objects.get(id=device_id)
    documentation = Documentation.objects.filter(device=device)
    auth_data = AuthData.objects.filter(device=device)
    features = Feature.objects.filter(device=device)

    ping_result = None
    if device.ip_address:
        try:
            response_time = ping(device.ip_address, timeout=2)
            ping_result = response_time is not None
        except Exception:
            ping_result = False

    return render(request, 'devices/device_detail.html', {
        'device': device,
        'documentation': documentation,
        'auth_data': auth_data,
        'features': features,
        'ping_result': ping_result,
    })

@require_GET
def ping_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    result = ping(device.ip_address, timeout=1)
    if result is None:
        status = "Недоступен"
    else:
        status = f"Доступен, время отклика {result*1000:.0f} мс"
    return JsonResponse({'status': status})

def check_web(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    ip = device.ip_address
    port = device.web_port or 80
    url_http = f"http://{ip}:{port}"
    try:
        response = requests.get(url_http, timeout=2)
        return JsonResponse({'status': f"Доступен (код {response.status_code})"})
    except requests.RequestException as e:
        return JsonResponse({'status': f"Недоступен: {str(e)}"})

# def check_cli_access(request):
#     if request.method == 'POST':
#         ip = "localhost"  # Для эмулятора
#         port = 2222
#         username = "admin"
#         password = "12345"
#         success, output = cli_auth(ip, port, username, password)
#         return JsonResponse({'success': success, 'output': output})

from django.http import JsonResponse
from .cli_auth import cli_auth

def cli_auth_view(request):
    if request.method == 'POST':
        try:
            # Для теста используем локальный сервер
            success, output = cli_auth(
                ip='localhost',
                port=2222,
                username='testuser',
                password='testpassword'
            )
            return JsonResponse({'success': success, 'output': output})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

# шаблон для ссылки на методику тестирования
def feature_method_view(request, feature_id):
    try:
        feature = Feature.objects.get(id=feature_id)
    except Feature.DoesNotExist:
        raise Http404("Функция не найдена")
    return render(request, 'devices/feature_method.html', {'feature': feature})


def index(request):
    return render(request, 'index.html')

# парсер PDF:

def extract_auth_view(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    manual = Documentation.objects.filter(device=device, doc_type='manual', status=True).first()

    if manual:
        login, password = extract_auth_data_from_pdf(manual.file_path.path)

        # В любом случае — обновляем или создаём AuthData
        AuthData.objects.update_or_create(
            device=device,
            access_type='web',
            defaults={
                'login': login if login else '',
                'password': password if password else ''
            }
        )
        device.login = login or ''
        device.password = password or ''

        device.save()

    return redirect('device_detail', device_id=device.id)




# def web_login_view(request, device_id):
#     device = get_object_or_404(Device, id=device_id)
#     auth = AuthData.objects.filter(device=device, access_type='web').first()
#
#     if not device.ip_address:
#         return JsonResponse({'status': 'Ошибка: нет IP-адреса устройства'})
#
#     port = device.web_port or 80
#
#     if auth and auth.login and auth.password:
#         result = try_web_login(device.ip_address, port, auth.login, auth.password)
#         if result:
#             return JsonResponse({'status': '✅ Успешная авторизация через Web'})
#         else:
#             return JsonResponse({'status': '❌ Авторизация не удалась (возможно, неверный логин/пароль)'})
#     else:
#         url = f"http://{device.ip_address}:{port}"
#         return JsonResponse({'status': f'⚠ Логин и пароль не заданы. Перейдите вручную: {url}', 'redirect': url})

# авторизация

def web_login_view(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    auth = AuthData.objects.filter(device=device, access_type='web').first()

    if not device.ip_address:
        return JsonResponse({'status': 'Ошибка: нет IP-адреса устройства'})

    port = device.web_port or 80

    if auth and auth.login and auth.password:
        result = try_web_login(device.ip_address, port, auth.login, auth.password)
        auth.last_login_status = result
        auth.last_login_checked = timezone.now()
        auth.save()

        if result:
            return JsonResponse({'status': '✅ Успешная авторизация через Web'})
        else:
            return JsonResponse({'status': '❌ Авторизация не удалась (возможно, неверный логин/пароль)'})
    else:
        url = f"http://{device.ip_address}:{port}"
        return JsonResponse({'status': f'⚠ Логин и пароль не заданы. Перейдите вручную: {url}', 'redirect': url})
