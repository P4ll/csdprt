# Generated by Django 3.2.3 on 2021-05-28 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_resumesmodel_test_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resumesmodel',
            name='test_field',
        ),
    ]