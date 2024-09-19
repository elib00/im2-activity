from django import forms
from .models import User, Profile

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["email", "username", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "age", "gender", "birthdate"]