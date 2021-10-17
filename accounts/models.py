from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.utils import timezone
# Create your models here.

class DefaultPics(models.Model):
    webinar_cover = models.ImageField(null=True, blank=True,upload_to='images/default/',default='accounts/static/images/webinar_cover.jpg')

state = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal')
    )
groups = (
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    )

sex_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

approval_choices =(
    ('1', 'Approved'),
    ('3', 'Rejected'),
    ('2', 'Pending'),
)

groups = (
    ('New', 'New'),
    ('In Pipeline', 'In Pipeline'),
    ('Converted', 'Converted'),
    ('Lost', 'Lost'),
    ('Not Interested', 'Not Interested'),
    )



class Staff(models.Model):
    value= (
    ('1', 'Operations'),
    ('2', 'Sales'),
    ('3', 'Trainer'),
    ('4', 'Admin'),
    ('5', 'Operations Manager'),
    ('6', 'Sales Manager'),
    ('7', 'Trainer Manager'),

    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    empid = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=10,null=True, blank=True)
    email = models.EmailField(max_length=200,null=True, blank=True)
    sex = models.CharField(max_length=10,null=True,choices=sex_choices, blank=True)
    dob = models.DateField(null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=100,null=True, blank=True,choices=groups)
    house = models.CharField(max_length=100,null=True, blank=True)
    street =models.CharField(max_length=100,null=True, blank=True)
    street2 =models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True,choices=state, blank=True)
    pin = models.CharField(max_length=100,null=True,blank=True)
    stype = models.CharField(max_length=100,null=True,choices=value, blank=True)
    status = models.CharField(max_length=20,choices=(('Active','Active'),('Inactive','Inactive')),default='Active')
    profile_pic = models.ImageField(null=True, blank=True,upload_to='images/dp/',default='accounts/static/images/user3.png')
    facebook = models.CharField(max_length=1000, null=True, blank=True)
    linkedin = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.CharField(max_length=1000, null=True, blank=True)
    approval = models.BooleanField(null=True, blank=True, default=False)


    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['name']]


    


class Course(models.Model):
    name = models.CharField(max_length=1000,null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True)
    pic = models.ImageField(null=True, blank=True, default='accounts/static/images/course.jpg',upload_to='images/course/')

    def __str__(self):
        return self.name

class Batch(models.Model):
    subject = models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_code = models.CharField(max_length=500, blank=True)
    trainer = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,limit_choices_to={'stype':"3"})
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    passcode = models.CharField(max_length=250,null=True, blank=True)
    type = models.CharField(max_length=100,choices=(('Weekend', 'Weekend'),('Weekday','Weekday')))
    status = models.CharField(max_length=100,choices=(('2','Yet to Start'),('1','Ongoing'),('3','Completed'),('4','Cancelled')),default='2')
    strength = models.IntegerField(null=True, blank=True)
    last_edit_time = models.DateTimeField(null=True, blank=True)
    last_edit_user = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name='edited_by')
    approval = models.CharField(max_length=100,null=True, blank=True,choices=approval_choices ,default='2')
    to_be_approved_by = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name='approved_by')
    def __str__(self):
        s = "-"
        return "%s %s %s %s %s %s %s" % (self.batch_code,s, self.trainer,s,self.start_date,s, self.start_time)

class TempBatch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)
    subject = models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_code = models.CharField(max_length=500, blank=True)
    trainer = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,limit_choices_to={'stype':"3"})
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    passcode = models.CharField(max_length=250,null=True, blank=True)
    type = models.CharField(max_length=100,choices=(('Weekend', 'Weekend'),('Weekday','Weekday')))
    status = models.CharField(max_length=100,choices=(('2','Yet to Start'),('1','Ongoing'),('3','Completed'),('4','Cancelled')),default='2')
    to_be_approved_by = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name='temp_approved_by')

class BatchData(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,null=True, blank=True)
    topic = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=10000,null=True, blank=True)
    date = models.DateField(null=True, blank=True)


class Reporting(models.Model):
    user = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name='staff')
    manager = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name='manager',limit_choices_to=Q(stype='4')|Q(stype='5')|Q(stype='6')|Q(stype='7'))

class ApprovalCount(models.Model):
    user = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,limit_choices_to=(Q(stype='4')|Q(status='5')|Q(status='6')),)
    count = models.CharField(max_length=100, null=True, blank=True)

class Email(models.Model):
    subject = models.CharField(max_length=1000, null=True, blank=True)
    message = models.TextField(max_length=10000,null=True, blank=True)
    from_address = models.EmailField(null=True, blank=True)
    to_address= models.CharField(max_length=5000,null=True, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100,null=True, blank=True,choices=(('Mail','Mail'),('Draft','Draft')))

    def __str__(self):
        return self.subject

