"""
URL configuration for webapp2025 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from payapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('portfolio_page/')),
    path('admin/', admin.site.urls),
    path('', include('register.urls')),
    path('payments/', include('payapp.urls')),
    path('portfolio_page/', views.portfolio_page, name = 'portfolio_page'),
    path('conversion/<str:from_currency>/<str:to_currency>/<str:amount>/', views.currency_conversion_api, name='currency_conversion_api'),
]
