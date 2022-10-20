from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='наименование категории')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='SLUG')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='наименование товара')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='SLUG')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='фото')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    stock = models.PositiveIntegerField(verbose_name='запас')
    available = models.BooleanField(default=True, verbose_name='доступный')
    created = models.DateTimeField(auto_now_add=True, verbose_name=' дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name