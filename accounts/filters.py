import django_filters
from django_filters import CharFilter

from .models import *


class StudentFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name',lookup_expr='icontains')
    email = CharFilter(field_name='email',lookup_expr='icontains')
    batches_attended = CharFilter(field_name='batches_attended',lookup_expr='icontains')
    now_attending = CharFilter(field_name='now_attending',lookup_expr='icontains')
    class Meta:
        model = Student
        fields = ['name','email','course_enrolled','batches_attended','now_attending','status']

class BatchFilter(django_filters.FilterSet):
    batch_code = CharFilter(field_name='batch_code',lookup_expr='icontains')
    class Meta:
        model = Batch
        fields = ['subject','batch_code','trainer','type','status']