from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.db.models import Q


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
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    start_time = forms.TimeField(required=False)
    end_time = forms.TimeField(required=False)
    type = forms.ChoiceField(required=False,choices=(('Weekend', 'Weekend'),('Weekday','Weekday')))
    class Meta:
        model = Batch
        fields = ['subject','trainer','start_date','end_date','start_time','end_time','link','passcode','type','status']

class SendMailForm(ModelForm):
    to = forms.CharField(required=False)
    class Meta:
        model = Email
        fields = '__all__'

class SendChatMessageForm(ModelForm):
    pic = forms.ImageField(required=False)
    message = forms.CharField(required=False)
    class Meta:
        model = ChatMessage
        fields = ['message','pic']

class SendQueryMessageForm(ModelForm):
    message = forms.CharField(required=False)
    pic = forms.ImageField(required=False)
    class Meta:
        model = ChatQuery
        fields = ['message','pic']

class CreateStaffForm(ModelForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
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
    status = forms.ChoiceField(required=False,choices=(('Active','Active'),('Inactive','Inactive')))
    class Meta:
        model = Staff
        fields = ['name','empid','mobile','email','sex','dob','doj','blood_group','house','street','street2','city','state','pin','stype','profile_pic','facebook','linkedin','instagram','status']

class LeadCreateForm(ModelForm):
    class Meta:
        model = Lead
        fields = ['name','email','mobile','sex','status']

class AddSCDForm(ModelForm):
    class Meta:
        model = StudentCourseData
        fields = ['batch']

class AddJobForm(ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Job
        fields = ['tags','title','description','link']

class ReportingForm(ModelForm):
    class Meta:
        model = Reporting
        fields = ['manager']

class UpdateTotalFee(ModelForm):
    class Meta:
        model = StudentPaymentData
        fields = ['total']

class StudentPaymentForm(ModelForm):
    class Meta:
        model = StudentPayments
        fields = ['amount']

class AddBatchDataForm(ModelForm):
    class Meta:
        model = BatchData
        fields = ['topic','link']

class AddWebinarForm(ModelForm):
    cover_pic = forms.ImageField(required=False)
    class Meta:
        model = Webinar
        fields = ['topic','description','date','time','status','meeting_link','cover_pic']

class PublicLeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = ['name','email','mobile']

class AddAssignmentForm(ModelForm):
    link = forms.CharField(required=False)
    attachment = forms.FileField(required=False)
    class Meta:
        model = Assignment
        fields = ['topic','batch','description','link','attachment']

class AddProjectsForm(ModelForm):
    link = forms.CharField(required=False)
    attachment = forms.FileField(required=False)
    class Meta:
        model = Project
        fields = ['batch','description','link','attachment','final_date']

class SubmitAssignmentForm(ModelForm):
    link = forms.CharField(required=False)
    attachment = forms.FileField(required=False)
    class Meta:
        model = StudentAssignmentData
        fields = ['link','attachment']

class SubmitProjectForm(ModelForm):
    link = forms.CharField(required=False)
    attachment = forms.FileField(required=False)
    class Meta:
        model = StudentProjectData
        fields = ['link','attachment']

class EditProfileForm(ModelForm):
    sex = forms.ChoiceField(choices=sex_choices,required=False)
    dob = forms.DateField(required=False)
    blood_group = forms.ChoiceField(required=False,choices=groups)
    house = forms.CharField(required=False)
    street =forms.CharField(required=False)
    street2 =forms.CharField(required=False)
    city = forms.CharField(required=False)
    profile_pic = forms.ImageField(required=False)
    cv = forms.FileField(required=False)
    pincode = forms.CharField(required=False)
    class Meta:
        model = Student
        fields = ['pincode','mobile','sex','dob','blood_group','house','street','street2','city','state','profile_pic','cv']


class AddTasksForm(ModelForm):
    status = forms.ChoiceField(required=False, choices=values)
    attachment = forms.FileField(required=False)
    class Meta:
        model = Task
        fields =['topic','description','user','status','attachment']

class TaskUpdateForm(ModelForm):
    status = forms.ChoiceField(required=False,choices=values)
    class Meta:
        model = Task
        fields = ['status']

class AddNotesForm(ModelForm):
    attachment = forms.FileField(required=False)
    class Meta:
        model = Notes
        fields = ['topic','description','attachment']
        
class LeadReassignForm(ModelForm):
    class Meta:
        model = Lead
        fields = ['assigned_to']

class AddComplaintsForm(ModelForm):
    pic1 = forms.FileField(required=False)
    pic2 = forms.FileField(required=False)
    pic3 = forms.FileField(required=False)
    class Meta:
        model = Complaint
        fields = ['topic','description','pic1','pic2','pic3']

class UpdateComplaintStatusForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']

class UpdateComplaintAssigneeForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['assignee']

class AddCommentForm(ModelForm):
    pic1 = forms.FileField(required=False)
    pic2 = forms.FileField(required=False)
    pic3 = forms.FileField(required=False)
    class Meta:
        model = ComplaintComment
        fields = ['message','pic1','pic2','pic3']





        

        


