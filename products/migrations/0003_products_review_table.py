# Generated by Django 4.1.4 on 2022-12-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_products_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='review_table',
            field=models.BooleanField(default=True),
        ),
    ]
