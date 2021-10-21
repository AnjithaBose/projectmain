# Generated by Django 3.2.8 on 2021-10-21 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0086_auto_20211021_1317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='status',
            new_name='student_status',
        ),
        migrations.RenameField(
            model_name='chatroom',
            old_name='timestamp',
            new_name='student_timestamp',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user_1_status',
            field=models.CharField(blank=True, choices=[('Read', 'Read'), ('Unread', 'Unread')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user_1_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user_2_status',
            field=models.CharField(blank=True, choices=[('Read', 'Read'), ('Unread', 'Unread')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user_2_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
