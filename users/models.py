from django.db import models
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [
        ('APP_ADMIN', 'App Admin'),
        ('COMPANY_ADMIN', 'Company Admin'),
        ('EMPLOYEE', 'Employee'),
    ]

    email = models.EmailField(_('email address'), unique=True, editable=False)
    user_name = models.CharField(max_length=150, unique=True, editable=False)
    start_date = models.DateTimeField(default=timezone.now, editable=False)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=USER_TYPE, editable=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)


    REQUIRED_FIELDS = ['user_name', 'first_name', 'type']
    
    def __str__(self):
        return self.user_name

# class Profile(models.Model):
#     user = models.OneToOneField(NewUser, on_delete=models.CASCADE, default="", related_name='profile')
#     linkedIn = models.TextField(blank=True)
#     github = models.TextField(blank=True)
