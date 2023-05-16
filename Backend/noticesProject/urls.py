"""noticesProject URL Configuration

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
from django.urls import path, re_path
from django.views.generic import TemplateView
from dgunotice import views
from dgunotice.views import LoginView, NoticeR, KeywordCR, KeywordUD

urlpatterns = [
    path('', views.testPage, name="test"),
    path('admin/', admin.site.urls),
    path('makeDB/', views.DBInitial, name="DBInitial"),
    path('login/', LoginView.as_view(), name="Login"),
    path('mainPage/notices/', NoticeR.as_view(), name='NoticeR'),
    path('mainPage/keywords/', KeywordCR.as_view(), name="keywordCR"),
    path('mainPage/keywords/<str:key>/', KeywordUD.as_view(), name="keywordUD"),
]
