from django.shortcuts import render, redirect
from .models import Device, Documentation, AuthData, Feature
from .forms import DeviceSearchForm
from django.http import Http404

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
    return render(request, 'devices/device_detail.html', {
        'device': device,
        'documentation': documentation,
        'auth_data': auth_data,
        'features': features,
    })
# шаблон для ссылки на методику тестирования
def feature_method_view(request, feature_id):
    try:
        feature = Feature.objects.get(id=feature_id)
    except Feature.DoesNotExist:
        raise Http404("Функция не найдена")
    return render(request, 'devices/feature_method.html', {'feature': feature})