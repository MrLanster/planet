"""
URL configuration for miniproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("dash",views.dash,name="dash"),
    path("logout",views.logout,name="logout"),
    path("unverified",views.unverified,name="unverified"),
    path("resend",views.resend,name="resend"),
    path("verify/<str:hash_value>",views.verify,name="verify"),
    path("getCart",views.get_cart,name="get_cart"),
    path("upload",views.upload_image,name="upload_image"),
    path("profile_upload",views.profile_upload,name="profile_upload"),
    path("uploads",views.uploads_json,name="uploads"),
    path("notification",views.notify,name="notify"),
]
