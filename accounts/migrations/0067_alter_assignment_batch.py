# Generated by Django 3.2.8 on 2021-10-17 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0066_rename_attachments_assignment_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='batch',
            field=models.ForeignKey(blank=True, limit_choices_to={'status': '1'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.batch'),
        ),
    ]
