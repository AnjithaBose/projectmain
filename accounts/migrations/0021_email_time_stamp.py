# Generated by Django 3.2.8 on 2021-10-08 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_email_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='time_stamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]