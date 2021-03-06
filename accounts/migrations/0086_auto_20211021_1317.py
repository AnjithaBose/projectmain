# Generated by Django 3.2.8 on 2021-10-21 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0085_student_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='status',
            field=models.CharField(blank=True, choices=[('Read', 'Read'), ('Unread', 'Unread')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