class ChatRoom(models.Model):
    user1 = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name="user1")
    user2 = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True,related_name="user2")

class ChatMessage(models.Model):
    chatroom =models.ForeignKey(ChatRoom,null=True, blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True)
    username = models.CharField(max_length=500,null=True, blank=True)
    pic = models.CharField(max_length=2000,null=True, blank=True)
    message = models.CharField(max_length=5000,null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
            return "[%s] %s by user: %s" % (
                self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                self.message,
                self.user,
                self.chatroom
            )


class Job(models.Model):
    tags = models.CharField(max_length=500,null=True, blank=True)
    title = models.CharField(max_length=500,null=True, blank=True)
    description = models.TextField(max_length=2000,null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    link = models.URLField(max_length=2000,null=True, blank=True)
    approval = models.CharField(max_length=20,null=True, blank=True,choices=approval_choices)

    


class Lead(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    sex = models.CharField(max_length=10,null=True,choices=sex_choices,blank=True,default="Male")
    generator = models.ForeignKey(Staff,on_delete=models.CASCADE, blank=True,null=True,related_name='representative')
    created_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100,null=True, blank=True,choices=groups,default="New")
    lms = models.BooleanField(default = False)
    approval = models.CharField(max_length=100,null=True, blank=True,choices=approval_choices)
    to_be_approved_by = models.ForeignKey(Staff,on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,blank=True)
    mobile = models.CharField(max_length=10,blank=True)
    email = models.EmailField(max_length=200,blank=True)
    sex = models.CharField(max_length=10,null=True,choices=sex_choices,blank=True)
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=100,null=True, blank=True,choices=groups)
    house = models.CharField(max_length=100,null=True,blank=True)
    street =models.CharField(max_length=100,null=True,blank=True)
    street2 =models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,choices=state,blank=True)
    course_enrolled = models.CharField(max_length=1000,null=True,blank=True)
    now_attending = models.CharField(max_length=1000,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    shared = models.CharField(max_length=100,choices=(('Yes', 'Yes'), ('No', 'No')),blank=True,null=True,default='No')
    status = models.CharField(max_length=20,choices=(('Active','Active'),('Inactive','Inactive')),default='Active',blank=True)
    profile_pic = models.ImageField(null=True,default='accounts/static/images/user1.png',blank=True, upload_to='images/dp/')
    cv = models.FileField(blank=True, null=True,upload_to='data/cv/')

    def __str__(self):
        return self.name

class StudentCourseData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student',null=True,blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE,related_name='batch',limit_choices_to=(Q(status='1')|Q(status='2')),blank=True)

class StudentPaymentData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_payments',null=True,blank=True)
    total = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.student.name

class StudentPayments(models.Model):
    spd = models.ForeignKey(StudentPaymentData,on_delete=models.CASCADE,null=True, blank=True,related_name='student_payment')
    amount = models.CharField(max_length=100,null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    representative = models.ForeignKey(Staff, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.spd.student.name



class Post(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    body = models.TextField(max_length=10000,null=True, blank=True)
    cover = models.ImageField(null=True, blank=True, upload_to='images/blog/')
    pic_1 = models.ImageField(null=True, blank=True, upload_to='images/blog/')
    pic_2 = models.ImageField(null=True, blank=True, upload_to='images/blog/')
    pic_3 = models.ImageField(null=True, blank=True, upload_to='images/blog/')


class Notification(models.Model):
    type = models.CharField(max_length=100,choices=(('1','Chat'), ('2','Account Creation'),('3','Batch Update'),('4','Query'),('5','General')))
    user1 = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True, blank=True)
    user2 = models.ForeignKey(Student,on_delete=models.CASCADE,null=True, blank=True)
    message = models.CharField(max_length=500, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=100,choices=(('1','Read'),('2','Unread')),default='2')

class Task(models.Model):
    user = models.ForeignKey(Staff,null=True, blank=True,on_delete=models.CASCADE,related_name='task_for')
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100,null=True, blank=True,choices=(('Pending','Pending'),('Complete','Complete')))
    assigned_by = models.ForeignKey(Staff,null=True, blank=True,on_delete=models.CASCADE,related_name='assigned_by')

class Webinar(models.Model):
    topic = models.CharField(max_length=1000,null=True, blank=True)
    description = models.TextField(max_length=3000,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=100,null=True, blank=True,choices=(('Upcoming','Upcoming'),('Completed','Completed')),default='Upcoming')
    strength = models.CharField(max_length=100,null=True, blank=True)
    public_url = models.CharField(max_length=1000, null=True, blank=True)
    meeting_link = models.CharField(max_length=1000, null=True, blank=True)
    cover_pic = models.ImageField(null=True, blank=True,upload_to='images/webinar_cover/')

    def __str__(self):
        return self.topic






    




