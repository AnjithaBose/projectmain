# Generated by Django 3.2.8 on 2021-10-12 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_chatmessage_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempbatch',
            name='to_be_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='temp_approved_by', to='accounts.staff'),
        ),
    ]
