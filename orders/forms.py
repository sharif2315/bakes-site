# forms.py
from django import forms
from .models import Order, Address, DeliveryDetail, StoreSettings


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.delivery_method = kwargs.pop('delivery_method', None)
        super().__init__(*args, **kwargs)
        # If pickup, make address fields not required

        if self.delivery_method == 'pickup':
            for field_name in ['street', 'town', 'postcode']:
                self.fields[field_name].required = False        

    def clean(self):
        cleaned_data = super().clean()

        if self.delivery_method == 'pickup':
            # Skip validation errors for address fields
            for field in ['street', 'town', 'postcode']:
                self._errors.pop(field, None)
                cleaned_data[field] = ''
        return cleaned_data
        
    class Meta:
        model = Address
        fields = ['street', 'town', 'postcode']
        widgets = {
            'street': forms.TextInput(attrs={'placeholder': '154 Cannon Street'}),
            'town': forms.TextInput(attrs={'placeholder': 'London'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'W12 6JE'}),
        }
        error_messages = {
            'street': {
                'required': 'Street address is required.',
                'max_length': 'Street address cannot exceed 100 characters.',
            },
            'town': {
                'required': 'Town/City is required.',
                'max_length': 'Town/City cannot exceed 20 characters.',
            },
            'postcode': {
                'required': 'Postcode is required.',
                'max_length': 'Postcode cannot exceed 10 characters.',
            },
        }


class DeliveryDetailForm(forms.ModelForm):
    class Meta:
        model = DeliveryDetail
        fields = ['delivery_method', 'requested_delivery_date', 'additional_requirements']
        widgets = {
            'requested_delivery_date': forms.TextInput(
                attrs={
                    'type': 'text',
                    'x-ref': 'datePickerInput',
                    '@click': 'datePickerOpen=!datePickerOpen',
                    'x-model': 'datePickerValue',
                    'x-on:keydown.escape': 'datePickerOpen=false',
                    'readonly': 'readonly', 
                }
            ),
            'additional_requirements': forms.Textarea(
                attrs={
                    'rows': 2, 
                    'placeholder': 'Any extra details ...'
                }
            ),
        }
        error_messages = {
            'delivery_method': {
                'required': 'Delivery method is required.',
            },
            'requested_delivery_date': {
                'required': 'Requested delivery date is required.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # You can fetch this from cache or DB
        settings = StoreSettings.objects.first()

        choices = []
        if settings.allow_delivery:
            choices.append(('delivery', 'Delivery'))
        if settings.allow_pickup:
            choices.append(('pickup', 'Pickup'))

        self.fields['delivery_method'].choices = choices


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
        error_messages = {
            'first_name': {
                'required': 'First name is required.',
                'max_length': 'First name cannot exceed 30 characters.',
            },
            'last_name': {
                'required': 'Last name is required.',
                'max_length': 'Last name cannot exceed 30 characters.',
            },
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if not email and not phone:
            self.add_error('email', 'Please enter an email or phone.')
            self.add_error('phone', 'Please enter an email or phone.')
            raise forms.ValidationError("Please provide at least an email address or a phone number.")        
