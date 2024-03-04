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
    path("cart/<str:value>/<int:qu>",views.cart,name="cart"),
    path("delete/<str:value>",views.delete,name="delete"),
    path("getCart",views.get_cart,name="get_cart")
]
