from django.contrib.auth import forms as auth_forms

# class LoginForm(auth_forms.AuthenticationForm):
#     def __init__(self, *args, **kw):
#         super().__init__(*args, **kw)
#         for field in self.fields.values():
#             field.widget.attrs['placeholder'] = field.label


from django import forms
from .models import User  # Userを追加
from django.contrib.auth.forms import UserCreationForm # この行を追加

class LoginForm(auth_forms.AuthenticationForm):
    #追加した
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label





class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

