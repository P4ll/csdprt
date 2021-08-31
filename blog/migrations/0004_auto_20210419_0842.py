# Generated by Django 3.2 on 2021-04-19 08:42

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type_post_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.typepost', verbose_name='Тип статьи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=tinymce.models.HTMLField(default=''),
            preserve_default=False,
        ),
    ]