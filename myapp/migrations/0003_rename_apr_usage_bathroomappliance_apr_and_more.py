# Generated by Django 5.0.3 on 2024-03-23 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_bathroomappliance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='apr_usage',
            new_name='apr',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='aug_usage',
            new_name='aug',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='dec_usage',
            new_name='dec',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='feb_usage',
            new_name='feb',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='jan_usage',
            new_name='jan',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='jul_usage',
            new_name='jul',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='jun_usage',
            new_name='jun',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='mar_usage',
            new_name='mar',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='may_usage',
            new_name='may',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='nov_usage',
            new_name='nov',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='oct_usage',
            new_name='oct',
        ),
        migrations.RenameField(
            model_name='bathroomappliance',
            old_name='sep_usage',
            new_name='sep',
        ),
    ]
