"""pavigator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.usersList),
    path('user/<str:indentifier>', views.specificUser,name="user"),
    path('create/', views.CreateUser,name="create"),
    path('update/<str:identifier>', views.UpdateUser,name="UpdateUser"),
    path('delete/<str:identifier>', views.DeleteUser,name="deleteUser"),
    path('timetable/<str:StopNumber>', views.TimeTable,name="GetTimeTable"),
    path('routing/', views.RouteMapping,name="Route_Mapping"),
]
