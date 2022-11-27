from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class Category(models.Model):
    category_name = models.CharField(max_length=200, db_index=True, verbose_name='наименование категории')
    category_slug = AutoSlugField(populate_from='category_name', verbose_name='SLUG', unique=True, blank=True, default=None)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.category_slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='категория', blank=True, null=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name='наименование товара')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='SLUG')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='фото')
    description = models.TextField(blank=True, verbose_name='описание', null=True)
    price = models.CharField(max_length=200, db_index=True, verbose_name='цена', blank=True, null=True)
    stock = models.PositiveIntegerField(verbose_name='запас', blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name='доступный', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=' дата создания', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])