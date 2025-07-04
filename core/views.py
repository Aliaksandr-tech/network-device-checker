from django.shortcuts import render, redirect
from .forms import DeviceSearchForm
from devices.models import Device
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def device_search_view(request):
    if request.method == 'POST':
        form = DeviceSearchForm(request.POST)
        if form.is_valid():
            model_name = form.cleaned_data['model']
            try:
                device = Device.objects.get(model=model_name)
                return redirect('device_detail', device_id=device.id)
            except Device.DoesNotExist:
                return render(request, 'core/device_not_found.html', {'model': model_name})
    else:
        form = DeviceSearchForm()
    return render(request, 'core/device_search.html', {'form': form})


@require_GET
def device_autocomplete(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    devices = Device.objects.filter(model__icontains=q).values('id', 'model')[:10]  # максимум 10
    results = [{'id': d['id'], 'model': d['model']} for d in devices]
    return JsonResponse({'results': results})
