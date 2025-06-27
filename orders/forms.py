# forms.py
from django import forms
from .models import Order, Address, DeliveryDetail


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'town', 'postcode']
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': '154 Cannon Street'}),
            'town': forms.TextInput(attrs={'placeholder': 'London'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'W12 6JE'}),
        }


class DeliveryDetailForm(forms.ModelForm):
    class Meta:
        model = DeliveryDetail
        fields = ['delivery_method', 'requested_delivery_date', 'additional_requirements']
        widgets = {
            'requested_delivery_date': forms.TextInput(attrs={
                'type': 'text',
                'x-ref': 'datePickerInput',
                '@click': 'datePickerOpen=!datePickerOpen',
                'x-model': 'datePickerValue',
                'x-on:keydown.escape': 'datePickerOpen=false',
                'readonly': 'readonly', 

            }),
            'additional_requirements': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Any extra details ...'
            }),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@mail.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '07512345678'}),
        }
