# Generated by Django 4.0.4 on 2022-04-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_rename_unit_name_unit_property_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='added_through',
            field=models.CharField(default='manual', max_length=10),
        ),
    ]
