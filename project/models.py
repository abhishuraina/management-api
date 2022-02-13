from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings

class Company(models.Model):
    name = models.TextField(unique=True)
    admin = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default="")
    REQUIRED_FIELDS = ['admin']
    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, default="")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, default="", related_name='employee', null=True)

    def __str__(self):
        return self.name.user_name


class Project(models.Model):
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default="", related_name='projects')
    # created_by = models.CharField(max_length=20)

    def __str__(self):
        return self.name

