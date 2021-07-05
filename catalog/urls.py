from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('address/', ProductListView.as_view(), name='api'),
    path('', index, name='index'),
]