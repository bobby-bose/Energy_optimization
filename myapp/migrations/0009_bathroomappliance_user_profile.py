# Generated by Django 5.0.3 on 2024-03-24 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_dininghallappliance_dininghall_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bathroomappliance',
            name='user_profile',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile'),
        ),
    ]
