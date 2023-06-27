from django.urls import path 
from . import views


urlpatterns = [
    path('' , views.home , name='dashboard'),
    path('employee' , views.employee , name="employee"),
    path('employee_details/<str:pk>/' , views.employee_details , name="employee_details"),

    path('upload/' , views.upload_file , name="upload"),
    

    path('login/' , views.loginPage , name="loginpage"),
    path('logout/' , views.logoutuser , name='logout'),


    path('userpage/' , views.userPage , name="user_page"),
    path('download/<str:pk>' , views.download_file , name="download_file"),

    path('create_user/' , views.create_user , name="create_user"),
    path('employe_form/<str:pk>' , views.updateUser , name="update_employee"),
    path('delete_employee/<str:pk>' , views.deleteUser , name="delete_employee"),

    path('change_password/' , views.change_password , name="change_password")
]
