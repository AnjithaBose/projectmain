# Generated by Django 3.2.8 on 2021-10-16 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0053_batchdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalcount',
            name='user',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('stype', '4'), ('status', '5'), ('status', '6'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='last_edit_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edited_by', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.course'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='to_be_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='trainer',
            field=models.ForeignKey(blank=True, limit_choices_to={'stype': '3'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='batchdata',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.batch'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='chatroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.chatroom'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='user1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='user2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='generator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='representative', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='to_be_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='manager',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('stype', '4'), ('stype', '5'), ('stype', '6'), ('stype', '7'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentcoursedata',
            name='batch',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('status', '1'), ('status', '2'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='batch', to='accounts.batch'),
        ),
        migrations.AlterField(
            model_name='studentcoursedata',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='accounts.student'),
        ),
        migrations.AlterField(
            model_name='studentpaymentdata',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_payments', to='accounts.student'),
        ),
        migrations.AlterField(
            model_name='studentpayments',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='studentpayments',
            name='spd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_payment', to='accounts.studentpaymentdata'),
        ),
        migrations.AlterField(
            model_name='tempbatch',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.batch'),
        ),
        migrations.AlterField(
            model_name='tempbatch',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.course'),
        ),
        migrations.AlterField(
            model_name='tempbatch',
            name='to_be_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temp_approved_by', to='accounts.staff'),
        ),
        migrations.AlterField(
            model_name='tempbatch',
            name='trainer',
            field=models.ForeignKey(blank=True, limit_choices_to={'stype': '3'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'Chat'), ('2', 'Account Creation'), ('3', 'Batch Update'), ('4', 'Query'), ('5', 'General')], max_length=100)),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('user1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.staff')),
                ('user2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
            ],
        ),
    ]
