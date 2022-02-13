from django.urls import path
from .views import  AllUsersAPIView, ProjectdetailAPIView, ProjectListAPIView, CompanyListAPIView, EmployeeListAPIView, CompanydetailAPIView, EmployeeDetailView
# , TaskDetail, TaskList,  
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

app_name = "project"

# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
# ]

urlpatterns = [
    path('users/', AllUsersAPIView.as_view(), name='all users' ),

    path('project/', ProjectListAPIView.as_view(), name='createProjects' ),
    path('project/<int:pk>/', ProjectdetailAPIView.as_view(), name='createProjects' ),
    path('company/', CompanyListAPIView.as_view(), name='company'),  
    path('company/<int:pk>/', CompanydetailAPIView.as_view(), name='createProjects' ),
 
    path('employees/', EmployeeListAPIView.as_view(), name='company'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='createProjects' ),

    # path('employees/<int:pk>/add/<int:pk>/', EmployeeListAPIView.as_view(), name='company'), 
    path('schema/', get_schema_view(
        title = "Management Schema",
        description="All APIs ",
        version="1.0.0",

    ), name="api-schema")

]
