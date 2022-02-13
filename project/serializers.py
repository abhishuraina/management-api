from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Project, Company, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    # company = serializers.CharField(max_length=20, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer): 
    # employee = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'company', 'admin')

class CompanySerializer(serializers.ModelSerializer): 
    employee = serializers.StringRelatedField(many=True, read_only=True)
    projects = serializers.StringRelatedField(many=True, read_only=True)
    admin = serializers.CharField(max_length=20, read_only=True)
    class Meta:
        model = Company
        fields = ('id', 'name', 'employee', 'projects', 'admin')

class CompanyAddSerializer(serializers.ModelSerializer): 
    # employee = serializers.StringRelatedField(many=True, read_only=True)
    # projects = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Company
        fields = ('id', 'name', 'admin')
