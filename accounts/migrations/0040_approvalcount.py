# Generated by Django 3.2.8 on 2021-10-11 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, limit_choices_to=models.Q(('stype', '4'), ('status', '5'), ('status', '6'), _connector='OR'), null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.staff')),
            ],
        ),
    ]
