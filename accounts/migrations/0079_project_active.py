# Generated by Django 3.2.8 on 2021-10-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0078_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
