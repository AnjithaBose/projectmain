from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout

from .functions import *
from .models import *
from .forms import *
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
            page = Pagination(request,course,5)
            form = CourseCreateForm()
            context={'staff':staff,'course': page,'form':form}
            return render(request,'admin/courses.html',context)
        else:
            return redirect('home')

    def post(self, request):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.all()
            form = CourseCreateForm(request.POST,request.FILES)
            if form.is_valid:
                form.save()
                msg = 'Course created successfully'
                context={'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'messages/admin/courses.html',context)
            else:
                alert = 'Course creation failed'
                context={'staff':staff,'course': course,'form':form,'alert':alert}
                return render(request,'messages/admin/courses.html',context)  
        else:
            return redirect('home')

class EditCourse(View):
    def get(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.get(id=id)
            form = CourseCreateForm(instance=course)
            context={'staff':staff,'course': course,'form':form}
            return render(request,'admin/edit_course.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.get(id=id)
            form = CourseCreateForm(request.POST,instance=course)
            if form.is_valid():
                c=form.save(commit=False)
                try:
                    pic = request.FILES['avatar']
                    c.pic = pic
                except:
                    c.pic = course.pic
                c.save()
                msg = 'Course edited successfully'
                context={'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'messages/admin/courses.html',context)
            else:
                msg = 'Course editing failed.Please review again.'
                context={'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'admin/edit_course.html',context)
        else:
            return redirect('home')

class DeleteCourse(View):
    def get(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.get(id=id)
            confirm = "Are you sure you want to delete?.Once clicked on OK changes cant be reverted."
            context={'staff':staff,'course': course,'confirm':confirm}
            return render(request,'messages/admin/courses.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            course = Course.objects.get(id=id)
            course.delete()
            msg = 'Course deleted successfully!'
            context={'staff':staff,'course': course,'msg':msg}
            return render(request,'messages/admin/courses.html',context)
        else:
            return redirect('home')


class ViewBatches(View):
    def get(self, request):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = Batch.objects.all()
            page = Pagination(request,batch,5)
            form = BatchCreateForm()
            context={'staff':staff,'batch': page,'form':form}
            return render(request,'operations/batches.html',context)
        else:
            return redirect('home')








            
            

