# Generated by Django 3.2 on 2021-04-18 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20210324_1215'),
        ('blog', '0002_alter_post_tag_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=255, verbose_name='Комментарий')),
                ('date', models.DateField(verbose_name='Дата')),
                ('author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.person', verbose_name='Aвтор')),
                ('post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Статья')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['date'],
            },
        ),
    ]