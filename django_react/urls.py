from django.contrib import admin
from django.urls import include, path
from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('items.urls'))
]