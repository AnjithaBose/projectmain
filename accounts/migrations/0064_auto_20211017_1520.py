# Generated by Django 3.2.8 on 2021-10-17 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0063_alter_defaultpics_webinar_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('In Pipeline', 'In Pipeline'), ('Converted', 'Converted'), ('Lost', 'Lost'), ('Not Interested', 'Not Interested')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('In Pipeline', 'In Pipeline'), ('Converted', 'Converted'), ('Lost', 'Lost'), ('Not Interested', 'Not Interested')], max_length=100, null=True),
        ),
    ]