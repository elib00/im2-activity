from django.shortcuts import render, redirect
from django.views import View
from .forms import UserSignupForm, ProfileSignupForm, LoginForm
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import get_object_or_404

#use ang model sa project (custom model)
User = get_user_model()

class SignupView(View):
    def get(self, request):
        user_form = UserSignupForm()
        profile_form = ProfileSignupForm()
        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserSignupForm(request.POST)
        profile_form = ProfileSignupForm(request.POST)

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
            return redirect("login")

        return render(request, "signup.html", {"user_form": user_form, "profile_form": profile_form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                request.session["user_id"] = user.id
                return redirect("sample_home")
            else:
                login_form.add_error(None, "Invalid username or password")    

        return render(request, "login.html", {"form": login_form})

class SampleHomepageView(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        user = None
        if user_id:
            user = get_object_or_404(User, id=user_id)
        
        return render(request, "sample_homepage.html", {"user": user})
        
