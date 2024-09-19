from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def validate_password(self, password):
        min_length = 8
        if len(password) < min_length:
            raise ValidationError(
                _("Password must be at least %(min_length)d characters long."),
                code='password_too_short',
                params={'min_length': min_length},
            )
            
    def validate_username(self, username):
        if self.model.objects.filter(username=username).exists():
            raise ValidationError(
                _("Username '%(username)s' is already taken."),
                code='username_taken',
                params={'username': username},
            )

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        #if the is_staff and is_superuser is not included in the fields
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") == False:
            raise ValueError("Superuser has to have is_staff being True")
        
        if extra_fields.get("is_superuser") == False:
            raise ValueError("Superuser has to have is_superuser being True")
     
        self.validate_username(extra_fields.get("username"))  # Validate username
        self.validate_password(password)  # Validate password
        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    #main fields
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    
    #for auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    #for creation details
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email" #auth purposes (unique identifier ni sha)
    REQUIRED_FIELDS = ["username"] #password is already handled (for security reasons daw)
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, default=0)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other')
    birthdate = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    
