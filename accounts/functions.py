from .models import *
from django.core.paginator import Paginator,EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.models import User
import time
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

today = datetime.datetime.now()


def AdminCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def MainOperation(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4' or staff.stype== '6' or staff.stype== '5' or staff.stype== '1':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def MainOperationTrainers(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4' or staff.stype== '6' or staff.stype== '5' or staff.stype== '1' or staff.stype== '7':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)


def Pagination(request,object,count):
    p = Paginator(object,count)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return (page)


def SalesManagerCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype=='4' or staff.stype== '6':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)


def OperationsCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '1' or staff.stype=='4' or staff.stype== '5':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def ManagerCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '6' or staff.stype=='4' or staff.stype== '5' or staff.stype== '7':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def SalesCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4' or staff.stype=='2' or staff.stype== '6':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def mailsend(request,subject,message,from_address,to):
    email_list = to.split(",")
    for i in email_list:
        send_mail(
            subject,
            message,
            'techsupport@teqstories.com',
            [i],
            fail_silently=False,
        )
    

def StaffCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff:
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def SalesOperation(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '6' or staff.stype=='4' or staff.stype== '5' or staff.stype== '2':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def StudentConvert(request,lead):
    user = User.objects.create_user(lead.email,lead.email,lead.mobile)
    user.save()
    student = Student(user=user,name=lead.name,email=lead.email,mobile=lead.mobile,sex=lead.sex,start_date=datetime.datetime.now())
    student.save()
    return (student)

def NotTrainerCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '6' or staff.stype=='4' or staff.stype== '5' or staff.stype== '2' or staff.stype== '1':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def scd(request,student):
    student.course_enrolled = []
    student.now_attending = []
    cd = StudentCourseData.objects.filter(student=student)
    for i in cd:
        student.course_enrolled.append(i.batch.subject.code)
        if i.batch.status == '1':
            student.now_attending.append(i.batch.batch_code)
    student.save()

def FindSCD(request,students):
    for stud in students:
        scd(request,stud)
        

def BatchStrength(request,id):
    batch = Batch.objects.get(id=id)
    scd = StudentCourseData.objects.filter(batch=batch)
    count =0
    for i in scd:
        count = count + 1
    batch.strength = count
    batch.save()
    return(batch)

def CopyBatch(request,batch):
    staff=Staff.objects.get(user=request.user)
    if staff.stype == '4':
        manager = staff
    else:
        manager = Manager(staff)
    temp = TempBatch(batch=batch,subject=batch.subject,batch_code=batch.batch_code,trainer=batch.trainer,start_date=batch.start_date,end_date=batch.end_date,start_time=batch.start_time,end_time=batch.end_time,link=batch.link,passcode=batch.passcode,type=batch.type,to_be_approved_by=manager)
    temp.save()
    return (temp)

def FindRoom(request,staff,id):
    receiver = Staff.objects.get(id=id)       
    try:
        chatroom = ChatRoom.objects.get(user1=staff,user2=receiver)
    except:
        try:
            chatroom = ChatRoom.objects.get(user1=receiver,user2=staff)
        except:
            chatroom = ChatRoom(user1 = staff, user2 = receiver)
            chatroom.save()
    return(chatroom)

def CheckActive(f):
    staff = Staff.objects.get(email=f.email)
    user = staff.user
    if f.status == 'Inactive' :
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    staff.save()

def DeleteStudent(student):
    user = User.objects.get(username=student.user)
    # student.delete()
    # user.delete()
    user.is_active = False
    user.save()
    student.status = 'Inactive'
    student.save()

def ActivateStudent(student):
    user = User.objects.get(username=student.user)
    user.is_active = True
    user.save()
    lead = Lead.objects.get(email=student.email)
    lead.status = 'Converted'
    lead.approval = '1'
    lead.save()
    student.save()

def CheckAccount(username):
    m=""
    try:
        staff = Staff.objects.get(user__username=username)
        if staff:
            user = staff.user
            if user.is_active:
                m ="Invalid login.Check your credentials!" 
            else:
                m = 'Staff account has been suspended. Please contact your reporting manager.'
        else:
            m ="Invalid login.Check your credentials!" 
    except:
        student = Student.objects.get(user__username=username)
        if student:
            if student.status == 'Inactive' :
                m ="Account has been suspended.Contact your representative."
        else:
            m ="Invalid login.Check your credentials!"
    finally:
        if m == "":
            m ="Invalid login.Check your credentials!"
        return(m)

def Manager(staff):
    reporting = Reporting.objects.get(user=staff)
    return(reporting.manager) 

def StudentAccountCreation(request,lead):
    student = StudentConvert(request,lead)
    lead.approval = '1'
    staff = Staff.objects.get(user=request.user)
    lead.to_be_approved_by = staff
    lead.lms = True
    lead.save()
    subject="[TEQSTORIES]-ACCOUNT CREATED"
    message =  "Hi Learner, \n\n\nYour account has created with https://lms.teqstories.com. Please login using your email as username and mobile number as password. \n\n\nIf you feel any difficulty please contact our representative or mail us as techsupport@teqstories.com. \n\n\nWith Regards,\nStudent Support Team,\nTeqstories "
    from_address = 'techsupport@teqstories.com'
    to = lead.email
    mailsend(request,subject,message,from_address,to)

def TrainerCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype == '3' or staff.stype=='4' or staff.stype== '7':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)
            

def TrainerManagerCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            staff = Staff.objects.get(user=user)
            if staff.stype=='4' or staff.stype== '7':
                return (True)
            else:
                return (False)
        except:
            return (False)
    else:
        return (False)

