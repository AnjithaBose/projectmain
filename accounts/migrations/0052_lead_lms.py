# Generated by Django 3.2.8 on 2021-10-15 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_auto_20211013_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='lms',
            field=models.BooleanField(default=False),
        ),
    ]
