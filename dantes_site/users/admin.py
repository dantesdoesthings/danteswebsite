from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserRegistrationForm, UserUpdateForm


class UserAdmin(BaseUserAdmin):
    add_form = UserRegistrationForm
    form = UserUpdateForm
    model = User
    list_display = ('email', 'name', 'is_superuser', 'is_active')
    ordering = ('email',)
    list_filter = ('is_superuser',)
    search_fields = ('email', 'name')


# Register your models here.
admin.site.register(User, UserAdmin)
