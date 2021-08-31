# Generated by Django 3.2.3 on 2021-05-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0004_merge_20210528_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacanciesmodel',
            name='counters',
        ),
        migrations.AddField(
            model_name='vacanciesmodel',
            name='counter',
            field=models.IntegerField(blank=True, default=0, verbose_name='Просмотрело'),
        ),
        migrations.AlterField(
            model_name='vacanciesmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]