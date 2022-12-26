from django.db import models


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Products(models.Model):
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField()
    category = models.ManyToManyField(Category)
    review_table = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, related_name='review')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
