from django import forms

class DeviceSearchForm(forms.Form):
    model = forms.CharField(label='Модель устройства', max_length=100)
