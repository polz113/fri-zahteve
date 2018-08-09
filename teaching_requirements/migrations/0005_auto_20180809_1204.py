# Generated by Django 2.0.7 on 2018-08-09 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_requirements', '0004_auto_20180802_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='requirements',
            field=models.ManyToManyField(blank=True, to='teaching_requirements.Resource', verbose_name='Zahteve'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=256, verbose_name='naziv'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='short_name',
            field=models.CharField(max_length=32, verbose_name='kratek naziv'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(blank=True, verbose_name='opis'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(max_length=256, verbose_name='naziv'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(blank=True, max_length=16, unique=True, verbose_name='koda'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=256, verbose_name='naziv'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='short_name',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='kratek naziv'),
        ),
        migrations.AddField(
            model_name='resourcecomment',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching_requirements.Resource'),
        ),
        migrations.AddField(
            model_name='resourcecomment',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teaching_requirements.Teacher'),
        ),
    ]
