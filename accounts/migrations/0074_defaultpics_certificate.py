# Generated by Django 3.2.8 on 2021-10-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0073_studentcoursedata_certificate_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultpics',
            name='certificate',
            field=models.ImageField(blank=True, default='accounts/static/images/Certificate.jpg', null=True, upload_to='images/default/'),
        ),
    ]