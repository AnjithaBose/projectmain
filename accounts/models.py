from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.utils import timezone
# Create your models here.

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



class Staff(models.Model):
    value= (
    ('1', 'Operations'),
    ('2', 'Sales'),
    ('3', 'Trainer'),
    ('4', 'Admin'),
    )
    user = models.OneToOneField(User,on_delete=models.PROTECT,null=True,blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    empid = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=10,null=True, blank=True)
    email = models.EmailField(max_length=200,null=True, blank=True)
    sex = models.CharField(max_length=10,null=True,choices=(('Male','Male'),('Female','Female'),('Others','Others')), blank=True)
    dob = models.DateField(null=True, blank=True)
    doj = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=100,null=True, blank=True,choices=groups)
    house = models.CharField(max_length=100,null=True, blank=True)
    street =models.CharField(max_length=100,null=True, blank=True)
    street2 =models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True,choices=state, blank=True)
    stype = models.CharField(max_length=100,null=True,choices=value, blank=True)
    status = models.CharField(max_length=20,choices=(('Active','Active'),('Inactive','Inactive')),default='Active')
    profile_pic = models.ImageField(null=True, blank=True,upload_to='images/dp/')
    approval = models.BooleanField(null=True, blank=True, default=False)
    admin_status = models.BooleanField(null=True, blank=True, default=False)


    def __str__(self):
        return self.name