def Uniquecode(request,subject_code,code):
    code = str(code[-4:])
    batch_code = "%s_%s" % (subject_code, code)
    try:
        batch = Batch.objects.get(batch_code=code)
        if batch :
            code = str(int(code)+1)
            Uniquecode(subject_code, code)
    except:
        return (batch_code)

def Notifications(staff):
    notifications = Notification.objects.filter(user1=staff,status='2').order_by('-date').order_by('-time')
    return notifications
def CountNotifications(notifications):
    count = 0
    for i in notifications:
        count = count +1 
    return count

def MarkAsRead(notify):
    for i in notify:
        i.status = '1'
        i.save()

def MonthlyRevenue():
    count = 0
    sp = StudentPayments.objects.all()
    for i in sp:
        if i.timestamp.month == today.month:
            count = int(count) + int(i.amount)
    return(count)

def CurrentActiveStudents():
    count = 0
    students = Student.objects.all()
    for i in students:
        if i.now_attending == "[]":
            count = count + 1
    st = students.count()
    st = st - count
    return (st)

def ClosedLeads():
    closed_leads = Lead.objects.filter(status='Converted')
    c1 = 0
    for i in closed_leads:
        if str(i.created_on.strftime('%b'))== str(today.strftime('%b')):
            pass
        else:
            c1 = c1 + 1
            closed_leads.exclude(email=i.email)
    cl=closed_leads.count()
    cl = cl-c1
    return (cl)

def StudentCheck(request):
    user = request.user
    if user.is_authenticated:
        try:
            student = Student.objects.get(user=user)
            if student:
                return (True)
            else:
                return (False)
        except:
            staff = Staff.objects.get(user=user)
            if staff.stype == '4':
                return (True)
            else:
                return (False)
    else:
        return (False)

def StudentNotifications(student):
    notifications = Notification.objects.filter(user2=student,status='2').order_by('-date').order_by('-time')
    return notifications

def StudentBatches(student):
    scd = StudentCourseData.objects.filter(student=student)
    batch = []
    for i in scd:
        batch.append(i.batch.batch_code)
    batches = Batch.objects.filter(batch_code__in=batch)
    return (batches)

def StudentActiveBatches(student):
    scd = StudentCourseData.objects.filter(student=student)
    batch = []
    for i in scd:
        batch.append(i.batch.batch_code)
    batches = Batch.objects.filter(batch_code__in=batch,status='1')
    return (batches)

def SendStudentNotification(type, student,message):
    date = datetime.datetime.today()
    time = datetime.datetime.now()
    timestamp = datetime.datetime.now()
    n=Notification(type=type,user2=student,message=message,date=date,time=time,timestamp=timestamp)
    n.save()

def CreateCertificate(student,scd):
    epoch = time.time()
    spd_id = "TS"
    certificate_id = "%s_%d" % (spd_id, epoch)
    template = DefaultPics.objects.get(id=3)
    certificate_id = str(certificate_id)
    date = str(datetime.datetime.now().date())
    img = Image.open(template.certificate)
    draw = ImageDraw.Draw(img)
    file_name = str("images/certificates/"+certificate_id+".pdf")
    selectFont = ImageFont.truetype("arialbd.ttf", size = 150)
    courseFont = ImageFont.truetype("arialbd.ttf", size = 100)
    codeFont = ImageFont.truetype("arialbd.ttf", size = 80)
    draw.text( (1750,980), student.name, (1,91,153),anchor="ma",font=selectFont,align ="center")
    draw.text( (1750,1430), scd.batch.subject.name, (1,1,1),anchor="ma",font=courseFont,align ="center")
    draw.text( (746,1960),certificate_id, (1,1,1),anchor="ma",font=codeFont,align ="center")
    draw.text( (1786,1960), date, (1,1,1),anchor="ma",font=codeFont,align ="center")
    img.save( file_name, "PDF", resolution=70.0)
    scd.certificate_id = certificate_id
    scd.save()


def SendNotification(type, staff,message):
    date = datetime.datetime.today()
    time = datetime.datetime.now()
    timestamp = datetime.datetime.now()
    n=Notification(type=type,user1=staff,message=message,date=date,time=time,timestamp=timestamp)
    n.save()

def CurrentBatches():
    return  Batch.objects.filter(status='1')

def UpcomingBatches():
    return Batch.objects.filter(status='2')

def ActiveLeads():
    return Lead.objects.filter(Q(status='New')|Q(status='In Pipeline'))

def UpcomingWebinar():
    return Webinar.objects.filter(status='Upcoming')

def UnallocatedStudents():
    stud = Student.objects.all()
    name = []
    for i in stud:
        if i.course_enrolled :
            pass
        else:
            name.append(i.name)
    students = Student.objects.filter(name__in=name)
    return (students)

def PendingTask(staff):
    return Task.objects.filter(user=staff,complete=False)

def Managing(staff):
    name = []
    reporting = Reporting.objects.all()
    for i in reporting:
        if i.manager == staff:
            name.append(i.user)
    staff_members = Staff.objects.filter(name__in=name)
    return(staff_members)

def StaffBirthdays():
    name = []
    staff = Staff.objects.all()
    for i in staff:
        if i.dob.month == today.month and i.dob.day > today.day:
            name.append(i.name)
    birthdays = Staff.objects.filter(name__in=name)
    return (birthdays)

def UnallocatedBatches():
    batches = Batch.objects.filter(trainer = None)
    return (batches)


def FindQueryRoom(request,id):
    receiver = Staff.objects.get(id=id)
    student = Student.objects.get(user=request.user)       
    try:
        chatroom = ChatRoom.objects.get(user1=receiver,student=student)
    except:
        chatroom = ChatRoom(user1 =receiver,student=student)
        chatroom.save()
    return(chatroom)






            











