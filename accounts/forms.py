from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class CourseCreateForm(ModelForm):
    pic = forms.ImageField(required=False)
    class Meta:
        model = Course
        fields = '__all__'

class BatchCreateForm(ModelForm):
    subject = forms.ModelChoiceField(queryset=Course.objects.all(),required=False)
    trainer = forms.ModelChoiceField(queryset=Staff.objects.filter(stype='3'),required=False)
    link = forms.CharField(required=False)
    passcode = forms.CharField(required=False)
    class Meta:
        model = Batch
        fields = ['subject','trainer','start_date','end_date','start_time','end_time','link','passcode','type','status']

class SendMailForm(ModelForm):
    to = forms.CharField(required=False)
    class Meta:
        model = Email
        fields = '__all__'

class SendChatMessageForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']

class CreateStaffForm(ModelForm):
    blood_group = forms.ChoiceField(required=False,choices = groups)
    house = forms.CharField(required=False)
    street = forms.CharField(required=False)
    street2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.ChoiceField(required=False,choices=state)
    stype = forms.ChoiceField(required=False,choices=Staff.value)
    profile_pic = forms.ImageField(required=False)
    facebook = forms.CharField(required=False)
    linkedin = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    class Meta:
        model = Staff
        fields = ['name','empid','mobile','email','sex','dob','doj','blood_group','house','street','street2','city','state','pin','stype','profile_pic','facebook','linkedin','instagram']

        


