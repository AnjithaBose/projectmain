from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string

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
                    # return redirect('trainer_dashboard')
                    return HttpResponse("Trainer dashboard")
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
            scd = StudentCourseData.objects.filter(batch=batch)
            form = SendMailForm()
            context={'staff':staff,'batch': batch,'scd':scd,'form':form}
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
                    msg = "Batch edits have been updated"
                else:
                    f.approval = False
                    r = Reporting.objects.get(user=staff)
                    f.to_be_approved_by = r.manager
                    msg = "Batch edits have been noted and send for approval"
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
        else:
            return redirect('home')


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
        else:
            return redirect('home')

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

class SendMailNotification(View):
    def post(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                context={'staff':staff,'msg':msg,'batch':batch}
            else:
                alert = "Notification send failed!.Please review your edit."
                context={'staff':staff,'alert':alert,'batch':batch}
            return render(request,'messages/admin/batch.html',context)
        else:
            return redirect ('home')
                



class SendDraft(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            draft = Email.objects.get(id=id)
            form = SendMailForm(instance=draft)
            context={'staff':staff,'form':form,'draft':draft}
            return render(request,'admin/send_mail.html',context)
        else:
            return redirect('home')


class ViewMail(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            mail = Email.objects.get(id=id)
            form = SendMailForm(instance=mail)
            context={'staff':staff,'form':form,'mail':mail}
            return render(request,'admin/view_mail.html',context)
        else:
            return redirect('home')


class ViewStaff(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            contacts = Staff.objects.filter(~Q(user=request.user))
            # contacts = Staff.objects.all()
            context={'staff':staff,'contacts':contacts}
            return render(request,'common/contacts.html',context)
        else:
            return redirect('home')

class Message(View):
    def get(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            
            receiver = Staff.objects.get(id=id)
            
            try:
                chatroom = ChatRoom.objects.get(user1=staff,user2=receiver)
            except:
                try:
                    chatroom = ChatRoom.objects.get(user1=receiver,user2=staff)
                except:
                    chatroom = ChatRoom(user1 = staff, user2 = receiver)
                    chatroom.save()
            chatmessage = ChatMessage.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendChatMessageForm()
            context={'staff':staff,'chatroom':chatroom,'chatmessage':chatmessage,'form':form}
            return render(request,'common/chat.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
            return redirect('home')


class CreateStaff(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = CreateStaffForm()
            context={'staff':staff,'form':form}
            return render(request,'admin/add_staff.html',context)
        else:
            return redirect('home')

    def post(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                    user.is_active = False
                if staff.stype== '5':
                    f.stype == 'Operations'
                else:
                    f.stype == 'Sales'
                f.save()
                relation = Reporting(user = f , manager = staff)
                relation.save()
                return redirect('view_contacts')
            else:
                return redirect('view_contacts')
        else:
            return redirect('home')
                
class Leads(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            new = Lead.objects.filter(status="New")
            pipe = Lead.objects.filter(status="In Pipeline")
            page = Pagination(request,new,10)
            pages = Pagination(request,pipe,10)
            form = LeadCreateForm()
            context={'staff':staff,'form':form,'new':page,'pipe':pages}
            return render(request,'sales/leads.html',context)
        else:
            return redirect('home')

    def post(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
            return redirect('home')

class UpdateLead(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            form = LeadCreateForm(instance = lead)
            context={'staff':staff,'form':form,'lead':lead}
            return render(request,'sales/update_lead.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            form = LeadCreateForm(request.POST,instance = lead)
            if form.is_valid():
                f = form.save(commit=False)
                if f.status == 'Converted':
                    return redirect('convert_lead',id=lead.id)
                msg = "Lead updated successfully."
                context={'staff':staff,'msg':msg}
            else:
                alert="Lead updation failed!.Please review your edit."
                context={'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            return redirect('home')

class ViewClosure(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.filter(status='Converted').order_by('-created_on')
            page = Pagination(request,lead,10)
            context={'staff':staff,'lead':page}
            return render(request,'sales/closure.html',context)
        else:
            return redirect('home')

class ViewHistory(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.all().order_by('-created_on')
            page = Pagination(request,lead,10)
            history = True
            context={'staff':staff,'lead':page,'history':history}
            return render(request,'sales/history.html',context)
        else:
            return redirect('home')

class CreateStudentAccount(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            process = "Are you sure you want to proceed?"
            context={'staff':staff,'lead':lead,'process':process}
            return render(request,'messages/sales/leads.html',context)
        else:
            return redirect('home')
        
    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            try:
                student = StudentConvert(request,lead)
                lead.status = "Converted"
                lead.save()
                subject="[TEQSTORIES]-ACCOUNT CREATED"
                message =  "Hi Learner, \n\n\nYour account has created with https://lms.teqstories.com. Please login using your email as username and mobile number as password. \n\n\nIf you feel any difficulty please contact our representative or mail us as techsupport@teqstories.com. \n\n\nWith Regards,\nStudent Support Team,\nTeqstories "
                from_address = 'techsupport@teqstories.com'
                to = lead.email
                mailsend(request,subject,message,from_address,to)
                msg = "Student account has been created and mails have been sent."
                context={'staff':staff,'msg':msg}
            except:
                alert = "Student account creation failed.Please try again"
                context={'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            return redirect('home')

class DeleteLMSProfile(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            confirm = "Are you sure you want to proceed?"
            context={'staff':staff,'lead':lead,'confirm':confirm}
            return render(request,'messages/sales/leads.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            try:    
                student = Student.objects.get(email=lead.email)
                lead.status = "In Pipeline"
                lead.save()
                user = User.objects.get(username=student.user)
                student.delete()
                user.delete()
                msg = "Account deleted successfully"
                context={'staff':staff,'msg':msg}
            except:
                alert = "Account deletion failed.Please try again"
                context={'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            return redirect('home')


class Students(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.all().order_by('-start_date')
            context={'staff':staff,'student':student}
            return render(request,'common/students.html',context)
        else:
            return redirect('home')

class ViewStudent(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            scd(request,student)
            cd = StudentCourseData.objects.filter(student=student)
            na = StudentCourseData.objects.filter(student=student,batch__status='1')
            context={'staff':staff,'student':student,'cd':cd,'na':na}
            return render(request,'common/student_profile.html',context)
        else:
            return redirect('home')

class AddSCD(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            scd(request,student)
            form = AddSCDForm()
            context={'staff':staff,'form':form,'student':student}
            return render(request,'operations/add_scd.html',context)
        else:
            return redirect('home')

    def post(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            form = AddSCDForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.student = student
                f.save()
                msg = "Successfully added Course Data"
                context={'staff':staff,'student':student,'msg':msg}
            else:
                alert = "Course adding failed!.Please review your edit."
                context={'staff':staff,'alert':alert,'student':student}
            return render(request,'messages/operations/student_profile.html',context)
        else:
            return redirect('home')

class DeleteSCD(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            scd = StudentCourseData.objects.get(id=id)
            student = scd.student
            scd.delete()
            return redirect('view_student',id=student.id)
        else:
            return redirect('home')

class UpdateShare(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            if student.shared == 'Yes':
                student.shared = 'No'
            elif student.shared == 'No':
                student.shared = 'Yes'
            student.save()
            return redirect('view_students')
        else:
            return redirect('home')

class SendSingleMail(View):
    def get(self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            mail = Email(to_address=student.email)
            form = SendMailForm(instance=mail)
            context = {'staff':staff,'form':form,'mail':mail}
            return render(request,'admin/single_mail.html',context)

    def post (self, request,id):
        x = NotTrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                context={'staff':staff,'mail':mail,'msg':msg}
            else:
                alert = "Mail send failed!.Please review your edit."
                context={'staff':staff,'alert':alert,'mail':mail}
            return render(request,'messages/common/students.html',context)
        else:
            return redirect('home')

class Jobs(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            staff = Staff.objects.get(user=request.user)
            job = Job.objects.filter(approval="Approved").order_by('-timestamp')
            page = Pagination(request,job,6)
            context = {'staff':staff,'job':page}
            return render(request,'common/jobs.html',context)
        else:
            return redirect('home')

class AddJob(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = AddJobForm()
            context = {'staff':staff,'form':form}
            return render(request,'common/add_job.html',context)
        else:
            return redirect('home')
    def post(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = AddJobForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.timestamp = datetime.datetime.now()
                f.approval = 'Approved'
                f.save()
                msg = 'Job added successfully.'
                context={'staff':staff,'msg':msg}
            else:
                alert="Job reporting failed!.Please review your edit."
                context={'staff':staff,'alert':alert}
            return render(request,'messages/common/jobs.html',context)
        else:
            return redirect('home')
            

class ViewTeqNews(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            staff = Staff.objects.get(user=request.user)
            posts = Post.objects.all()
            context={'staff':staff,'posts':posts}
            return render(request,'common/blog.html',context)
        else:
            return redirect('home')

class ViewProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context={'staff':staff}
            return render(request,'common/profile.html',context)
        else:
            return redirect('home')

class EditProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = CreateStaffForm(instance=staff)
            context={'staff':staff,'form':form}
            return render(request,'common/edit_profile.html',context)
        else:
            return redirect('home')

    def post(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                context={'staff':staff,'msg':msg}
            else:
                alert = "Profile updated failed!.Please review your edit."
                context={'staff':staff,'alert':alert}
            return render(request,'messages/common/profile.html',context)
        else:
            return redirect('home')




        
                




            











            















        



            

            




















            
            

