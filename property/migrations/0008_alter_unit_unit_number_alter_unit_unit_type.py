# Generated by Django 4.0.4 on 2022-04-16 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_alter_unit_city_alter_unit_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=35),
            preserve_default=False,
        ),
    ]
