import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, View

from blog.forms import ArticleForm, CommentForm, PostForm
from blog.models import Comment, Post, Tag
from blog.services import get_userprofile


class NewsListView(View):
    """Список новостей"""
    def get(self, request):
        news = Post.objects.filter(type_post_id__title="Новость").order_by('-id')
        page_number = request.GET.get('page', 1)
        paginator = Paginator(news, 3)
        page = paginator.get_page(page_number)
        tags = Tag.objects.all()
        return render(request, 'blog/news/news.html', {'news': page, 'page': page, 'tags': tags})


def search_news(request):
    """Поиск новостей"""
    if request.method == 'POST':
        search_body = json.loads(request.body).get('searchQuery')
        posts = Post.objects.filter(type_post_id__title="Новость").filter(title__icontains=search_body) | \
                   Post.objects.filter(type_post_id__title="Новость").filter(text__icontains=search_body)
        data = posts.values()
        return JsonResponse(list(data), safe=False)


class TagsListView(View):
    """Список новостей и статьей по тегу"""

    def get(self, request, id):
        tag = Tag.objects.get(id=id)
        posts = Post.objects.filter(tag_id=id)
        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts, 3)
        page = paginator.get_page(page_number)
        tags = Tag.objects.exclude(id=id)
        return render(request, 'blog/tag/list.html', {'tag': tag, 'posts': page, 'page': page, 'tags': tags})


class NewsDetailView(View):
    """Подробнеая информация о новости"""

    def get(self, request, id):
        news = Post.objects.get(id=id)
        comments = Comment.objects.filter(post_id=news)
        form = CommentForm
        return render(request, 'blog/news/detail.html', {'news': news, 'form': form, 'comments': comments})


class CommentView(LoginRequiredMixin, View):
    def get(self, request, id):
        """Список комментарией к новости"""
        news = Post.objects.get(id=id)
        comments = Comment.objects.filter(post_id=news)
        return render(request, 'blog/news/admin/comments/list.html', {'comments': comments, 'news': news})

    def post(self, request, id):
        """Добавление комменатирия к новости"""
        news = Post.objects.get(id=id)
        comment = Comment(author_id=request.user, post_id=news)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:news_detail', id)
        else:
            news = Post.objects.get(id=id)
            comments = Comment.objects.filter(post_id=news)
            error = form.errors
            try:
                if error['captcha'][0] == 'Неверный ответ':
                    error = 'Неверно введены символы с картинки'
            except: pass
            form = CommentForm(request.POST, instance=comment)

            return render(request, 'blog/news/detail.html', {'news': news, 'form': form, 'error': error,
                                                             'comments': comments})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление комментария"""
    model = Comment
    template_name = 'blog/news/admin/comments/delete.html'
    success_url = reverse_lazy('blog:news_admin')


class NewsAdminListView(LoginRequiredMixin, View):
    """Список новостей пользователя"""
    def get(self, request):
        user = get_userprofile(request)
        if user.is_superuser:
            posts = Post.objects.filter(type_post_id__title='Новость').annotate(comments=Count('comment'))
        else:
            posts = Post.objects.filter(author_id=user, type_post_id__title='Новость').annotate(
                comments=Count('comment'))
        return render(request, 'blog/news/admin/admin_list.html', {'posts': posts})


class NewsCreateView(LoginRequiredMixin, View):
    """Создание новости"""

    def get(self, request):
        form = PostForm
        return render(request, 'blog/news/admin/create.html', {'form': form, 'error': None})

    def post(self, request):
        post = Post(author_id=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:news_admin')
        else:
            error = form.errors
            return render(request, 'blog/news/admin/create.html', {'form': form, 'error': error})


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление новости"""
    model = Post
    template_name = 'blog/news/admin/update.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:news_admin')
    success_message = 'Новость обновлена'


class NewsDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление новости"""
    model = Post
    template_name = 'blog/news/admin/delete.html'
    success_url = reverse_lazy('blog:news_admin')


class ArticleAdminListView(LoginRequiredMixin, View):
    """Список статей пользователя"""
    def get(self, request):
        user = get_userprofile(request)
        if user.is_superuser:
            posts = Post.objects.filter(type_post_id__title='Статья')
        else:
            posts = Post.objects.filter(author_id=user, type_post_id__title='Статья')
        return render(request, 'blog/articles/admin/list.html', {'posts': posts})


class ArticleCreateView(LoginRequiredMixin, View):
    """Создание статьи"""

    def get(self, request):
        form = ArticleForm
        return render(request, 'blog/articles/admin/create.html', {'form': form, 'error': None})

    def post(self, request):
        post = Post(author_id=request.user)
        form = ArticleForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:article_admin')
        else:
            error = form.errors
            return render(request, 'blog/articles/admin/create.html', {'form': form, 'error': error})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление статьи"""
    model = Post
    template_name = 'blog/articles/admin/update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('blog:article_admin')
    success_message = 'Статья обновлена'


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статьи"""
    model = Post
    template_name = 'blog/articles/admin/delete.html'
    success_url = reverse_lazy('blog:article_admin')


class ArticleDetailView(View):
    """Просмотр подробной информации о статье"""
    def get(self, request, id):
        post = Post.objects.get(id=id)
        return render(request, 'blog/articles/detail.html', {'post': post})
