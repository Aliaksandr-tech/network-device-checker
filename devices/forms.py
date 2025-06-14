from django import forms

class DeviceSearchForm(forms.Form):
    model = forms.CharField(
        label='Модель устройства',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, Huawei MA5680T'
        })
    )
