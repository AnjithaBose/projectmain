# Generated by Django 3.2.8 on 2021-10-17 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0060_webinar'),
    ]

    operations = [
        migrations.AddField(
            model_name='webinar',
            name='cover_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/webinar_cover/'),
        ),
    ]
