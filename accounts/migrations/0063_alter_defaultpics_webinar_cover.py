# Generated by Django 3.2.8 on 2021-10-17 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0062_defaultpics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultpics',
            name='webinar_cover',
            field=models.ImageField(blank=True, default='accounts/static/images/webinar_cover.jpg', null=True, upload_to='images/default/'),
        ),
    ]