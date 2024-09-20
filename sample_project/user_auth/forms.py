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
            self.add_error("password", "Password must be at least 8 characters")
            raise forms.ValidationError("Password must be at least 8 characters")

        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class ProfileSignupForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "age", "gender", "birthdate"]
    
class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=150, label="Email", widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email:
            self.add_error("email", "Email field must be provided")
            
        if not password:
            self.add_error("password", "Password field must be provided")

        return cleaned_data