from django.shortcuts import render, redirect
from django.views import View
from .forms import UserSignupForm, ProfileForm
from .models import User, Profile

class SignupView(View):
    def get(self, request):
        user_form = UserSignupForm()
        profile_form = ProfileForm()
        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserSignupForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password"]
            username = user_form.cleaned_data["username"]
            
            # Create the user using the manager's create_user method
            user = User.objects.create_user(
                email=email,
                password=password,
                username=username  # Ensure you include all required fields
            )
        
            # Save the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            #TODO
            # Redirect to a success page or login
            return redirect('success')  # Replace 'success' with your success URL

        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form})
