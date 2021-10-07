from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class CourseCreateForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'