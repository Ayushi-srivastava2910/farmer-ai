from django import forms
from .models import Farmer

class FarmerRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Farmer
        fields = ['username','email','phone','location','password']