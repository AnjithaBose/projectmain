# Generated by Django 3.2.8 on 2021-10-17 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0067_alter_assignment_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('link', models.CharField(blank=True, max_length=2000, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='images/assignment/')),
                ('date', models.DateField(blank=True, null=True)),
                ('final_date', models.DateField(blank=True, null=True)),
                ('batch', models.ForeignKey(blank=True, limit_choices_to=models.Q(('status', '1'), ('status', '3'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.batch')),
            ],
        ),
    ]
