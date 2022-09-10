from user_management.models import UserDetail
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User, models 

class UserRegistraionForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Email", widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        email = models.EmailField(unique=True)
        fields = [ 'username','email','password1','password2']

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control', 'required':  True,'autofocus':True}),
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        userCount = User.objects.filter(email=email).count()
        if userCount > 0:
            raise forms.ValidationError('This email has already been taken.')
        return email

class EditUserForm(forms.ModelForm):
    uid = forms.CharField(widget=forms.HiddenInput(attrs={'required': False}))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'name@example.com', 'required': True}))
    class Meta:
        model = User
        fields = ['uid', 'first_name','last_name','email',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        uid = self.cleaned_data.get('uid')
        prevEmail = User.objects.get(id=uid).email
        if email!=prevEmail:
            userCount = User.objects.filter(email=email).count()
            if userCount > 0:
                raise forms.ValidationError('This email has already been taken.')
        return email

class EditUserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['contact_no','address','gender','dob',]

class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password1']
