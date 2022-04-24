# Generated by Django 4.0.4 on 2022-04-15 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_alter_unit_unit_designation_alter_unit_unit_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='city',
            field=models.CharField(default='Nairobi', max_length=50),
        ),
        migrations.AddField(
            model_name='unit',
            name='country',
            field=models.CharField(default='Kenya', max_length=50),
        ),
        migrations.AddField(
            model_name='unit',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='zip',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]