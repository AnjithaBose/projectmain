# Generated by Django 3.2.8 on 2021-10-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_reporting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=1000, null=True)),
                ('message', models.TextField(blank=True, max_length=10000, null=True)),
                ('from_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('to_address', models.CharField(blank=True, max_length=5000, null=True)),
            ],
        ),
    ]
