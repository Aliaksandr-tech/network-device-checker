from django.shortcuts import render, redirect
from .forms import DeviceSearchForm
from devices.models import Device

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

