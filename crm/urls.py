"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('', Home.as_view(),name='home'),


    path('administrator/home/',AdminDashboard.as_view(),name='admin_dashboard'),
    path('administrator/courses/',ViewCourses.as_view(),name='view_courses'),
    path('administrator/course/edit/<id>/',EditCourse.as_view(),name='edit_course'),
    path('administrator/course/delete/<id>/',DeleteCourse.as_view(),name='delete_course'),


    path('operations/batches/',ViewBatches.as_view(),name='view_batches'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
