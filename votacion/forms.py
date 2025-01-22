from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from votacion.chilean_RUN_utils import run_is_valid, run_clean

class RunLoginForm(AuthenticationForm):
    run = forms.CharField(label="Ingresa RUN", max_length=14)
    run.widget.attrs.update(placeholder="RUN")
    
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.error_messages['invalid_run'] = 'El RUN ingresado no aprueba la verificación.'
        self.error_messages['invalid_login'] = 'RUN y password incorrectos.'
        self.fields['username'].required = False
        self.fields['username'].widget.is_required = False
        self.fields['password'].widget.attrs.update(placeholder="Password")

    def clean(self):
        run = self.cleaned_data.get('run')
        if run_is_valid(run):
            username = run_clean(run)
        else:
            raise self.get_invalid_run_error()
        
        password = self.cleaned_data.get("password")
        if password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def get_invalid_run_error(self):
        return ValidationError(
            self.error_messages["invalid_run"],
            code="invalid_run",
            params={"username": self.username_field.verbose_name},
        )
