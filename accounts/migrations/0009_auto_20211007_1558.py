# Generated by Django 3.2.8 on 2021-10-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_batch_batch_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
