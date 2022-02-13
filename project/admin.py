from django.contrib import admin
from .models import Company, Employee
from .models import Project

# Register your models here.
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Employee)
