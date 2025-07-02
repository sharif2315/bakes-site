from django import forms
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Message")
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, "RECAPTCHA_PUBLIC_KEY", None) and getattr(settings, "RECAPTCHA_PRIVATE_KEY", None):
            self.fields['captcha'] = ReCaptchaField(
                error_messages={
                    'required': 'Please complete the CAPTCHA.',
                    'invalid-input-response': 'CAPTCHA validation failed. Please try again.',
                }
            )