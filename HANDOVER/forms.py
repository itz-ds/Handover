from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class UserProfileForm(forms.ModelForm):

    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_pic = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'True', 'value': 'India'}), )

    class Meta:
        model = UserProfile
        fields = [
            'fullname',
            'profile_pic',
            'phone',
            'street1',
            'street2',
            'city',
            'state',
            'zipcode',
            'country',

        ]