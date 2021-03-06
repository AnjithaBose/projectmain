# Generated by Django 3.2.8 on 2021-10-20 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0082_task_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('AB+', 'AB+'), ('AB-', 'AB-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('AB+', 'AB+'), ('AB-', 'AB-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=100, null=True),
        ),
    ]
