from .models import *
from django.core.paginator import Paginator,EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.models import User



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

def Pagination(request,object,count):
    p = Paginator(object,count)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return (page)


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
            if staff.stype == '6' or staff.stype=='4' or staff.stype== '5':
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
        

def BatchStrength(request,id):
    batch = Batch.objects.get(id=id)
    scd = StudentCourseData.objects.filter(batch=batch)
    count =0
    for i in scd:
        count = count + 1
    batch.strength = count
    batch.save()
    return(batch)

def CopyBatch(batch):
    temp = TempBatch(batch=batch,subject=batch.subject,batch_code=batch.batch_code,trainer=batch.trainer,start_date=batch.start_date,end_date=batch.end_date,start_time=batch.start_time,end_time=batch.end_time,link=batch.link,passcode=batch.passcode,type=batch.type,status=batch.status)
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








