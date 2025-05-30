# Generated by Django 5.1.8 on 2025-04-30 10:12

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='body',
        ),
        migrations.AddField(
            model_name='homepage',
            name='about1_description',
            field=models.TextField(default='Test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about1_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about1_title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about2_description',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='about2_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about2_title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='contact_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepage',
            name='contact_title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='gallery_title',
            field=models.CharField(default='1', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_description',
            field=models.TextField(default='djbjdhhdk'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='hero_title',
            field=models.CharField(default='dbjdbjdk', max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AboutFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.PositiveSmallIntegerField(choices=[(1, 'First'), (2, 'Second')])),
                ('svg_icon', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='about_features', to='home.homepage')),
            ],
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('svg_icon', models.CharField(max_length=255)),
                ('contact_text', models.CharField(max_length=255)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_methods', to='home.homepage')),
            ],
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='home.homepage')),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=9)),
                ('hours', models.CharField(max_length=50)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='opening_hours', to='home.homepage')),
            ],
        ),
    ]
