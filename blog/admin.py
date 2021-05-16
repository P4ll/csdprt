from django.contrib import admin

from .models import Comment, Post, Tag, TypePost


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'description', 'author_id')


@admin.register(TypePost)
class TypePostAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'date', 'author_id', 'thumbnail')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('date', 'body', 'post_id', 'author_id')
