# Generated by Django 3.2.3 on 2021-05-28 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumesmodel',
            name='test_field',
            field=models.IntegerField(default=0),
        ),
    ]
