# Generated by Django 3.1.2 on 2020-10-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('np_ac_rs_updates', '0005_student_lozinka'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='uredjaj',
            new_name='fcm_token',
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
