from django import forms


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
        'disabled': True,
    }), required=True)

    password_again = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password (again)',
        'class': 'form-control',
        'disabled': True,
    }), required=False)


class ChangeSshPublicKeyForm(forms.Form):
    public_key = forms.CharField(max_length=128, widget=forms.Textarea(attrs={
        'placeholder': 'SSH Public Key',
        'class': 'form-control',
        'disabled': True,
    }), required=True)
