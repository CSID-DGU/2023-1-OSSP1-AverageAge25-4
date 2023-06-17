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
from dgunotice.views import LoginView, SignupView, MainPageView, SearchView, KeywordProcessView, KeywordAddView, verifyEmailView

urlpatterns = [
    path('', views.testPage, name="test"),
    path('admin/', admin.site.urls),
    path('makeDB/', views.DBInitial, name="DBInitial"),
    path('login/', LoginView.as_view(), name="Login"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('mainPage/', MainPageView.as_view(), name='main_page'),
    path('mainPage/reorder/', MainPageView.as_view(), name='main_page_reorder'),
    path('mainPage/add/', KeywordAddView.as_view(), name='add_keyword'),
    path('mainPage/show_similar', MainPageView.as_view(), name='show_similar'),
    path('mainPage/<str:keyword>/', KeywordProcessView.as_view(), name='keyword_process'),
    path('search/', SearchView.as_view(), name='search'),
    path('verify/', verifyEmailView.as_view(), name='verify_email'),
    #path('mainPage/show_similar/', MainPageView.as_view(), name='similar')
    #### 테스트용 크롤링 함수 ####
    path('firstCrawl/', views.crawlInitial, name="crawlInitial")

]
