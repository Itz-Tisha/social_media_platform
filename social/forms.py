from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm
from .models import webuser,web_post,followers,comments

# from django.core.exceptions import ValidationError
# from django.contrib.auth.hashers import make_password
# from .models import event

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = UserType
#         fields = ['name', 'email', 'password', 'user_type']

#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         if password and len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         return make_password(password)  

   
class signupform(forms.ModelForm):
    
    class Meta:
        model = webuser
        fields = ("name","email","password","age","ac_type")
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter a password'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter your age'}),
            'ac_type': forms.Select(attrs={'placeholder': 'Select account type'})
        }

class loginform(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your username'}),
        label="name"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your password'}),
        label="password"
    )

class postform(forms.ModelForm):
    class Meta:
        model = web_post
        fields = ('desc','post_image')
 
 
class follow_r(forms.ModelForm):
    
    class Meta:
        model = followers
        fields = ("webuser1Id","webuser1Id")

class commentform(forms.ModelForm):
    class Meta:
        model = comments
        fields = ("comment",)
        
class edit_profileform(forms.ModelForm):
    class Meta:
        model=webuser
        fields=("name","email","password","age","ac_type","image")
        widgets = {
             'image': forms.FileInput(attrs={'class': 'form-control'})
        }