# Generated by Django 3.2.8 on 2021-10-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0071_auto_20211018_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('1', 'Chat'), ('2', 'Account Creation'), ('3', 'Batch Update'), ('4', 'Query'), ('5', 'General'), ('6', 'Course')], max_length=100),
        ),
    ]