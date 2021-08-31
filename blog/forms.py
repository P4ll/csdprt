from datetime import date

from django import forms
from django.utils.safestring import mark_safe

from blog.models import Comment, Post, TypePost
from captcha.fields import CaptchaField

from blog.services import get_change_color_text


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        try:
            img_html = mark_safe(f'<br><img src="{value.url}"/><br><br>')
            return f'{img_html}{input_html}'
        except:

            return f'{input_html}'


class PostForm(forms.ModelForm):

    def save(self, commit=True):
        post = super().save(commit=False)
        post.date = date.today()
        post.type_post_id = TypePost.objects.get(title='Новость')
        if commit:
            title = self.cleaned_data['title']
            text = self.cleaned_data['text']
            post.text = get_change_color_text(title, text)
            post.save()
            self.save_m2m()

        return post

    class Meta:
        model = Post
        fields = ['title', 'thumbnail', 'description', 'text', 'tag_id', 'author_id']
        exclude = ('author_id',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'thumbnail': ImagePreviewWidget(),
        }


class ArticleForm(forms.ModelForm):

    def save(self, commit=True):
        post = super().save(commit=False)
        post.date = date.today()
        post.type_post_id = TypePost.objects.get(title='Статья')
        if commit:

            post.save()
            self.save_m2m()

        return post

    class Meta:
        model = Post
        fields = ['title', 'thumbnail', 'text', 'tag_id', 'author_id']
        exclude = ('author_id',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'thumbnail': ImagePreviewWidget(),
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите код с картинки')

    def save(self, commit=True):
        post = super().save(commit=False)
        post.date = date.today()
        post.type_post_id = TypePost.objects.get(title='Новость')
        if commit:
            post.save()

        return post

    class Meta:
        model = Comment
        fields = ['body', 'author_id']
        exclude = ('author_id',)
        widgets = {
            'body': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
