from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User, Post, Comment, Ticket, TicketReply


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'job']

    password = forms.CharField(max_length=11, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(max_length=11, widget=forms.PasswordInput, label='repeated password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلا ثبت شده است')
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('!این شماره تلفن قبلا وارد شده')
        return phone
    
    def clean_password2(self):
        if self.cleaned_data['password'] !=  self.cleaned_data['password2']:
            raise forms.ValidationError('رمزعبور مطابقت ندارد')
        return self.cleaned_data['password2']
        
    
class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone',
                   'job', 'bio', 'date_of_birth', 'photo']
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('!این شماره تلفن قبلا ثبت شده')
        return phone
    
    def clean_user(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلا ثبت شده است')
        return username
    

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['massage', 'name', 'email', 'phone', 'subject']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن صحیح نمی باشد")
            elif Ticket.objects.exclude(phone=phone).filter(phone=phone).exists():
                raise forms.ValidationError("این شماره تلفن ثبت شده است!")
            else:
                return phone
            

class CustomPassChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "پسورد فعلی"
        self.fields['new_password'].label = "رمز جدید"
        self.fields['new_password2'].label = "تکرار رمز جدید"

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'description', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    
class TicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['text']