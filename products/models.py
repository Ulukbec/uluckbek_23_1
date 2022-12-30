from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')

    def __str__(self):
        return self.title


class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    image = models.ImageField(blank=True, verbose_name='Фото')
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    created_date = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField(verbose_name="Цена")
    category = models.ManyToManyField(Category, verbose_name="Категории")
    review_table = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='review')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
