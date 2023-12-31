from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
# Create your models here.

def upload_to(instance, filename):
        return 'images/{filename}'.format(filename=filename)

class Items(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField()
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to=upload_to, verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    available = models.BooleanField(default=True, verbose_name='Доступен ли товар')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('title', kwargs={'title_slug': self.slug})

    class Meta:
        verbose_name = 'Список товаров'
        verbose_name_plural = 'Список товаров'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']