# Generated by Django 5.1.9 on 2025-05-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_dietaryoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dietary_options',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.dietaryoption'),
        ),
    ]
