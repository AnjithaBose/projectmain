# Generated by Django 3.2.8 on 2021-10-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_alter_batch_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='username',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='staff',
            unique_together={('name',)},
        ),
    ]
