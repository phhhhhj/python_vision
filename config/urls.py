from django.contrib import admin
from django.urls import path

from today.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', select_rand, name='random5'),
    path('save/<id>', click_style, name='style_list'),
]
