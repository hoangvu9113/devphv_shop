from django.forms import Form, CharField, PasswordInput, EmailField, TextInput
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class RegisterForm(Form):
    username=CharField(label='', max_length=30, widget=TextInput(attrs={'class': "form-control", 'placeholder':'Tên Đăng Nhập'}))
    email = EmailField(label='', widget=TextInput(attrs={'class': "form-control", 'placeholder':'Email'}))
    password=CharField(label='', widget=PasswordInput(attrs={'class': "form-control",'placeholder':'Mật khẩu'}))
    confirm_password=CharField(label='', widget=PasswordInput(attrs={'class': "form-control",'placeholder':'Nhập lại mật khẩu'}))
    first_name=CharField(label='', max_length=30, widget=TextInput(attrs={'class': "form-control",'placeholder':'Tên'}))
    last_name=CharField(label='', max_length=30, widget=TextInput(attrs={'class': "form-control",'placeholder':'Họ'}))

    def clean_confirm_password(self):
        if 'password' in self.cleaned_data:
            password=self.cleaned_data['password']
            confirm_password=self.cleaned_data['confirm_password']
            if password==confirm_password and password:
                return confirm_password
        raise ValidationError("Mật khẩu không trùng khớp")

    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
           return username
        raise ValidationError ('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.')
        
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
           return email
        raise ValidationError ('Email đã tồn tại. Vui lòng chọn email khác.')
    
    def save(self):
        User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

class LoginForm(Form):
    username = CharField(label='', max_length=30, widget=TextInput(attrs={'class': "form-control", 'placeholder':'Tên đăng nhập'}))
    password=CharField(label='', widget=PasswordInput(attrs={'class': "form-control", 'placeholder':'Mật khẩu'}))