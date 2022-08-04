from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser


class UserProfileManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User requires valid email')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.name_counter = self.model.objects.filter(name=name).count()
        user.is_verified = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff =True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Also acts as username for login purposes
    email = models.EmailField(max_length=50, unique=True)
    # Arbitrary name, functions as display name
    name = models.CharField(max_length=100)
    # Counter that allows people with identical names to be distinguished from each other
    name_counter = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
