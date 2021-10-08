from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

from .functions import *
from .models import *
from .forms import *
import time
import datetime
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
            wdbatch = Batch.objects.filter(type="Weekday",approval=True)
            webatch = Batch.objects.filter(type="Weekend",approval=True)
            page = Pagination(request,wdbatch,5)
            pages = Pagination(request,webatch,5)
            form = BatchCreateForm()
            context={'staff':staff,'wdbatch': page,'webatch': pages,'form':form}
            return render(request,'operations/batches.html',context)
        else:
            return redirect('home')

    def post(self, request):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = BatchCreateForm(request.POST)
            if form.is_valid():
                f=form.save(commit=False)
                code = time.time()
                f.batch_code = "%s_%d" % (f.subject.code, code)
                if staff.stype == '4' or staff.stype== '5':
                    f.approval = True
                else:
                    f.approval = False
                f.save()
                msg = 'Batch added successfully'
                context={'staff':staff,'msg':msg}
            else:
                alert = 'Batch creation failed!.Please review your edit.'
                context={'staff':staff,'alert':alert}
            return render(request,'messages/operations/batches.html',context)
        else:
            return redirect('home')

class ViewBatch(View):
    def get(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = Batch.objects.get(id=id)
            context={'staff':staff,'batch': batch}
            return render(request,'operations/batch.html',context)
        else:
            return redirect('home')



class EditBatch(View):
    def get(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = Batch.objects.get(id=id)
            form = BatchCreateForm(instance=batch)
            context={'staff':staff,'batch': batch,'form':form}
            return render(request,'operations/edit_batch.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = Batch.objects.get(id=id)
            form = BatchCreateForm(request.POST,instance=batch)
            if form.is_valid():
                f = form.save(commit=False)
                f.last_edit_time = datetime.datetime.now()
                f.last_edit_user = staff 
                if staff.stype == '4' or staff.stype== '5':
                    f.approval = True
                    f.to_be_approved_by = staff
                    msg = "Batch edites have been updated"
                else:
                    f.approval = False
                    r = Reporting.objects.get(user=staff)
                    f.to_be_approved_by = r.manager
                    msg = "Batch edites have been noted and send for approval"
                f.save()
                context={'staff':staff,'msg':msg}
                return render(request,'messages/operations/batches.html',context)
            else:
                alert="Batch editing failed!.Please review your edit."
                context={'staff':staff,'alert':alert}
                return render(request,'messages/operations/batches.html',context)
        else:
            return redirect('home')


class ViewMails(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            draft = Email.objects.filter(status="Draft").order_by('-time_stamp')
            mail = Email.objects.filter(status="Mail").order_by('-time_stamp')
            page = Pagination(request,mail,10)
            context={'staff':staff,'draft':draft,'mail':page}
            return render(request,'admin/view_mails.html',context)


class SendMail(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = SendMailForm()
            draft = Email.objects.filter(status="Draft")
            mail = Email.objects.filter(status="Mail")
            context={'staff':staff,'form':form,'draft':draft,'mail':mail}
            return render(request,'admin/send_mail.html',context)

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = SendMailForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                if f.to_address :
                    f.status = "Mail"
                    mailsend(request,f.subject,f.message,staff.email,f.to_address)
                    msg ="Mail(s) send successfully."
                else:
                    f.status = "Draft"
                    msg ="Mail successfully saved as draft." 
                context={'staff':staff,'msg':msg}
                f.time_stamp = datetime.datetime.now()
                f.from_address = staff.email
                f.save()
            else:
                alert="Mail send failed!.Please try again."
                context={'staff':staff,'alert':alert}
            return render(request,'messages/admin/view_mails.html',context)
        else:
            return redirect('home')

class SendDraft(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            draft = Email.objects.get(id=id)
            form = SendMailForm(instance=draft)
            context={'staff':staff,'form':form,'draft':draft}
            return render(request,'admin/send_mail.html',context)


class ViewMail(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            mail = Email.objects.get(id=id)
            form = SendMailForm(instance=mail)
            context={'staff':staff,'form':form,'mail':mail}
            return render(request,'admin/view_mail.html',context)

            

            




















            
            

