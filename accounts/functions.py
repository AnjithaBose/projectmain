from .models import *
from django.core.paginator import Paginator,EmptyPage
from django.core.mail import send_mail


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
            from_address,
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



