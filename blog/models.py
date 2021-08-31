from ckeditor.fields import RichTextField
from django.db import models

from accounts.models import AdvUser


# Тип статьи
class TypePost(models.Model):
    name = models.CharField(max_length=20, verbose_name='Человечиские url')
    title = models.CharField(max_length=20, verbose_name='Тип')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Тип статьи'
        verbose_name_plural = 'Типы статей'
        ordering = ['title']


# Тег
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тег')
    date = models.DateField(verbose_name='Дата')
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    author_id = models.ForeignKey(AdvUser, null=True, on_delete=models.CASCADE, verbose_name='Aвтор')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


# Статья
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.CharField(max_length=255, verbose_name='Описание')
    text = RichTextField(blank=True, null=True, verbose_name='Текст материала')
    date = models.DateField(verbose_name='Дата')
    thumbnail = models.ImageField(verbose_name='Изображение', blank=True, null=True,)

    tag_id = models.ManyToManyField(Tag, verbose_name='Теги')
    author_id = models.ForeignKey(AdvUser, null=True, on_delete=models.CASCADE, verbose_name='Aвтор')
    type_post_id = models.ForeignKey(TypePost, null=True, on_delete=models.CASCADE, verbose_name='Тип материала')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['title']


# Комментарий
class Comment(models.Model):
    body = models.CharField(max_length=255, verbose_name='Комментарий')
    date = models.DateField(verbose_name='Дата')

    author_id = models.ForeignKey(AdvUser, null=True, on_delete=models.CASCADE, verbose_name='Aвтор')
    post_id = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, verbose_name='Статья')

    def __str__(self):
        return f'{self.post_id.title} {self.author_id.last_name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date']


