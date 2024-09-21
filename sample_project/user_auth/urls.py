from django.urls import path
from .views import SignupView, LoginView, SampleHomepageView
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="login/", permanent=False)),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("sample_home/", SampleHomepageView.as_view(), name="sample_home")
]
