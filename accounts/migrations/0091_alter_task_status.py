# Generated by Django 3.2.8 on 2021-10-21 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0090_alter_student_cv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('0', '0'), ('25', '25'), ('50', '50'), ('75', '75'), ('100', '100')], default='0', max_length=100, null=True),
        ),
    ]