"""
URL configuration for Assistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from camera_app import views

urlpatterns = [
    path("", views.login, name="login"),  # http://localhost:8000/
    path("user_register/", views.register, name="register"),  # http://localhost:8000/user_register/
    path('camera_app/', include('camera_app.urls')),  # http://localhost:8000/camera_app/

]
