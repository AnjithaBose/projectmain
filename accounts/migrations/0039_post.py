# Generated by Django 3.2.8 on 2021-10-10 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_job_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('body', models.TextField(blank=True, max_length=10000, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
                ('pic_1', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
                ('pic_2', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
                ('pic_3', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
            ],
        ),
    ]
