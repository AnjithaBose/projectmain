from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .functions import *
from .models import *
from .forms import *
import time
import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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
            message = CheckAccount(username)
            msg = message
            return render(request,'common/login.html',{'msg':msg})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class PasswordChangeView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated: 
            form = PasswordChangeForm(user=user)
            try:
                staff = Staff.objects.get(user=user)
                notify = Notifications(staff)
                count = CountNotifications(notify)
                return render(request,'common/password_change.html',{'staff':staff,'notify':notify,'count':count,'form':form})
            except:
                student = Student.objects.get(user=user)
                notify = StudentNotifications(student)
                count = CountNotifications(notify)
                return render(request,'common/password_change.html',{'student':student,'notify':notify,'count':count,'form':form})
        else:
            return redirect('logout')  

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                msg="Password Updated successfully"
                try:
                    staff = Staff.objects.get(user=user)
                    notify = Notifications(staff)
                    count = CountNotifications(notify)
                    context={'staff':staff,'msg':msg,'notify':notify,'count':count}
                except:
                    student = Student.objects.get(user=user)
                    notify = StudentNotifications(student)
                    count = CountNotifications(notify)
                    context={'student':student,'msg':msg,'notify':notify,'count':count}
                finally:
                    return render(request,'messages/common/home.html',context)
                    
            else:
                # alert="Password Updation failed. Please try again after some time."
                try:
                    staff = Staff.objects.get(user=user)
                    notify = Notifications(staff)
                    count = CountNotifications(notify)
                    context ={'count':count,'notify':notify,'staff':staff,'form':form}
                except:
                    student = Student.objects.get(user=user)
                    notify = StudentNotifications(student)
                    count = CountNotifications(notify)
                    context={'student':student,'form':form,'notify':notify,'count':count}
                finally:
                    return render(request,'common/password_change.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    


class Home(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                s = Staff.objects.get(user=user)
                if s.stype == '1' or s.stype == '5':
                    return redirect('operations_dashboard')
                elif s.stype == '2' or s.stype == '6' :
                    return redirect('sales_dashboard')
                elif s.stype == '3' :
                    return redirect('trainer_dashboard')
                elif s.stype == '4' :
                    return redirect('admin_dashboard')
                elif s.stype == '7':
                    return redirect('trainer_manager_dashboard')
                else:
                    return redirect('logout')
            except:
                try:
                    s =Student.objects.get(user=user)
                    return redirect('student_dashboard')
                except:
                    return redirect('logout')
        else:
            return redirect('logout')

class MarkasRead(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                staff = Staff.objects.get(user=request.user)
                notify = Notification.objects.filter(user1=staff)
            except:
                student = Student.objects.get(user=request.user)
                notify = Notification.objects.filter(user2=student)
            finally:
                for i in notify:
                    i.status = 'Read'
                    i.save()
            return HttpResponse(status = 200)
         




class AdminDashboard(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True: 
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            current_batches = CurrentBatches().count()
            upcoming_batches = UpcomingBatches().count()
            active_leads = ActiveLeads().count()
            closed_leads = ClosedLeads()
            st = CurrentActiveStudents()
            pending_lms = Lead.objects.filter(approval='2').count()
            c3 = MonthlyRevenue()
            webinar = UpcomingWebinar().count()
            trainers = Staff.objects.filter(stype='3').order_by('doj')
            leads = Lead.objects.filter(Q(status='New')|Q(status='In Pipeline'))
            context={'webinar':webinar,'count':count,'notify':notify,'staff':staff,'current_batches':current_batches,'upcoming_batches':upcoming_batches,'active_leads':active_leads,'closed_leads':closed_leads,'students':st,'pending_lms':pending_lms,'monthly_fee_collected':c3,'trainers':trainers,'leads':leads}
            # print(today.strftime('%b'))
            return render(request,'admin/dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ViewCourses(View):
    def get(self, request):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            course = Course.objects.all()
            page = Pagination(request,course,5)
            form = CourseCreateForm()
            context={'count':count,'notify':notify,'staff':staff,'course': page,'form':form}
            return render(request,'admin/courses.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            course = Course.objects.all()
            form = CourseCreateForm(request.POST,request.FILES)
            if form.is_valid:
                form.save()
                msg = 'Course created successfully'
                context={'count':count,'notify':notify,'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'messages/admin/courses.html',context)
            else:
                alert = 'Course creation failed'
                context={'count':count,'notify':notify,'staff':staff,'course': course,'form':form,'alert':alert}
                return render(request,'messages/admin/courses.html',context)  
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class EditCourse(View):
    def get(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            course = Course.objects.get(id=id)
            form = CourseCreateForm(instance=course)
            context={'count':count,'notify':notify,'staff':staff,'course': course,'form':form}
            return render(request,'admin/edit_course.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
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
                context={'count':count,'notify':notify,'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'messages/admin/courses.html',context)
            else:
                msg = 'Course editing failed.Please review again.'
                context={'count':count,'notify':notify,'staff':staff,'course': course,'form':form,'msg':msg}
                return render(request,'admin/edit_course.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class DeleteCourse(View):
    def get(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            course = Course.objects.get(id=id)
            confirm = "Are you sure you want to delete?.Once clicked on OK changes cant be reverted."
            context={'count':count,'notify':notify,'staff':staff,'course': course,'confirm':confirm}
            return render(request,'messages/admin/courses.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x= AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            course = Course.objects.get(id=id)
            course.delete()
            msg = 'Course deleted successfully!'
            context={'count':count,'notify':notify,'staff':staff,'course': course,'msg':msg}
            return render(request,'messages/admin/courses.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ViewBatches(View):
    def get(self, request):
        x = MainOperationTrainers(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            wdbatch = Batch.objects.filter(type="Weekday",approval='1').order_by('status')
            for i in wdbatch:
                i = BatchStrength(request,i.id)
            webatch = Batch.objects.filter(type="Weekend",approval='1').order_by('status')
            for i in wdbatch:
                i = BatchStrength(request,i.id)
            page = Pagination(request,wdbatch,5)
            pages = Pagination(request,webatch,5)
            form = BatchCreateForm()
            context={'count':count,'notify':notify,'staff':staff,'wdbatch': page,'webatch': pages,'form':form}
            return render(request,'operations/batches.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = BatchCreateForm(request.POST)
            if form.is_valid():
                f=form.save(commit=False)
                code = str(time.time())
                uniquecode = Uniquecode(request,f.subject.code,code)
                f.batch_code = uniquecode
                if staff.stype == '4' or staff.stype== '5':
                    f.approval = '1'
                    f.to_be_approved_by = staff
                    msg = 'Batch added successfully'
                else:
                    f.approval = '2'
                    f.to_be_approved_by = Manager(staff)
                    msg = 'Batch added successfully and has been sent for approval'
                f.save()
                temp = CopyBatch(request,f)
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert = 'Batch creation failed!.Please review your edit.'
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/operations/batches.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewBatch(View):
    def get(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = BatchStrength(request,id)
            scd = StudentCourseData.objects.filter(batch=batch)
            form = SendMailForm()
            context={'count':count,'notify':notify,'staff':staff,'batch': batch,'scd':scd,'form':form}
            return render(request,'operations/batch.html',context)
        else:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '7' or staff.stype == '3':
                batch = BatchStrength(request,id)
                scd = StudentCourseData.objects.filter(batch=batch)
                context={'count':count,'notify':notify,'staff':staff,'batch': batch,'scd':scd}
                return render(request,'operations/batch.html',context)
            else:
                if request.user.is_authenticated:
                    return render(request,'messages/common/permission_error.html')
                else:
                    return redirect('home')
            



class EditBatch(View):
    def get(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = Batch.objects.get(id=id)
            form = BatchCreateForm(instance=batch)
            context={'count':count,'notify':notify,'staff':staff,'batch': batch,'form':form}
            return render(request,'operations/edit_batch.html',context)
        else:
            try:
                staff = Staff.objects.get(user=request.user)
                notify = Notifications(staff)
                count = CountNotifications(notify)
                if staff.stype == '7' or staff.stype == '3':
                    batch = Batch.objects.get(id=id)
                    form = BatchCreateForm(instance=batch)
                    context={'count':count,'notify':notify,'staff':staff,'batch': batch,'form':form}
                    return render(request,'operations/edit_batch.html',context)
                else:
                    if request.user.is_authenticated:
                        return render(request,'messages/common/permission_error.html')
                    else:
                        return redirect('home')
            except:
                if request.user.is_authenticated:
                    return render(request,'messages/common/permission_error.html')
                else:
                    return redirect('home')

    def post(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = Batch.objects.get(id=id)
            trainer = batch.trainer
            link = batch.link
            passcode = batch.passcode
            form = BatchCreateForm(request.POST,instance=batch)
            if form.is_valid():
                f = form.save(commit=False)
                if staff.stype == '5':
                    f.trainer = trainer
                    f.link = link
                    f.passcode = passcode
                f.last_edit_time = datetime.datetime.now()
                f.last_edit_user = staff 
                if staff.stype == '4' or staff.stype== '5':
                    f.approval = '1'
                    f.to_be_approved_by = staff
                    f.save()
                    msg = "Batch edits have been updated"
                else:
                    temp = CopyBatch(request,batch)
                    f.approval = '2'
                    r = Reporting.objects.get(user=staff)
                    f.to_be_approved_by = r.manager
                    f.save()
                    msg = "Batch edits have been noted and send for approval"
                f.save()
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
                return render(request,'messages/operations/batches.html',context)
            else:
                alert="Batch editing failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
                return render(request,'messages/operations/batches.html',context)
        else:
            try:
                staff = Staff.objects.get(user=request.user)
                notify = Notifications(staff)
                count = CountNotifications(notify)
                if staff.stype == '7' or staff.stype == '3':
                    staff = Staff.objects.get(user=request.user)
                    notify = Notifications(staff)
                    count = CountNotifications(notify)
                    batch = Batch.objects.get(id=id)
                    subject = batch.subject
                    start_date = batch.start_date
                    end_date = batch.end_date
                    start_time = batch.start_time
                    end_time = batch.end_time 
                    trainer = batch.trainer
                    link = batch.link
                    passcode = batch.passcode
                    type = batch.type
                    form = BatchCreateForm(request.POST,instance=batch)
                    if form.is_valid():
                        f = form.save(commit=False)
                        f.subject = subject
                        f.start_date = start_date
                        f.end_date = end_date
                        f.start_time = start_time
                        f.end_time = end_time
                        f.type = type 
                        f.last_edit_time = datetime.datetime.now()
                        f.last_edit_user = staff 
                        f.approval = '1'
                        f.to_be_approved_by = staff
                        if staff.stype == '3':
                            f.trainer = trainer
                            f.link = link
                            f.passcode = passcode
                        f.save()
                        msg = "Batch edits have been updated"
                        context={'count':count,'notify':notify,'staff':staff,'msg':msg}
                        return render(request,'messages/operations/batches.html',context)
                    else:
                        alert="Batch editing failed!.Please review your edit."
                        context={'count':count,'notify':notify,'staff':staff,'alert':alert}
                        return render(request,'messages/operations/batches.html',context)
            except:
                if request.user.is_authenticated:
                    return render(request,'messages/common/permission_error.html')
                else:
                    return redirect('home')


class ViewBatchEditApprovals(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4':
                temp = TempBatch.objects.all()
            elif staff.stype == '5':
                temp = TempBatch.objects.filter(to_be_approved_by=staff)
            context={'count':count,'notify':notify,'staff':staff,'temp':temp}
            return render(request,'operations/batch_approvals.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ApproveBatch(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            temp = TempBatch.objects.get(id=id)
            batch = temp.batch
            batch.approval = '1'
            batch.save()
            temp.delete()
            context={'count':count,'notify':notify,'staff':staff}
            return redirect('batch_edit_approvals')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class RejectBatch(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            temp = TempBatch.objects.get(id=id,to_be_approved_by= staff)
            batch = temp.batch
            batch.subject = temp.subject
            batch.batch_code = temp.batch_code
            batch.trainer = temp.trainer
            batch.start_date = temp.start_date
            batch.end_date = temp.end_date
            batch.start_time = temp.start_time
            batch.end_time = temp.end_time
            batch.link = temp.link
            batch.passcode = temp.passcode
            batch.type = temp.type
            batch.status = temp.status
            batch.approval = '1'
            batch.save()
            temp.delete()
            context={'count':count,'notify':notify,'staff':staff}
            return redirect('batch_edit_approvals')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')








class ViewMails(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            draft = Email.objects.filter(status="Draft").order_by('-time_stamp')
            mail = Email.objects.filter(status="Mail").order_by('-time_stamp')
            page = Pagination(request,mail,10)
            context={'count':count,'notify':notify,'staff':staff,'draft':draft,'mail':page}
            return render(request,'admin/view_mails.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class SendMail(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = SendMailForm()
            
            context={'count':count,'notify':notify,'staff':staff,'form':form,}
            return render(request,'admin/send_mail.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
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
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
                f.time_stamp = datetime.datetime.now()
                f.from_address = staff.email
                f.save()
            else:
                alert="Mail send failed!.Please try again."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/admin/view_mails.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class SendMailNotification(View):
    def post(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = SendMailForm(request.POST)
            batch = Batch.objects.get(id=id)
            scd = StudentCourseData.objects.filter(batch=batch)
            to=[]
            for i in scd:
                to.append(i.student.email)
            if form.is_valid():
                f = form.save(commit=False)
                sub = f.subject
                message = f.message
                for i in to:
                    mailsend(request,sub,message,staff.email,i)
                msg = "Notifications send successfully!"
                context={'count':count,'notify':notify,'staff':staff,'msg':msg,'batch':batch}
            else:
                alert = "Notification send failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert,'batch':batch}
            return render(request,'messages/admin/batch.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')
                

class SendDraft(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            draft = Email.objects.get(id=id)
            form = SendMailForm(instance=draft)
            context={'count':count,'notify':notify,'staff':staff,'form':form,'draft':draft}
            return render(request,'admin/send_mail.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ViewMail(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            mail = Email.objects.get(id=id)
            form = SendMailForm(instance=mail)
            context={'count':count,'notify':notify,'staff':staff,'form':form,'mail':mail}
            return render(request,'admin/view_mail.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class DeleteDraft(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            mail = Email.objects.get(id=id)
            mail.delete()
            return redirect('view_mails')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')



class ViewStaff(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            contacts = Staff.objects.filter(~Q(user=request.user),approval=True)
            context={'count':count,'notify':notify,'staff':staff,'contacts':contacts}
            return render(request,'common/contacts.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class PendingStaff(View):
    def get(self, request):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            candidates = Staff.objects.filter(approval=False)
            context={'count':count,'notify':notify,'staff':staff,'candidates':candidates}
            return render(request,'admin/pending_staff.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewPendingStaff(View):
    def get(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            profile = Staff.objects.get(id=id)
            reporting = Reporting.objects.get(user=profile)
            context={'count':count,'notify':notify,'staff':staff,'profile':profile,'reporting':reporting}
            return render(request,'admin/pending_staff_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ApproveStaff(View):
    def get(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            candidate = Staff.objects.get(id=id)
            CheckActive(candidate)
            candidate.approval=True
            candidate.status = 'Active'
            candidate.save()
            return redirect('pending_staff')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')



class Message(View):
    def get(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            chatroom = FindRoom(request,staff,id)
            if chatroom.user1 == staff:
                user = chatroom.user2
            else:
                user = chatroom.user1
            chatmessage = ChatMessage.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendChatMessageForm()
            context={'count':count,'notify':notify,'staff':staff,'chatroom':chatroom,'chatmessage':chatmessage,'form':form,'user':user}
            return render(request,'common/chat2.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            receiver = Staff.objects.get(id=id)
            form = SendChatMessageForm(request.POST)
            if form.is_valid():
                f= form.save(commit=False)
                f.user = staff
                try:
                    chatroom = ChatRoom.objects.get(user1=staff,user2=receiver)
                except:
                    chatroom = ChatRoom.objects.get(user1=receiver,user2=staff)
                f.chatroom = chatroom
                f.timestamp = datetime.datetime.now()
                f.save()
            return redirect('message',id=id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class GetMessage(View):
    def get(self, request,id,cid):
        staff = Staff.objects.get(user=request.user)
        notify = Notifications(staff)
        count = CountNotifications(notify)
        chatroom = ChatRoom.objects.get(id=cid)
        messages = ChatMessage.objects.filter(chatroom=chatroom)
        for i in messages:
            i.username = i.user.name
            i.pic = i.user.profile_pic.url
            i.save()
        return JsonResponse({"messages":list(messages.values()),"staff":str(staff)})
        



class CreateStaff(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = CreateStaffForm()
            context={'count':count,'notify':notify,'staff':staff,'form':form}
            return render(request,'admin/add_staff.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = CreateStaffForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                user = User.objects.create_user(f.email,f.email,f.mobile)
                user.save()
                f.user = user
                y = AdminCheck(request)
                if y == True:
                    f.approval = True
                else:
                    f.approval = False
                    f.status = 'Inctive'
                    user.is_active = False
                    user.save()
                if staff.stype== '5':
                    f.stype == 'Operations'
                elif staff.stype== '6':
                    f.stype == 'Sales'
                elif staff.stype == '7':
                    f.stype == 'Trainer'
                f.save()
                relation = Reporting(user=f,manager=staff)
                relation.save()
                return redirect('view_contacts')
            else:
                return redirect('view_contacts')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


                
class Leads(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4' or staff.stype == '6':
                new = Lead.objects.filter(status="New")
                pipe = Lead.objects.filter(status="In Pipeline")
            else:
                new = Lead.objects.filter(status="New",generator=staff)
                pipe = Lead.objects.filter(status="In Pipeline",generator=staff)
            page = Pagination(request,new,10)
            pages = Pagination(request,pipe,10)
            form = LeadCreateForm()
            context={'count':count,'notify':notify,'staff':staff,'form':form,'new':page,'pipe':pages}
            return render(request,'sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = LeadCreateForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.name = f.name.title()
                f.email = f.email.casefold()
                f.generator = staff
                f.created_on = datetime.datetime.now()
                f.save()
                if f.status == 'Converted':
                    return redirect('convert_lead',id=f.id)
                msg = "Lead added successfully!"
                context = {'staff':staff,'msg':msg}
            else:
                alert = 'Lead adding failed.Please try again.'
                context = {'alert':alert,'staff':staff}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class UpdateLead(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            form = LeadCreateForm(instance = lead)
            context={'count':count,'notify':notify,'staff':staff,'form':form,'lead':lead}
            return render(request,'sales/update_lead.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            form = LeadCreateForm(request.POST,instance = lead)
            if form.is_valid():
                f = form.save(commit=False)
                if f.status == 'Converted':
                    return redirect('convert_lead',id=lead.id)
                msg = "Lead updated successfully."
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert="Lead updation failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewClosure(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4' or staff.stype == '6':
                lead = Lead.objects.filter(status='Converted').order_by('-created_on')
            else:
                lead = Lead.objects.filter(status='Converted',generator=staff).order_by('-created_on')
            page = Pagination(request,lead,10)
            context={'count':count,'notify':notify,'staff':staff,'lead':page}
            return render(request,'sales/closure.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewHistory(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4' or staff.stype == '6':
                lead = Lead.objects.all().order_by('-created_on')
            else:
                lead = Lead.objects.filter(generator=staff).order_by('-created_on')
            page = Pagination(request,lead,10)
            history = True
            context={'count':count,'notify':notify,'staff':staff,'lead':page,'history':history}
            return render(request,'sales/history.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class CreateStudentAccount(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            try:
                student = Student.objects.get(email=lead.email)
                if student:
                    ActivateStudent(student)
                    msg = 'Student account successfully activated'
                    context={'count':count,'notify':notify,'staff':staff,'lead':lead,'msg':msg} 
            except:
                process = "Are you sure you want to proceed?"
                context={'count':count,'notify':notify,'staff':staff,'lead':lead,'process':process}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')
        
    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            try:
                lead.status = "Converted"
                if staff.stype == '4' or staff.stype == '6':
                    StudentAccountCreation(request,lead)
                    msg = "Student account has been created and mails have been sent."
                else:
                    lead.approval = '2'
                    manager = Manager(staff)
                    lead.to_be_approved_by = manager
                    lead.save()
                    msg = "Student account has been created and have been sent for approval."
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            except:
                alert = "Student account creation failed.Please try again"
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ListLMSApprovals(View):
    def get(self, request):
        x = SalesManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4':
                leads = Lead.objects.filter(approval='2',lms=False).order_by('-created_on')
            else:
                leads = Lead.objects.filter(approval='2',lms= False,to_be_approved_by= staff).order_by('-created_on')
            context={'count':count,'notify':notify,'staff':staff,'leads':leads}
            return render(request,'sales/lms_approval.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ApproveLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            return redirect('convert_lead',id=id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')




class DeleteLMSProfile(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            confirm = "Are you sure you want to proceed?"
            context={'count':count,'notify':notify,'staff':staff,'lead':lead,'confirm':confirm}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            try:
                student = Student.objects.get(email=lead.email)
                if staff.stype == '4' or staff.stype== '6':
                    DeleteStudent(student)
                    lead.status = "Lost"
                    lead.approval = '1'
                    lead.save()
                    msg = "Account deleted successfully"
                else:
                    lead.approval = '2'
                    reporting = Reporting.objects.get(user=staff)
                    lead.to_be_approved_by = reporting.manager
                    lead.save()
                    msg = "Account has been marked for deletion and has been sent for approval."
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            except:
                alert = "Account deletion failed.Please try again"
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ListLMSDeletion(View):
    def get(self, request):
        x = SalesManagerCheck(request)
        if x == True:
            user = request.user
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '4':
                lead = Lead.objects.filter(approval='2',lms = True)
            else:
                lead = Lead.objects.filter(approval='2',lms=True,to_be_approved_by = staff)
            context={'count':count,'notify':notify,'staff':staff,'lead':lead}
            return render(request,'sales/lms_deletion.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class ApproveDelLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            return redirect('revert_lead', id=id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class RejectDelLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id = id)
            lead.approval = '1'
            lead.to_be_approved_by = staff
            lead.save()
            return redirect('list_lms_revert')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')





class Students(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            students = Student.objects.all().order_by('-start_date')
            FindSCD(request,students)
            context={'count':count,'notify':notify,'staff':staff,'students':students}
            return render(request,'common/students.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewStudent(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            scd(request,student)
            cd = StudentCourseData.objects.filter(student=student)
            na = StudentCourseData.objects.filter(student=student,batch__status='1')
            context={'count':count,'notify':notify,'staff':staff,'students':student,'cd':cd,'na':na}
            return render(request,'common/student_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class AddSCD(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            scd(request,student)
            form = AddSCDForm()
            context={'count':count,'notify':notify,'staff':staff,'form':form,'student':student}
            return render(request,'operations/add_scd.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            form = AddSCDForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.student = student
                f.save()
                msg = "Successfully added Course Data"
                context={'count':count,'notify':notify,'staff':staff,'student':student,'msg':msg}
            else:
                alert = "Course adding failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert,'student':student}
            return render(request,'messages/operations/student_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class DeleteSCD(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            scd = StudentCourseData.objects.get(id=id)
            student = scd.student
            scd.delete()
            return redirect('view_student',id=student.id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class UpdateShare(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            if student.shared == 'Yes':
                student.shared = 'No'
            elif student.shared == 'No':
                student.shared = 'Yes'
            student.save()
            return redirect('view_students')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class SendSingleMail(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            mail = Email(to_address=student.email)
            form = SendMailForm(instance=mail)
            context = {'staff':staff,'form':form,'mail':mail}
            return render(request,'admin/single_mail.html',context)

    def post (self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            mail = Email(to_address=student.email)
            form = SendMailForm(request.POST,instance=mail)
            if form.is_valid():
                f = form .save(commit=False)
                mailsend(request,f.subject,f.message,staff.email,student.email)
                f.from_address = staff.email
                f.time_stamp = datetime.datetime.now()
                f.status = 'Mail'
                f.save()
                msg = "Mail send successfully"
                context={'count':count,'notify':notify,'staff':staff,'mail':mail,'msg':msg}
            else:
                alert = "Mail send failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert,'mail':mail}
            return render(request,'messages/common/students.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class Jobs(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                staff = Staff.objects.get(user=request.user)
                notify = Notifications(staff)
                count = CountNotifications(notify)
                job = Job.objects.filter(approval="Approved").order_by('-timestamp')
                page = Pagination(request,job,6)
                context = {'staff':staff,'job':page,'notify':notify,'count':count}
            except:
                student= Student.objects.get(user=request.user)
                notify = StudentNotifications(student)
                count = CountNotifications(notify)
                job = Job.objects.filter(approval="Approved").order_by('-timestamp')
                page = Pagination(request,job,6)
                context = {'student':student,'job':page,'notify':notify,'count':count}
            return render(request,'common/jobs.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class AddJob(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddJobForm()
            context = {'staff':staff,'form':form}
            return render(request,'common/add_job.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')
    def post(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddJobForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.timestamp = datetime.datetime.now()
                f.approval = 'Approved'
                f.save()
                msg = 'Job added successfully.'
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert="Job reporting failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/common/jobs.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')
            

class ViewTeqNews(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            posts = Post.objects.all()
            context={'count':count,'notify':notify,'staff':staff,'posts':posts}
            return render(request,'common/blog.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ViewProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            context={'count':count,'notify':notify,'staff':staff}
            return render(request,'common/profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class EditProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = CreateStaffForm(instance=staff)
            context={'count':count,'notify':notify,'staff':staff,'form':form}
            return render(request,'common/edit_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            name = staff.name
            email = staff.email
            empid = staff.empid
            doj = staff.doj
            stype = staff.stype
            form = CreateStaffForm(request.POST,instance=staff)
            if form.is_valid():
                f = form.save(commit=False)
                f.name = name
                f.email = email
                f.empid = empid
                f.doj = doj
                f.stype = stype
                try:
                    pic = request.FILES['pic']
                    f.profile_pic = pic
                    f.save()
                except:
                    f.save()
                msg = "Profile updated successfully"
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert = "Profile updated failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/common/profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class OperationsDashboard(View):
    def get(self, request):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            current_batches = CurrentBatches().count()
            upcoming_batches = UpcomingBatches().count()
            upcoming_webinar = UpcomingWebinar().count()
            pending_task = PendingTask(staff).count()
            staff_members = Managing(staff)
            birthdays = StaffBirthdays()
            active_batches = CurrentBatches()
            coming_batches = UpcomingBatches()
            context ={'coming_batches':coming_batches,'active_batches':active_batches,'staff':staff,'notify':notify,'count':count,'current_batches':current_batches,'upcoming_batches':upcoming_batches,'upcoming_webinar':upcoming_webinar,'pending_task':pending_task,'staff_members':staff_members,'birthdays':birthdays}
            return render(request,'operations/dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class EditStaff(View):
    def get(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            profile = Staff.objects.get(id=id)
            form = CreateStaffForm(instance=profile)
            reporting = Reporting.objects.get(user=profile)
            form_manager = ReportingForm(instance=reporting)
            context={'count':count,'notify':notify,'staff':staff,'form':form,'profile':profile,'form_manager':form_manager}
            return render(request,'admin/edit_staff.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            profile = Staff.objects.get(id=id)
            email = profile.email
            form = CreateStaffForm(request.POST,instance=profile)
            form_manager = ReportingForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.email = email
                if form_manager.is_valid():
                    reporting = Reporting.objects.get(user=profile)
                    reporting.manager = form_manager.cleaned_data['manager']
                    try:
                        reporting.save()
                        f.save()
                        CheckActive(f)
                        msg = "Updated staff account successfully."
                        context ={'staff':staff,'msg':msg,'profile':profile}
                    except:
                        alert="Failed to edit staff account. Please review your edits."
                        context ={'alert':alert,'staff':staff,'profile':profile}
                else:
                    alert="Failed to edit staff account. Please review your edits."
                    context ={'alert':alert,'staff':staff,'profile':profile}
            else:
                alert="Failed to edit staff account. Please review your edits."
                context ={'alert':alert,'staff':staff}
            return render(request,'messages/admin/staff_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class SalesDashboard(View):
    def get(self, request):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            context ={'staff':staff}
            return render(request,'operations/dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class GetStudentPaymentDetails(View):
    def get(self, request,id):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            try:
                spd = StudentPaymentData.objects.get(student=student)
            except:
                spd = StudentPaymentData(student=student,total="0")
                spd.save()
            payments = StudentPayments.objects.filter(spd=spd).order_by('-timestamp')
            feeform = StudentPaymentForm()
            context ={'staff':staff,'student':student,'spd':spd,'payments':payments,'feeform':feeform,'notify':notify,'count':count}
            return render(request,'sales/student_payments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            student = Student.objects.get(id=id)
            spd = StudentPaymentData.objects.get(student=student)
            feeform = StudentPaymentForm(request.POST)
            if feeform.is_valid():
                f = feeform.save(commit=False)
                f.spd = spd
                f.timestamp = datetime.datetime.now()
                f.representative = staff
                f.save()
                msg = "Fee details successfully updated."
                context ={'staff':staff,'msg':msg,'student':student}
            else:
                alert = "Failed to update fee details. Please review your edits."
                context ={'staff':staff,'alert':alert,'student':student}
            return render(request,'messages/common/student_profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class TrainerDashboard(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            current_batches = Batch.objects.filter(status='1',trainer=staff).count()
            upcoming_batches = Batch.objects.filter(status='2',trainer=staff).count()
            active_batches = Batch.objects.filter(status='1',trainer=staff)
            coming_batches = Batch.objects.filter(status='2',trainer=staff)
            pending_task = PendingTask(staff).count()
            pending_queries = ChatRoom.objects.filter(user1=staff,user_1_status='Unread').count()
            context ={'pending_queries':pending_queries,'pending_task':pending_task,'active_batches':active_batches,'coming_batches':coming_batches,'upcoming_batches':upcoming_batches,'current_batches':current_batches,'staff':staff,'notify':notify,'count':count}
            if staff.stype == '4' or staff.stype== '7':
                return redirect('trainer_manager_dashboard')
            else:
                return render(request,'trainer/dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class TrainerManagerDashboard(View):
    def get(self, request):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            current_batches = CurrentBatches().count()
            upcoming_batches = UpcomingBatches().count()
            unallocated_batches = UnallocatedBatches().count()
            pending_task = PendingTask(staff).count()
            active_batches = CurrentBatches()
            coming_batches = UpcomingBatches()
            staff_members = Managing(staff)
            birthdays = StaffBirthdays()
            context ={'birthdays':birthdays,'staff_members':staff_members,'active_batches':active_batches,'coming_batches':coming_batches,'pending_task':pending_task,'unallocated_batches':unallocated_batches,'staff':staff,'notify':notify,'count':count,'upcoming_batches':upcoming_batches,'current_batches':current_batches}
            return render(request,'trainer/manager_dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyBatches(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            wdbatch = Batch.objects.filter(trainer=staff,type="Weekday")
            webatch = Batch.objects.filter(trainer=staff,type="Weekend")
            wdpage = Pagination(request,wdbatch,5)
            wepage = Pagination(request,webatch,5)
            context={'count':count,'notify':notify,'staff':staff,'wdbatch':wdpage,'webatch':wepage}
            return render(request,'trainer/my_batches.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyStudents(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = Batch.objects.filter(trainer=staff)
            name = []
            scd = StudentCourseData.objects.filter(batch__in=batch)
            for i in scd:
                name.append(i.student.name)
            students = Student.objects.filter(name__in=name).order_by('name')
            FindSCD(request,students)
            context={'count':count,'notify':notify,'staff':staff,'students':students}
            return render(request,'trainer/my_students.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyCurrentBatch(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            wdbatch = Batch.objects.filter(trainer=staff,type="Weekday",status='1')
            webatch = Batch.objects.filter(trainer=staff,type="Weekend",status='1')
            context={'count':count,'notify':notify,'staff':staff,'wdbatch':wdbatch,'webatch':webatch}
            return render(request,'trainer/upload_videos.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class UploadVideos(View):
    def get(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = Batch.objects.get(id=id)
            batch_data = BatchData.objects.filter(batch=batch)
            form = AddBatchDataForm()
            time = datetime.datetime.now()
            context={'count':count,'notify':notify,'staff':staff,'batch':batch,'form':form,'batch_data':batch_data,'time':time}
            return render(request,'trainer/videos.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch = Batch.objects.get(id=id)
            form = AddBatchDataForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.batch = batch
                f.date = datetime.datetime.now()
                f.save()
                msg = "Videos uploaded successfully and notifications send."
                context={'count':count,'notify':notify,'staff':staff,'msg':msg,'batch':batch}
            else:
                alert = "Failed to upload video.Please try again."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert,'batch':batch}
            return render(request,'messages/trainer/videos.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class UpdateVideo(View):
    def get(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            video = BatchData.objects.get(id=id)
            batch = Batch.objects.get(id=video.batch.id)
            form = AddBatchDataForm(instance=video)
            context={'count':count,'notify':notify,'staff':staff,'form':form,'video':video,'batch':batch}
            return render(request,'trainer/update_video.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            video = BatchData.objects.get(id=id)
            batch = Batch.objects.get(id=video.batch.id)
            form = AddBatchDataForm(request.POST,instance=video)
            if form.is_valid():
                form.save()
                msg = "Batch data updated successfully."
                context ={'staff':staff,'msg':msg,'batch':batch}
            else:
                alert = "Failed to update batch data.Please review your edits."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert,'batch':batch}
            return render(request,'messages/trainer/videos.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class PlayVideo(View):
    def get(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            batch_data = BatchData.objects.get(id=id)
            batch = Batch.objects.get(id=batch_data.batch.id)
            url = "trainer/upload/videos/"
            context={'count':count,'notify':notify,'staff':staff,'batch_data':batch_data,'batch':batch,'url':url}
            return render(request,'common/video_player.html',context)
        else:
            try:
                student = Student.objects.get(user=request.user)
                if student:
                    notify = StudentNotifications(student)
                    count = CountNotifications(notify)
                    batch_data = BatchData.objects.get(id=id)
                    batch = Batch.objects.get(id=batch_data.batch.id)
                    context={'count':count,'notify':notify,'student':student,'batch_data':batch_data,'batch':batch}
                    return render(request,'common/video_player.html',context)
                else:
                    if request.user.is_authenticated:
                        return render(request,'messages/common/permission_error.html')
                    else:
                        return redirect('home')
            except:
                if request.user.is_authenticated:
                    return render(request,'messages/common/permission_error.html')
                else:
                    return redirect('home')


class SendLeadMail(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            lead = Lead.objects.get(id=id)
            email = Email(to_address=lead.email)
            form = SendMailForm(instance=email)
            context={'count':count,'notify':notify,'staff':staff,'lead':lead,'form':form}
            return render(request,'admin/send_mail.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ActiveWebinar(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            webinar = Webinar.objects.filter(status='Upcoming').order_by('date')
            context={'count':count,'notify':notify,'staff':staff,'webinar':webinar}
            return render(request,'common/webinar.html',context)
        else:
            webinar = Webinar.objects.filter(status='Upcoming').order_by('date')
            context={'webinar':webinar}
            return render(request,'common/public_webinar.html',context)

class AddWebinar(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddWebinarForm()
            context ={'count':count,'notify':notify,'staff':staff,'form':form}
            return render(request,'admin/add_webinar.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddWebinarForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                if f.public_url:
                    pass
                else:
                    code = time.time()
                    url = "%s_%d" % ("TEQ",code)
                    if f.cover_pic:
                        f.public_url = url
                        f.save()
                    else:
                        f.public_url = url
                        temp = DefaultPics.objects.get(id=3)
                        img = Image.open(temp.webinar_cover)
                        draw = ImageDraw.Draw(img)
                        dt = str(f.date)
                        tm = str(f.time)
                        file_name = str("images/webinar_cover/"+f.public_url+".jpg")
                        selectFont = ImageFont.truetype("arialbd.ttf", size = 40)
                        courseFont = ImageFont.truetype("arialbd.ttf", size = 20)
                        codeFont = ImageFont.truetype("arialbd.ttf", size = 20)
                        draw.text( (395,369), f.topic, (255,255,255),anchor="ma",font=selectFont,align ="center")
                        draw.text( (104,501), dt, (255,255,255),anchor="ma",font=courseFont,align ="center")
                        draw.text( (695,501),tm, (255,255,255),anchor="ma",font=codeFont,align ="center")
                        img.save( file_name, "JPEG", resolution=70.0)
                        f.pic = img
                        f.save()
                msg = "Webinar published successfully."
                context = {'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert = "Webinar published failed!.Please review your edit."
                context={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/admin/webinar.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')  

class WebinarRegister(View):
    def get(self, request,id):
        webinar = Webinar.objects.get(public_url=id)
        form = PublicLeadForm()
        context = {'form':form, 'webinar':webinar}
        return render(request,'common/public_register.html',context)

    def post(self, request,id):
        webinar = Webinar.objects.get(public_url=id)
        form = PublicLeadForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.status = 'New'
            subject = "[TEQSTORIES] WEBINAR INVITATION"
            message = "%s_%s_%s" %("Dear participant,\n\nThanks for attending this webinar conducted by Teqstories Solution Pvt.Ltd. Please proceed to the webinar using the following link.\n",webinar.meeting_link,"\n\nWith regards,\nStudent Support Team\nTeqstories")
            from_address = "techsupport@teqstories.com"
            to = f.email
            mailsend(request,subject,message,from_address,to)
            msg = "Meeting link has been sent to your email address."
            context ={'webinar':webinar,'msg':msg}
        else:
            alert= "Error occured.Please review your details."
            context = {'webinar':webinar,'alert':alert}
        return render(request,'messages/common/public_register.html',context)


class StudentDashboard(View):
    def get(self, request):
        x =  StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            enrolled_courses = StudentCourseData.objects.filter(student=student).count()
            active_courses = StudentCourseData.objects.filter(batch__status="1",student=student).count()
            payments = StudentPayments.objects.filter(spd__student=student).count()
            scd = StudentCourseData.objects.filter(student=student)
            batch = []
            trainer = []
            for i in scd:
                batch.append(i.batch.batch_code)
                trainer.append(i.batch.trainer)
            batches = Batch.objects.filter(batch_code__in=batch)
            trainers = Staff.objects.filter(name__in=trainer)
            assignments = Assignment.objects.filter(batch__in=batches).count()
            submitted = StudentAssignmentData.objects.filter(student=student).count()
            pending_assignments = int(assignments)-int(submitted)
            context = {'pending_assignments':pending_assignments,'trainers':trainers,'batches': batches,'student':student,'notify':notify,'count':count,'enrolled_courses':enrolled_courses,'active_courses':active_courses,'payments_done':payments}
            return render(request,'student/dashboard.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class MyClassroom(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            batches = StudentActiveBatches(student)
            context = {'student':student,'batches':batches,'count':count,'notify':notify}
            return render(request,'student/my_classroom.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyRecordings(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            batches = StudentBatches(student)
            context = {'student':student,'batches':batches,'count':count,'notify':notify}
            return render(request,'student/my_recordings.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ClassRecordings(View):
    def get(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            batch = Batch.objects.get(id=id)
            batch_data = BatchData.objects.filter(batch=batch)
            context={'count':count,'notify':notify,'student':student,'batch': batch,'batch_data':batch_data}
            return render(request,'student/class_recordings.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class UploadAssignment(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '7' or staff.stype == '4':
                assignments = Assignment.objects.all().order_by('-date')
            else:
                assignments = Assignment.objects.filter(batch__trainer = staff).order_by('-date')
            form = AddAssignmentForm()
            context ={'count':count,'notify':notify,'staff':staff,'form':form,'assignments':assignments}
            return render(request,'trainer/assignments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddAssignmentForm(request.POST,request.FILES)
            if form.is_valid():
                f = form.save(commit=False)
                if staff.stype == '3':
                    batch = Batch.objects.get(id=f.batch.id)
                    if batch.trainer == staff:
                        pass
                    else:
                        alert = "You are not allowed to add assignments to this batch."
                        context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
                        return render(request,'messages/trainer/assignments.html',context)
        
                f.date = datetime.datetime.now()
                f.save()
                msg = "Assignment added successfully."
                context = {'count':count,'notify':notify,'staff':staff,'msg':msg}
                return render(request,'messages/trainer/assignments.html',context)
            else:
                alert = "Failed to save assignment.Please try again"
                context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
                return render(request,'messages/trainer/assignments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class UploadProject(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            if staff.stype == '7' or staff.stype == '4':
                projects = Project.objects.all().order_by('-date')
            else:
                projects = Project.objects.filter(batch__trainer = staff).order_by('-date')
            form = AddProjectsForm()
            context ={'count':count,'notify':notify,'staff':staff,'form':form,'projects':projects}
            return render(request,'trainer/projects.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddProjectsForm(request.POST,request.FILES)
            if form.is_valid():
                f = form.save(commit=False)
                if staff.stype == '3':
                    batch = Batch.objects.get(id=f.batch.id)
                    if batch.trainer == staff:
                        pass
                    else:
                        alert = "You are not allowed to add assignments to this batch."
                        context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
                        return render(request,'messages/trainer/projects.html',context)
        
                f.date = datetime.datetime.now()
                f.save()
                msg = "Project added successfully."
                context = {'count':count,'notify':notify,'staff':staff,'msg':msg}
                return render(request,'messages/trainer/projects.html',context)
            else:
                alert = "Failed to save project.Please try again"
                context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
                return render(request,'messages/trainer/projects.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')



class ViewAssignments(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            scd = StudentCourseData.objects.filter(student=student)
            batch= []
            for i in scd:
                batch.append(i.batch)
            assignments = Assignment.objects.filter(batch__in=batch)
            context ={'count':count,'notify':notify,'student':student,'assignments': assignments}
            return render(request,'student/assignments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class ViewProjects(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            scd = StudentCourseData.objects.filter(student=student)
            batch= []
            for i in scd:
                batch.append(i.batch)
            projects = Project.objects.filter(batch__in=batch)
            context ={'count':count,'notify':notify,'student':student,'projects': projects}
            return render(request,'student/projects.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

class SubmitAssignment(View):
    def get(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            assignment = Assignment.objects.get(id=id)
            try:
                sad = StudentAssignmentData.objects.filter(assignment=assignment).filter(Q(status='Pending')|Q(status='Approved'))
                if sad:
                    alert="You have alredy submitted this assignment."
                    context={'count':count,'notify':notify,'student':student,'alert':alert,'assignment':assignment}
                    return render(request,'messages/student/assignments.html',context)
                else:
                    pass
            except:
                pass
            submissions = StudentAssignmentData.objects.filter(student=student)
            form = SubmitAssignmentForm()
            context ={'count':count,'student':student,'notify':notify,'form':form,'assignment':assignment,'submissions':submissions}
            return render(request,'student/submit_assignment.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            assignment = Assignment.objects.get(id=id)
            form = SubmitAssignmentForm(request.POST,request.FILES)
            if form.is_valid:
                f = form.save(commit=False)
                if not f.link and not f.attachment:
                    alert = "Please provide a valid link or a valid document"
                    context={'count':count,'notify':notify,'student':student,'alert':alert,'assignment':assignment}
                    return render(request,'messages/student/submit_assignment.html',context)
                else:
                    f.student = student
                    f.assignment = assignment
                    f.submitted_on = datetime.datetime.now()
                    f.status = 'Pending'
                    f.save()
                    msg = "Assignment submitted successfully."
                    context = {'count':count,'notify':notify,'student':student,'msg':msg}
                    return render(request,'messages/student/assignments.html',context)
            else:
                alert = "Failed to submit assignment.Please try again."
                context={'count':count,'notify':notify,'student':student,'alert':alert,'assignment':assignment}
                return render(request,'messages/student/submit_assignment.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class AssignemtSubmissions(View):
     def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            sad = StudentAssignmentData.objects.filter(student=student).order_by('-submitted_on')
            context={'count':count,'notify':notify,'student':student,'sad':sad}
            return render(request,'student/assignment_submissions.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class SubmitProject(View):
    def get(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            project = Project.objects.get(id=id)
            try:
                spd = StudentProjectData.objects.filter(project=project).filter(Q(status='1')|Q(status='2'))
                if spd:
                    alert="You have alredy submitted this project."
                    context={'count':count,'notify':notify,'student':student,'alert':alert,'project':project}
                    return render(request,'messages/student/projects.html',context)
                elif project.active==False:
                    alert="This project has stopped accepting results.Please contact your trainer if you find this as an error."
                    context={'count':count,'notify':notify,'student':student,'alert':alert,'project':project}
                    return render(request,'messages/student/projects.html',context)
                else:
                    pass
            except:
                pass
            form = SubmitProjectForm()
            context ={'count':count,'student':student,'notify':notify,'form':form,'project':project}
            return render(request,'student/submit_project.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            project = Project.objects.get(id=id)
            form = SubmitProjectForm(request.POST,request.FILES)
            if form.is_valid:
                f = form.save(commit=False)
                if not f.link and not f.attachment:
                    alert = "Please provide a valid link or a valid document"
                    context={'count':count,'notify':notify,'student':student,'alert':alert,'project':project}
                    return render(request,'messages/student/submit_project.html',context)
                else:
                    f.student = student
                    f.project = project
                    f.submitted_on = datetime.datetime.now()
                    f.status = '1'
                    f.save()
                    msg = "Project submitted successfully."
                    context = {'count':count,'notify':notify,'student':student,'msg':msg}
                    return render(request,'messages/student/projects.html',context)
            else:
                alert = "Failed to submit project.Please try again."
                context={'count':count,'notify':notify,'student':student,'alert':alert,'project':project}
                return render(request,'messages/student/submit_project.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ProjectSubmissions(View):
     def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            spd = StudentProjectData.objects.filter(student=student).order_by('-submitted_on')
            context={'count':count,'notify':notify,'student':student,'spd':spd}
            return render(request,'student/project_submissions.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class Projects(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            id = id
            if id == '0':
                spd = StudentProjectData.objects.filter(status='1')
                context = {'count':count,'notify':notify,'staff':staff,'spd':spd}
            else:
                project = Project.objects.get(id=id)
                spd = StudentProjectData.objects.filter(project=project)
                context = {'count':count,'notify':notify,'staff':staff,'spd':spd,'project':project}
            return render(request,'trainer/projects_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

class Assignments(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            id = id
            if id == '0':
                sad = StudentAssignmentData.objects.filter(status='Pending')
                context = {'count':count,'notify':notify,'staff':staff,'sad':sad}
            else:
                assignment = Assignment.objects.get(id=id)
                sad = StudentAssignmentData.objects.filter(assignment=assignment)
                context = {'count':count,'notify':notify,'staff':staff,'sad':sad,'assignment':assignment}
            return render(request,'trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

class ApproveAssignment(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            sad = StudentAssignmentData.objects.get(id=id)
            process = "Are you sure you want to approve this assignment?"
            context ={'count':count,'notify':notify,'staff':staff,'sad':sad,'process':process}
            return render(request,'messages/trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            sad = StudentAssignmentData.objects.get(id=id)
            sad.status = '2'
            sad.save()
            type = 6
            message = "Assignment approved by Teqstories"
            SendStudentNotification(type,sad.student,message)
            msg = "Assignment successfully approved and notifications send"
            context ={'count':count,'notify':notify,'staff':staff,'sad':sad,'msg':msg}
            return render(request,'messages/trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class RejectAssignment(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            sad = StudentAssignmentData.objects.get(id=id)
            confirm = "Are you sure you want to reject this assignment?"
            context ={'count':count,'notify':alert,'staff':staff,'sad':sad,'confirm':confirm}
            return render(request,'messages/trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            sad = StudentAssignmentData.objects.get(id=id)
            sad.status = '3'
            sad.save()
            type = 6
            message = "Assignment rejected by Teqstories.Please upload again."
            SendStudentNotification(type,sad.student,message)
            msg = "Assignment successfully rejected."
            context ={'count':count,'notify':notify,'staff':staff,'sad':sad,'msg':msg}
            return render(request,'messages/trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class ApproveProject(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            spd = StudentProjectData.objects.get(id=id)
            process = "Are you sure you want to approve this project and create the certificate?"
            context ={'count':count,'notify':notify,'staff':staff,'spd':spd,'process':process}
            return render(request,'messages/trainer/projects_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            spd = StudentProjectData.objects.get(id=id)
            spd.status = '2'
            spd.save()
            student = spd.student
            scd = StudentCourseData.objects.get(student=student,batch=spd.project.batch)
            CreateCertificate(student,scd)
            type = 6
            message = "Projects approved and certificates released."
            SendStudentNotification(type,student,message)
            msg = "Assignment successfully approved, certificates have been released and notifications send."
            context ={'count':count,'notify':notify,'staff':staff,'spd':spd,'msg':msg}
            return render(request,'messages/trainer/assignments_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 


class RejectProject(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            spd = StudentProjectData.objects.get(id=id)
            confirm = "Are you sure you want to reject this assignment?"
            context ={'count':count,'notify':alert,'staff':staff,'spd':spd,'confirm':confirm}
            return render(request,'messages/trainer/projects_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            spd = StudentProjectData.objects.get(id=id)
            spd.status = '3'
            spd.save()
            type = 6
            message = "Project rejected by Teqstories.Please upload again."
            SendStudentNotification(type,spd.student,message)
            msg = "Assignment successfully rejected and notifications send."
            context ={'count':count,'notify':notify,'staff':staff,'spd':spd,'msg':msg}
            return render(request,'messages/trainer/projects_submitted.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home') 

class MyCertificates(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            scd = StudentCourseData.objects.filter(student=student)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            context = {'count':count,'notify':notify,'student':student,'scd':scd}
            return render(request,'student/my_certificates.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class SendChatNotification(View):
    def get(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            chatroom = ChatRoom.objects.get(id=id)
            type = 1
            if chatroom.user1 == staff:
                msg = "%s-%s" % ("New message from ",str(staff))
                SendNotification(type,chatroom.user2,msg)
            elif chatroom.user2 == staff:
                msg = "%s-%s" % ("New message from ",str(staff))
                SendNotification(type,chatroom.user1,msg)
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 404)

class RemoveAssignment(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            assignment = Assignment.objects.get(id=id)
            confirm = "Are you sure you want to remove this assignment?This may remove all the submitted assignments as well."
            context={'count':count,'notify':notify,'staff':staff,'confirm':confirm}
            return render(request,'messages/trainer/assignments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            assignment = Assignment.objects.get(id=id)
            try:
                assignment.delete()
                msg = "Assignment deleted successfully"
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            except:
                alert = "Failed to delete assignment.Please try again"
                context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/trainer/assignments.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class RemoveProject(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            project = Project.objects.get(id=id)
            confirm = "This will not completly remove the project but will stop accepting new submissions.Are you sure you want to continue?"
            context={'count':count,'notify':notify,'staff':staff,'confirm':confirm}
            return render(request,'messages/trainer/projects.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            project = Project.objects.get(id=id)
            try:
                project.active = False
                project.save()
                msg = "Project deactivated successfully"
                context={'count':count,'notify':notify,'staff':staff,'msg':msg}
            except:
                alert = "Failed to delactivate project.Please try again"
                context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/trainer/projects.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ActivateProject(View):
    def get(self, request,id):
        x = TrainerManagerCheck(request)
        if x == True:
            project = Project.objects.get(id=id)
            project.active =True
            project.save()
            return redirect('upload_projects')
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class AskQuery(View):
    def get(self, request,id):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            chatroom = FindQueryRoom(request,id)
            chatmessage = ChatQuery.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendQueryMessageForm()
            context={'count':count,'notify':notify,'student':student,'chatroom':chatroom,'chatmessage':chatmessage,'form':form}
            return render(request,'student/ask_query.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = StudentCheck(request)
        if x == True:
            form = SendQueryMessageForm(request.POST,request.FILES)
            chatroom = FindQueryRoom(request,id)
            if form.is_valid():
                f = form.save(commit=False)
                f.chatroom = chatroom
                f.user = request.user
                f.date = datetime.datetime.today()
                f.time = datetime.datetime.now()
                f.timestamp = datetime.datetime.now()
                chatroom.user_1_status = 'Unread'
                chatroom.student_status = 'Read' 
                f.save()
                chatroom.timestamp = datetime.datetime.now()
                chatroom.save()
                return redirect('ask_queries',id=id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyTrainers(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            scd = StudentCourseData.objects.filter(student=student)
            trainer = []
            for i in scd:
                trainer.append(i.batch.trainer)
            trainers = Staff.objects.filter(name__in=trainer)
            context={'count':count,'notify':notify,'student':student,'trainers':trainers}
            return render(request,'student/my_trainers.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class MyProfile(View):
    def get(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            form = EditProfileForm(instance=student)
            scd = StudentCourseData.objects.filter(student=student)
            context={'scd':scd,'count':count,'notify':notify,'student':student,'form':form}
            return render(request,'student/profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


    def post(self, request):
        x = StudentCheck(request)
        if x == True:
            student = Student.objects.get(user=request.user)
            name = student.name
            email = student.email
            status = student.status
            start_date = student.start_date
            notify = StudentNotifications(student)
            count = CountNotifications(notify)
            form = EditProfileForm(request.POST,request.FILES,instance=student)
            if form.is_valid():
                f = form.save(commit=False)
                try:
                    pic = request.FILES['pic']
                    f.profile_pic = pic
                    f.save()
                except:
                    f.save()
                msg = "Profile updated successfully."
                context = {'count':count,'notify':notify,'student':student,'msg':msg}
            else:
                alert = "Failed to update profile.Please try again!"
                context={'count':count,'notify':notify,'student':student,'alert':alert}
            return render(request,'messages/student/profile.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')


class Poke(View):
    def get(self, request,id):
        user = request.user
        if user.is_authenticated:
            try:
                student = Student.objects.get(user=user)
                chatroom = ChatRoom.objects.get(id=id)
                if chatroom.student == student:
                    chatroom.user_1_status = 'Unread'
                    chatroom.student_status = 'Read'
                    chatroom.timestamp = datetime.datetime.now()
                    chatroom.save()
                    staff = chatroom.user1
                    type = 4
                    msg = "%s-%s" % ("New query from ",str(student.name))
                    SendNotification(type,staff,msg)
                    return HttpResponse(status = 200)
                else:
                    return render(request,'messages/common/permission_error.html')
            except:
                staff = Staff.objects.get(user=request.user)
                chatroom = ChatRoom.objects.get(id=id)
                print(chatroom)
                if chatroom.user1 == staff:
                    student = chatroom.student
                    chatroom.user_1_status = 'Read'
                    chatroom.student_status = 'Unread'
                    chatroom.timestamp = datetime.datetime.now()
                    chatroom.save()
                    type = 4
                    msg = "%s-%s" % ("Reply for query from ",str(staff.name))
                    SendStudentNotification(type,student,msg)
                    return HttpResponse(status = 200)
                else:
                    return render(request,'messages/common/permission_error.html')        
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')



class ViewQueries(View):
    def get(self, request):
        x= TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            chatroom = ChatRoom.objects.filter(user1=staff).order_by('-timestamp')
            for i in chatroom:
                student = i.student
                if student:
                    pass
                else:
                    chatroom = chatroom.exclude(i)
            context = {'count':count,'notify':notify,'staff':staff,'chatroom':chatroom}
            return render(request,'trainer/view_queries.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class ReplyQuery(View):
    def get(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            chatroom = ChatRoom.objects.get(id=id)
            chatmessage = ChatQuery.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendQueryMessageForm()
            context = {'chatmessage':chatmessage,'count':count,'notify':notify,'staff':staff,'chatroom':chatroom,'form':form}
            return render(request,'trainer/reply_query.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request,id):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            chatroom = ChatRoom.objects.get(id=id)
            chatmessage = ChatQuery.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendQueryMessageForm(request.POST,request.FILES)
            if form.is_valid:
                f = form.save(commit=False)
                f.chatroom = chatroom
                f.user = request.user
                f.date = datetime.datetime.today()
                f.time = datetime.datetime.now()
                f.timestamp = datetime.datetime.now()
                chatroom.user_1_status = 'Read'
                chatroom.student_status = 'Unread' 
                f.save()
                chatroom.timestamp = datetime.datetime.now()
                chatroom.save()
                return redirect('reply_query',id=id)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

class TaskManager(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddTasksForm()
            if staff.stype == '4':
                task = Task.objects.all()
            else:
                task = Task.objects.filter(assigned_by= staff)
            context ={'count':count,'notify':notify,'staff':staff,'form':form,'task':task}
            return render(request,'admin/assign_task.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            notify = Notifications(staff)
            count = CountNotifications(notify)
            form = AddTasksForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.assigned_by = staff
                f.timestamp = datetime.datetime.now()
                f.status = '0'
                f.save()
                type = 5
                msg = "%s-%s" % ("New task allocated by ",str(staff.name))
                SendNotification(type,f.user,msg)
                msg = "Task added successfully and notifications send."
                context ={'count':count,'notify':notify,'staff':staff,'msg':msg}
            else:
                alert = "Failed to add task.Please try again."
                context ={'count':count,'notify':notify,'staff':staff,'alert':alert}
            return render(request,'messages/admin/task_manager.html',context)
        else:
            if request.user.is_authenticated:
                return render(request,'messages/common/permission_error.html')
            else:
                return redirect('home')




            





            
        

            
            


























            









            






            



            

        

           
























                









        
                




            











            















        



            

            




















            
            

