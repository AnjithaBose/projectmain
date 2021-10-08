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
        


