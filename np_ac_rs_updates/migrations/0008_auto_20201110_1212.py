# Generated by Django 3.1.2 on 2020-11-10 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('np_ac_rs_updates', '0007_auto_20201109_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='departmani',
            new_name='smerovi_departmani',
        ),
        migrations.RemoveField(
            model_name='student',
            name='smerovi',
        ),
    ]
