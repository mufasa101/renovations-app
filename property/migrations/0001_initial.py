# Generated by Django 4.0.4 on 2022-04-13 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.IntegerField(blank=True, null=True)),
                ('unit_name', models.CharField(max_length=35)),
                ('unit_designation', models.CharField(max_length=35)),
                ('unit_type', models.CharField(blank=True, max_length=35, null=True)),
                ('move_out_date', models.DateField(blank=True, null=True)),
                ('move_in_date', models.DateField(blank=True, null=True)),
                ('made_ready_date', models.DateField(blank=True, null=True)),
                ('days_vacant', models.IntegerField(default=0)),
                ('priror_rent', models.IntegerField(default=0)),
                ('net_renovated_rent', models.IntegerField(default=0)),
                ('monthly_net_increase', models.IntegerField(default=0)),
                ('annualized_increase', models.IntegerField(default=0)),
                ('paint_contractor', models.IntegerField(default=0)),
                ('resurface', models.IntegerField(default=0)),
                ('cabinets', models.IntegerField(default=0)),
                ('cabinets_hardware', models.IntegerField(default=0)),
                ('quartz_counter_top', models.IntegerField(default=0)),
                ('appliance_package', models.IntegerField(default=0)),
                ('carpet', models.IntegerField(default=0)),
                ('flooring', models.IntegerField(default=0)),
                ('tub_tile', models.IntegerField(default=0)),
                ('hardware', models.IntegerField(default=0)),
                ('blinds', models.IntegerField(default=0)),
                ('misc', models.IntegerField(default=0)),
                ('total_renovation', models.IntegerField(default=0)),
                ('annualized_return', models.IntegerField(default=0)),
                ('lighting', models.IntegerField(default=0)),
                ('date_completed', models.IntegerField(default=0)),
                ('comments', models.TextField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='charges_added_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Units',
                'ordering': ['unit_number'],
            },
        ),
    ]
