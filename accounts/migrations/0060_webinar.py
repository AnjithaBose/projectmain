# Generated by Django 3.2.8 on 2021-10-17 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0059_auto_20211017_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, max_length=3000, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Upcoming', 'Upcoming'), ('Completed', 'Completed')], default='Upcoming', max_length=100, null=True)),
                ('strength', models.CharField(blank=True, max_length=100, null=True)),
                ('public_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('meeting_link', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
