# Generated by Django 2.0.5 on 2018-05-23 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0005_auto_20180521_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='choices',
        ),
        migrations.AddField(
            model_name='question',
            name='choice1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='choice2',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='choice3',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='difficulty',
            field=models.CharField(choices=[('d', 'Difficult'), ('s', 'Simple')], max_length=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='objective',
            field=models.CharField(choices=[('r', 'Reminding'), ('u', 'Understanding'), ('c', 'Creativity')], max_length=1),
        ),
    ]