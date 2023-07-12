from django.contrib import admin
from django.urls import include, path
from items import views

urlpatterns = [
    path('api/items/',  views.items_list),
    path('api/items/<int:pk>/',  views.items_detail),
]