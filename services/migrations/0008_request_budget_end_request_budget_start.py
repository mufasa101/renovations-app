# Generated by Django 4.0.4 on 2022-04-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_alter_request_authorized_alarm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='budget_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='budget_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
