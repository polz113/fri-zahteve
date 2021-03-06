# Generated by Django 2.0.7 on 2018-08-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching_requirements', '0003_auto_20180729_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='code',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='activity',
            name='lecture_type',
            field=models.CharField(choices=[('P', 'Predavanja'), ('LV', 'Laboratorijske vaje'), ('AV', 'Avditorne vaje')], max_length=16),
        ),
        migrations.AlterField(
            model_name='provides',
            name='n',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
