from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

def ruttup(r):
    fixed = r
    fixed = fixed.replace('.','').replace(',','').replace(' ','')
    if len(fixed.split('-')) == 2:
        fixed, vd = fixed.split('-')
    else:
        fixed = fixed.replace('-','')
        fixed, vd = fixed[:-1], fixed[-1]
    return fixed, vd

def validating_digit(rut):
    factors = zip(str(rut).zfill(8), '32765432')
    suma = sum([ int(a)*int(b)  for a,b in factors])
    val = (-suma) % 11
    return {10: 'K', 11: '0'}.get(val, str(val))

def rut_is_valid(s):
    is_valid = False
    if s:
        n_str, d_str = ruttup(s)
        try:
            n = int(n_str)
        except ValueError:
            pass
        else:
            if 5*10**5 < n < 47*10**6:
                is_valid = d_str.upper() == validating_digit(n)
    return is_valid

class RutLoginForm(AuthenticationForm):
    rut = forms.CharField(label="Ingresa Rut", max_length=14)
    rut.widget.attrs.update(placeholder="Rut")
    
    
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.error_messages['invalid_rut'] = 'El rut ingresado no aprueba la verificación.'
        self.error_messages['invalid_login'] = 'Rut y password incorrectos.'
        self.fields['username'].required = False
        self.fields['username'].widget.is_required = False
        self.fields['password'].widget.attrs.update(placeholder="Password")

    def clean(self):
        rut = self.cleaned_data.get('rut')
        if rut_is_valid(rut):
            n, d = ruttup(rut)
            username = '-'.join([str(n), d.lower()])
        else:
            raise self.get_invalid_rut_error()
        
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
    
    def get_invalid_rut_error(self):
        return ValidationError(
            self.error_messages["invalid_rut"],
            code="invalid_rut",
            params={"username": self.username_field.verbose_name},
        )
