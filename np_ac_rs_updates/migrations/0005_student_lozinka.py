# Generated by Django 3.1.2 on 2020-10-26 17:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('np_ac_rs_updates', '0004_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='lozinka',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]