from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Entrer Mot de Passe',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmer Mot de Passe'
    }))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Le mot de passe ne correspond pas!"
            )
        

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Entrer Prénoms'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Entrer Nom de Famille'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrer Numéro de téléphone'
        self.fields['email'].widget.attrs['placeholder'] = 'Entrer un addresse mail valide'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    