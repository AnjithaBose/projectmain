# Generated by Django 3.2.8 on 2021-10-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_socialprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='facebook',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='instagram',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='linkedin',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='SocialProfile',
        ),
    ]
