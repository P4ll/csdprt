from django.urls import path

from .views import *

app_name='landings'

urlpatterns = [
	path ('', index, name='index'),
	path ('northvalley/', north_valley, name='north_valley'),
	path('enter/', enter, name='enter'),
	path('history/', history, name='history'),
	path('compschool/', compschool, name='compschool'),
]