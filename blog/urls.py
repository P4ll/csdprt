from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name='blog'

urlpatterns = [
	path('news', NewsListView.as_view(), name='news'),
	path('news/admin', NewsAdminListView.as_view(), name='news_admin'),
	path('news/create', NewsCreateView.as_view(), name='news_create'),
	path('news/<int:id>', NewsDetailView.as_view(), name='news_detail'),
	path('news/<int:pk>/update', NewsUpdateView.as_view(), name='news_update'),
	path('news/<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
	path('news/search', csrf_exempt(search_news), name='news_search'),

	path('news/<int:id>/comment', CommentView.as_view(), name='comment'),
	path('news/<int:id>/comment/<int:pk>', CommentDeleteView.as_view(), name='comment_delete'),

	path('tag/<int:id>', TagsListView.as_view(), name='tag_detail'),

	path('article/admin', ArticleAdminListView.as_view(), name='article_admin'),
	path('article/create', ArticleCreateView.as_view(), name='article_create'),
	path('article/<int:id>', ArticleDetailView.as_view(), name='article_detail'),
	path('article/<int:pk>/update', ArticleUpdateView.as_view(), name='article_update'),
	path('article/<int:pk>/delete', ArticleDeleteView.as_view(), name='article_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)