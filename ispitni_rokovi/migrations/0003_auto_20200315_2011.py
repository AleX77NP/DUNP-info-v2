# Generated by Django 3.0.4 on 2020-03-15 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ispitni_rokovi', '0002_smer_departman'),
    ]

    operations = [
        migrations.CreateModel(
            name='IspitniRok',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('godina', models.IntegerField()),
                ('ispitni_rok', models.CharField(max_length=64)),
                ('url_slike', models.CharField(default='slika ispitnog roka', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Predmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='departman',
            name='naziv',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='smer',
            name='naziv',
            field=models.CharField(max_length=64),
        ),
        migrations.CreateModel(
            name='SmerPredmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv_predmeta', models.CharField(max_length=255)),
                ('id_predmeta', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ispitni_rokovi.Predmet')),
                ('id_smera', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ispitni_rokovi.Smer')),
            ],
        ),
    ]
