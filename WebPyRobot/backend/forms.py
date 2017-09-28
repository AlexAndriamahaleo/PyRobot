from django import forms


class SignUpForm (forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'class':'validate'}))
    username = forms.CharField(label='Pseudo', required=True, widget=forms.TextInput(attrs={'class':'validate'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

class ChangeDataForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, disabled=True, widget=forms.TextInput(attrs={'class':'validate'}))
    username = forms.CharField(label='Pseudo', required=True, disabled=True, widget=forms.TextInput(attrs={'class':'validate'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

class CodeForm (forms.Form):
    ia = forms.CharField(label='ia')
