# Generated by Django 3.2.8 on 2021-10-30 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0102_alter_lead_assigned_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='username',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
