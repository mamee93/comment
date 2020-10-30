from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import Profile


class SignUpForm(UserCreationForm):
	
	class Meta:
		model = User
		fields = ['username','email','password1','password2']



class ProfileEditForm(forms.ModelForm):

    class  Meta:
        model = Profile 
        fields = ['user','boi','photo']
        
class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class  Meta:
        model = User
        fields = ['username','first_name','last_name','email']

 


 