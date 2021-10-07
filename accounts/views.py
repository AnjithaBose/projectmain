from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

from .functions import *
from .models import *
# Create your views here.


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('home')
        else:
            msg=""
            return render(request,'common/login.html',{'msg':msg})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg ="Invalid login.Check your credentials!"
            return render(request,'common/login.html',{'msg':msg})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class Home(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                s = Staff.objects.get(user=user)
                if s.stype == '1' :
                    return redirect('operations_dashboard')
                elif s.stype == '2' :
                    return redirect('sales_dashboard')
                elif s.stype == '3' :
                    return redirect('trainer_dashboard')
                elif s.stype == '4' :
                    return redirect('admin_dashboard')
                else:
                    return redirect('logout')
            except:
                try:
                    return redirect('student_dashboard')
                except:
                    return redirect('logout')
        else:
            return redirect('logout')


class AdminDashboard(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True: 
            staff = Staff.objects.get(user=request.user)
            context={'staff':staff}
            return render(request,'admin/dashboard.html',context)
        else:
            return redirect('home')


class ViewCourses(View):
    def get(self, request):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.all()
            context={'staff':staff,'course': course}
            return render(request,'admin/courses.html',context)
        else:
            return redirect('home')
