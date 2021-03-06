# Generated by Django 4.0.4 on 2022-04-13 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='authorized_alarm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='authorized_enter',
            field=models.CharField(default='anytime', max_length=20),
        ),
        migrations.AddField(
            model_name='request',
            name='authorized_enter_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='authorized_enter_start',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='authorized_pet',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='request_type',
            field=models.CharField(default='non resident', max_length=35),
        ),
        migrations.AddField(
            model_name='request',
            name='special_instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_added_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField(blank=True, null=True)),
                ('date_in', models.DateField(blank=True, null=True)),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('status', models.CharField(default='not started', max_length=35)),
                ('random_maintenance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('action_notes', models.TextField(blank=True, null=True)),
                ('action_title', models.TextField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_added_by', to=settings.AUTH_USER_MODEL)),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.request')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='requests')),
                ('video', models.URLField(blank=True, null=True)),
                ('random_maintenance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=35, null=True)),
                ('category', models.CharField(blank=True, max_length=35, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_added_by', to=settings.AUTH_USER_MODEL)),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.request')),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_type', models.CharField(default='materials', max_length=35)),
                ('cost_name', models.CharField(blank=True, max_length=35, null=True)),
                ('random_maintenance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('cost_number', models.IntegerField(default=1)),
                ('cost_description', models.TextField(blank=True, null=True)),
                ('cost_total', models.IntegerField()),
                ('paid', models.CharField(default='not paid', max_length=10)),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('paid_by', models.CharField(default='us', max_length=10)),
                ('ref_no', models.CharField(blank=True, max_length=45, null=True)),
                ('paid_through', models.CharField(default='cash', max_length=25)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cost_added_by', to=settings.AUTH_USER_MODEL)),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.request')),
            ],
        ),
    ]
