from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Asset, AssetOwnership


class AssetRegistrationForm(forms.ModelForm):
    class Meta:
        model = AssetOwnership
        fields = ['min_price', 'max_price', 'update_interval_minutes']

    ticker = forms.CharField(max_length=10, required=False)

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']
        return ticker.upper()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
