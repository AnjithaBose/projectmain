from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core import serializers

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
            return render(request,'common/login.html',{'msg':msg})
        else:
            msg = CheckAccount(username)
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
                    # return redirect('student_dashboard')
                    return HttpResponse("Student dashboard")
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
            return render(request,'messages/common/permission_error.html')


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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')


class ViewBatches(View):
    def get(self, request):
        x = MainOperationTrainers(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            wdbatch = Batch.objects.filter(type="Weekday",approval='1').order_by('status')
            for i in wdbatch:
                i = BatchStrength(request,i.id)
            webatch = Batch.objects.filter(type="Weekend",approval='1').order_by('status')
            for i in wdbatch:
                i = BatchStrength(request,i.id)
            page = Pagination(request,wdbatch,5)
            pages = Pagination(request,webatch,5)
            form = BatchCreateForm()
            context={'staff':staff,'wdbatch': page,'webatch': pages,'form':form}
            return render(request,'operations/batches.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
                    f.approval = '1'
                    f.to_be_approved_by = staff
                    msg = 'Batch added successfully'
                else:
                    f.approval = '2'
                    reporting = Reporting.objects.get(user=staff) 
                    f.to_be_approved_by = reporting.manager
                    msg = 'Batch added successfully and has been sent for approval'
                f.save()
                temp = CopyBatch(request,f)
                context={'staff':staff,'msg':msg}
            else:
                alert = 'Batch creation failed!.Please review your edit.'
                context={'staff':staff,'alert':alert}
            return render(request,'messages/operations/batches.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

# class ApprovalBatch(View):
#     def get(self,request):
#         x = ManagerCheck(request)
#         if x == True:
#             staff = Staff.objects.get(user=request.user)
#             batch = Batch.objects.filter()


class ViewBatch(View):
    def get(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = BatchStrength(request,id)
            scd = StudentCourseData.objects.filter(batch=batch)
            form = SendMailForm()
            context={'staff':staff,'batch': batch,'scd':scd,'form':form}
            return render(request,'operations/batch.html',context)
        else:
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '7' or staff.stype == '3':
                batch = BatchStrength(request,id)
                scd = StudentCourseData.objects.filter(batch=batch)
                context={'staff':staff,'batch': batch,'scd':scd}
                return render(request,'operations/batch.html',context)
            else:
                return render(request,'messages/common/permission_error.html')
            



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
            try:
                staff = Staff.objects.get(user=request.user)
                if staff.stype == '7' :
                    batch = Batch.objects.get(id=id)
                    form = BatchCreateForm(instance=batch)
                    context={'staff':staff,'batch': batch,'form':form}
                    return render(request,'operations/edit_batch.html',context)
                else:
                    return render(request,'messages/common/permission_error.html')
            except:
                return render(request,'messages/common/permission_error.html')

    def post(self, request,id):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            batch = Batch.objects.get(id=id)
            form = BatchCreateForm(request.POST,instance=batch)
            if form.is_valid():
                f = form.save(commit=False)
                if staff.stype == '5':
                    f.trainer = batch.trainer
                    f.link = batch.link
                    f.passcode = batch.passcode
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
                context={'staff':staff,'msg':msg}
                return render(request,'messages/operations/batches.html',context)
            else:
                alert="Batch editing failed!.Please review your edit."
                context={'staff':staff,'alert':alert}
                return render(request,'messages/operations/batches.html',context)
        else:
            try:
                staff = Staff.objects.get(user=request.user)
                if staff.stype == '7' :
                    staff = Staff.objects.get(user=request.user)
                    batch = Batch.objects.get(id=id)
                    subject = batch.subject
                    start_date = batch.start_date
                    end_date = batch.end_date
                    start_time = batch.start_time
                    end_time = batch.end_time
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
                        f.save()
                        msg = "Batch edits have been updated"
                        context={'staff':staff,'msg':msg}
                        return render(request,'messages/operations/batches.html',context)
                    else:
                        alert="Batch editing failed!.Please review your edit."
                        context={'staff':staff,'alert':alert}
                        return render(request,'messages/operations/batches.html',context)
            except:
                return render(request,'messages/common/permission_error.html')


class ViewBatchEditApprovals(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            temp = TempBatch.objects.filter(to_be_approved_by=staff)
            context={'staff':staff,'temp':temp}
            return render(request,'operations/batch_approvals.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class ApproveBatch(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            temp = TempBatch.objects.get(id=id,to_be_approved_by= staff)
            batch = temp.batch
            batch.approval = '1'
            batch.save()
            temp.delete()
            context={'staff':staff}
            return redirect('batch_edit_approvals')
        else:
            return render(request,'messages/common/permission_error.html')

class RejectBatch(View):
    def get(self, request,id):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
            context={'staff':staff}
            return redirect('batch_edit_approvals')
        else:
            return render(request,'messages/common/permission_error.html')








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
            return render(request,'messages/common/permission_error.html')


class SendMail(View):
    def get(self, request):
        x = ManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = SendMailForm()
            
            context={'staff':staff,'form':form,}
            return render(request,'admin/send_mail.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')
                



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
            return render(request,'messages/common/permission_error.html')


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
            return render(request,'messages/common/permission_error.html')


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
            return render(request,'messages/common/permission_error.html')

class Message(View):
    def get(self, request,id):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            chatroom = FindRoom(request,staff,id)
            chatmessage = ChatMessage.objects.filter(chatroom=chatroom).order_by('timestamp')
            form = SendChatMessageForm()
            context={'staff':staff,'chatroom':chatroom,'chatmessage':chatmessage,'form':form}
            return render(request,'common/chat.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

class GetMessage(View):
    def get(self, request,id,cid):
        staff = Staff.objects.get(user=request.user)
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
            form = CreateStaffForm()
            context={'staff':staff,'form':form}
            return render(request,'admin/add_staff.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')
                
class Leads(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '4' or staff.stype == '6':
                new = Lead.objects.filter(status="New")
                pipe = Lead.objects.filter(status="In Pipeline")
            else:
                new = Lead.objects.filter(status="New",generator=staff)
                pipe = Lead.objects.filter(status="In Pipeline",generator=staff)
            page = Pagination(request,new,10)
            pages = Pagination(request,pipe,10)
            form = LeadCreateForm()
            context={'staff':staff,'form':form,'new':page,'pipe':pages}
            return render(request,'sales/leads.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

class ViewClosure(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '4' or staff.stype == '6':
                lead = Lead.objects.filter(status='Converted').order_by('-created_on')
            else:
                lead = Lead.objects.filter(status='Converted',generator=staff).order_by('-created_on')
            page = Pagination(request,lead,10)
            context={'staff':staff,'lead':page}
            return render(request,'sales/closure.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class ViewHistory(View):
    def get(self, request):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '4' or staff.stype == '6':
                lead = Lead.objects.all().order_by('-created_on')
            else:
                lead = Lead.objects.filter(generator=staff).order_by('-created_on')
            page = Pagination(request,lead,10)
            history = True
            context={'staff':staff,'lead':page,'history':history}
            return render(request,'sales/history.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class CreateStudentAccount(View):
    def get(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id=id)
            try:
                student = Student.objects.get(email=lead.email)
                if student:
                    ActivateStudent(student)
                    msg = 'Student account successfully activated'
                    context={'staff':staff,'lead':lead,'msg':msg} 
            except:
                process = "Are you sure you want to proceed?"
                context={'staff':staff,'lead':lead,'process':process}
            return render(request,'messages/sales/leads.html',context)
        else:
            return render(request,'messages/common/permission_error.html')
        
    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                context={'staff':staff,'msg':msg}
            except:
                alert = "Student account creation failed.Please try again"
                context={'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class ListLMSApprovals(View):
    def get(self, request):
        x = SalesManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '4':
                leads = Lead.objects.filter(approval='2',lms=False).order_by('-created_on')
            else:
                leads = Lead.objects.filter(approval='2',lms= False,to_be_approved_by= staff).order_by('-created_on')
            context={'staff':staff,'leads':leads}
            return render(request,'sales/lms_approval.html',context)
        else:
            return render(request,'messages/common/permission_error.html')


class ApproveLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            return redirect('convert_lead',id=id)
        else:
            return render(request,'messages/common/permission_error.html')




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
            return render(request,'messages/common/permission_error.html')

    def post(self, request,id):
        x = SalesOperation(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
                    print("test")
                    lead.to_be_approved_by = reporting.manager
                    lead.save()
                    msg = "Account has been marked for deletion and has been sent for approval."
                context={'staff':staff,'msg':msg}
            except:
                alert = "Account deletion failed.Please try again"
                context={'staff':staff,'alert':alert}
            return render(request,'messages/sales/leads.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class ListLMSDeletion(View):
    def get(self, request):
        x = SalesManagerCheck(request)
        if x == True:
            user = request.user
            staff = Staff.objects.get(user=request.user)
            if staff.stype == '4':
                lead = Lead.objects.filter(approval='2',lms = True)
            else:
                lead = Lead.objects.filter(approval='2',lms=True,to_be_approved_by = staff)
            context={'staff':staff,'lead':lead}
            return render(request,'sales/lms_deletion.html',context)
        else:
            return render(request,'messages/common/permission_error.html')


class ApproveDelLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            return redirect('revert_lead', id=id)
        else:
            return render(request,'messages/common/permission_error.html')

class RejectDelLMSProfile(View):
    def get(self, request,id):
        x = SalesManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            lead = Lead.objects.get(id = id)
            lead.approval = '1'
            lead.to_be_approved_by = staff
            lead.save()
            return redirect('list_lms_revert')
        else:
            return render(request,'messages/common/permission_error.html')





class Students(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.all().order_by('-start_date')
            context={'staff':staff,'student':student}
            return render(request,'common/students.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')

class AddJob(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = AddJobForm()
            context = {'staff':staff,'form':form}
            return render(request,'common/add_job.html',context)
        else:
            return render(request,'messages/common/permission_error.html')
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
            return render(request,'messages/common/permission_error.html')
            

class ViewTeqNews(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            staff = Staff.objects.get(user=request.user)
            posts = Post.objects.all()
            context={'staff':staff,'posts':posts}
            return render(request,'common/blog.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class ViewProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context={'staff':staff}
            return render(request,'common/profile.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class EditProfile(View):
    def get(self, request):
        x = StaffCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            form = CreateStaffForm(instance=staff)
            context={'staff':staff,'form':form}
            return render(request,'common/edit_profile.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

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
            return render(request,'messages/common/permission_error.html')


class OperationsDashboard(View):
    def get(self, request):
        x = OperationsCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context ={'staff':staff}
            return render(request,'operations/dashboard.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class EditStaff(View):
    def get(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            profile = Staff.objects.get(id=id)
            form = CreateStaffForm(instance=profile)
            reporting = Reporting.objects.get(user=profile)
            form_manager = ReportingForm(instance=reporting)
            context={'staff':staff,'form':form,'profile':profile,'form_manager':form_manager}
            return render(request,'admin/edit_staff.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

    def post(self, request,id):
        x = AdminCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
            return render(request,'messages/common/permission_error.html')


class SalesDashboard(View):
    def get(self, request):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context ={'staff':staff}
            return render(request,'operations/dashboard.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class GetStudentPaymentDetails(View):
    def get(self, request,id):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            student = Student.objects.get(id=id)
            try:
                spd = StudentPaymentData.objects.get(student=student)
            except:
                spd = StudentPaymentData(student=student,total="0")
                spd.save()
            payments = StudentPayments.objects.filter(spd=spd).order_by('-timestamp')
            feeform = StudentPaymentForm()
            context ={'staff':staff,'student':student,'spd':spd,'payments':payments,'feeform':feeform}
            return render(request,'sales/student_payments.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

    def post(self, request,id):
        x = SalesCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
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
            return render(request,'messages/common/permission_error.html')


class TrainerDashboard(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context ={'staff':staff}
            if staff.stype == '4' or staff.stype== '7':
                return redirect('trainer_manager_dashboard')
            else:
                return render(request,'trainer/dashboard.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class TrainerManagerDashboard(View):
    def get(self, request):
        x = TrainerManagerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            context ={'staff':staff}
            return render(request,'trainer/manager_dashboard.html',context)
        else:
            return render(request,'messages/common/permission_error.html')

class MyBatches(View):
    def get(self, request):
        x = TrainerCheck(request)
        if x == True:
            staff = Staff.objects.get(user=request.user)
            wdbatch = Batch.objects.filter(trainer=staff,type="Weekday")
            webatch = Batch.objects.filter(trainer=staff,type="Weekend")
            wdpage = Pagination(request,wdbatch,5)
            wepage = Pagination(request,webatch,5)
            context={'staff':staff,'wdbatch':wdpage,'webatch':wepage}
            return render(request,'trainer/my_batches.html',context)
        else:
            return render(request,'messages/common/permission_error.html')








                









        
                




            











            















        



            

            




















            
            

