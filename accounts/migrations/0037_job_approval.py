# Generated by Django 3.2.8 on 2021-10-10 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_alter_studentcoursedata_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='approval',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], max_length=20, null=True),
        ),
    ]
