from django import forms

class SignUpForm(forms.Form):
    name                = forms.CharField(label='Name', max_length=45)
    email               = forms.EmailField(label='Email', max_length=45)
    password            = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=250)
    phone_number        = forms.CharField(label='Phone_number', required=False, max_length=20) 
    is_location_agreed  = forms.BooleanField(label='Is_location_agreeed', required=False)
    is_promotion_agreed = forms.BooleanField(label='Is_promotion_agreed', required=False)

class SignInForm(forms.Form):
    email    = forms.EmailField(label='Email', max_length=45)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=250)
