from django.contrib import admin
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False  # Prevent deletion of profile independently
    verbose_name_plural = "Profile"
    fields = ["first_name", "last_name", "age", "gender", "birthdate"]

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'username', 'created_at', 'updated_at')
    search_fields = ('email', 'username')
    ordering = ('-created_at', )
    inlines = [ProfileInline]

admin.site.register(User, UserAdmin)