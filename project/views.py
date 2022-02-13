from asyncio import constants
from audioop import add
from copyreg import constructor

from urllib import request
from django.db import models
from rest_framework.response import Response
from rest_framework import generics, serializers
from .serializers import EmployeeSerializer, ProjectSerializer, CompanySerializer, ProjectSerializer, CompanyAddSerializer
from rest_framework import generics
from rest_framework import status
from users.models import NewUser
from users.serializers import CustomUserSerializer
from rest_framework.views import APIView
import logging
from rest_framework import permissions
from project.models import Project, Company, Employee
import json
from django.forms.models import model_to_dict

class AllUsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):    
        users = NewUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        jsonObj = serializer.data
        return Response(jsonObj, status=status.HTTP_201_CREATED )


# Views to handle Project related actions
class ProjectListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):   
        
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        jsonObj = serializer.data
        return Response(jsonObj, status=status.HTTP_201_CREATED )

    def post(self, request):
        print("post request project", request.user)
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        if user_type != "EMPLOYEE":
            return Response({"error":"Only Employees can add projects"}, status = status.HTTP_400_BAD_REQUEST)

        print("logged in user", final_user)

        addProject = Employee.objects.filter(name = final_user["id"]).values('company', 'id')
        if(not addProject):
            return Response({"error":"user Not registered with a company yet"}, status = status.HTTP_400_BAD_REQUEST)
        print(addProject)
        # addEmp = addEmp.data
        addProject = json.dumps(list(addProject))
        addProject = json.loads(addProject)
        print(addProject[0]["company"])
        companyAdminComp = addProject[0]["company"]
        print("logged in user company, company in which project to be added",(companyAdminComp), (request.data["company"]))
        if(str(companyAdminComp) != request.data["company"]):
            return Response({"error":"Operation not possible"}, status = status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data = request.data)
        if(serializer.is_valid()):
            print("valid")
            instance = serializer.save()
            if instance:
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        return Response({"error":"Bad Request"}, status = status.HTTP_400_BAD_REQUEST)


class ProjectdetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        print("hello",snippet)
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(user_type)
        snippet = self.get_object(pk)
        if(user_type != "EMPLOYEE" ):
            return Response({"error" : "Only users of type Employees can update projects"}, status = status.HTTP_400_BAD_REQUEST)

        addProject = Employee.objects.filter(name = final_user["id"]).values('company', 'id')
        if(not addProject):
            return Response({"error":"user Not registered with a company yet"}, status = status.HTTP_400_BAD_REQUEST)
        print(addProject)
        # addEmp = addEmp.data
        addProject = json.dumps(list(addProject))
        addProject = json.loads(addProject)
        print(addProject[0]["company"])
        companyAdminComp = addProject[0]["company"]
        print("logged in user company, company in which project to be added",(companyAdminComp), (request.data["company"]))
        if(str(companyAdminComp) != request.data["company"]):
            return Response({"error":"Operation not possible"}, status = status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(user_type)
        snippet = self.get_object(pk)
        if(user_type != "EMPLOYEE" ):
            return Response({"error" : "Only users of type Employees admins can update projects"}, status = status.HTTP_400_BAD_REQUEST)

        snippet = self.get_object(pk)
        snippet.delete()
        return Response({"success":"successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class CompanyListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):    
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(final_user)
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        jsonObj = serializer.data
        return Response(jsonObj, status=status.HTTP_201_CREATED )

    def post(delf, request):
        print("post request")
        userserializer = CustomUserSerializer(request.user)
        print(request.data)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(user_type)
        if(user_type == "EMPLOYEE" or user_type == "COMPANY_ADMIN"):
            return Response({"error" : "Only APP ADMINS Of app can add companies"}, status = status.HTTP_400_BAD_REQUEST)
        serializer = CompanyAddSerializer(data = request.data)
        print("here", serializer.is_valid(), serializer)
        if(serializer.is_valid()):
            print("valid")
            instance = serializer.save()
            if instance:
                if user_type == "APP_ADMIN":
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    return Response({"error":"Only APP Admins can add Companies"}, status = status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
# View to delete company
class CompanydetailAPIView(APIView):
    def get_object(self, pk):
            try:
                return Company.objects.get(pk=pk)
            except Company.DoesNotExist:
                raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProjectSerializer(snippet)
        return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(user_type)
        snippet = self.get_object(pk)
        if(user_type != "APP_ADMIN" ):
            return Response({"error" : "Only APP_ADMINS can delete companies"}, status = status.HTTP_400_BAD_REQUEST)

        snippet = self.get_object(pk)
        snippet.delete()
        return Response({"success":"Operation successful"}, status=status.HTTP_204_NO_CONTENT)

    
class EmployeeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # Get list of employees
    def get(self, request):   
        employees = Employee.objects.all()
        print(employees)
        serializer = EmployeeSerializer(employees, many=True)
        jsonObj = serializer.data
        return Response(jsonObj, status=status.HTTP_201_CREATED)
        
    def post(self, request):
        print("post request", request.user)
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(final_user)
        print("hello",request.data["name"])
        addEmp = NewUser.objects.filter(pk = request.data["name"]).values('email', 'company')
        # addEmp = addEmp.data
        addEmp = json.dumps(list(addEmp))
        addEmp = json.loads(addEmp)
        print(addEmp[0]["company"])
        tempCompany = addEmp[0]["company"]
        if(tempCompany != None):
            print("null")
            return Response({"error": "Employee Already Working"}, status = status.HTTP_400_BAD_REQUEST)
      
        serializer = EmployeeSerializer(data = request.data)
        print(serializer, serializer.is_valid())
        if(serializer.is_valid()):
            print("valid")
            instance = serializer.save()
            print(instance)
            if instance and user_type == "COMPANY_ADMIN":
                print("yes")
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                return Response({"error":"Only Company Admins can add employees"}, status = status.HTTP_400_BAD_REQUEST)


        return Response({"error":"bad request"}, status = status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise status.HTTP_400_BAD_REQUEST

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = EmployeeSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(final_user)
        snippet = self.get_object(pk)
        if(user_type != "COMPANY_ADMIN" ):
            return Response({"error" : "Only COMPANY ADMIN CAN remove employees"}, status = status.HTTP_400_BAD_REQUEST)
    
        serializer = EmployeeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        userserializer = CustomUserSerializer(request.user)
        user = userserializer.data
        user = json.dumps(user)
        final_user = json.loads(user) 
        user_type = final_user["type"]
        print(user_type)
        snippet = self.get_object(pk)
        if(user_type != "COMPANY_ADMIN" ):
            return Response({"error" : "Only COMPANY ADMINS can remove people"}, status = status.HTTP_400_BAD_REQUEST)

        snippet = self.get_object(pk)
        snippet.delete()
        return Response({"success":"Operation successful"}, status=status.HTTP_204_NO_CONTENT)
