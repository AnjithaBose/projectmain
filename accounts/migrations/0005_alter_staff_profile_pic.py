# Generated by Django 3.2.8 on 2021-10-07 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211007_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/user3.png', null=True, upload_to='images/dp/'),
        ),
    ]
