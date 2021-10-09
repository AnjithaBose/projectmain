# Generated by Django 3.2.8 on 2021-10-09 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_studentcoursedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcoursedata',
            name='batch',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('status', 'Ongoing'), ('status', 'Yet to Start'), _connector='OR'), on_delete=django.db.models.deletion.PROTECT, related_name='batch', to='accounts.batch'),
        ),
    ]
