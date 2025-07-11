# Generated by Django 5.1.9 on 2025-06-13 16:49

import django.db.models.deletion
import home.models
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SvgIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.TextField(help_text='Paste full inline SVG code here.')),
            ],
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('hero_title', models.CharField(max_length=255)),
                ('hero_description', models.TextField()),
                ('hero_image_url', models.URLField(blank=True, help_text='Optional. Used only if uploaded image is not provided.')),
                ('about_sections', wagtail.fields.StreamField([('about_section', 6)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 1: ('wagtail.blocks.CharBlock', (), {}), 2: ('wagtail.blocks.TextBlock', (), {}), 3: ('wagtail.snippets.blocks.SnippetChooserBlock', (home.models.SvgIcon,), {'required': False}), 4: ('wagtail.blocks.StructBlock', [[('svg_icon', 3), ('title', 1), ('description', 2)]], {}), 5: ('wagtail.blocks.ListBlock', (4,), {'max_num': 3}), 6: ('wagtail.blocks.StructBlock', [[('image', 0), ('title', 1), ('description', 2), ('features', 5)]], {})}, verbose_name='About Sections')),
                ('gallery_title', models.CharField(max_length=255)),
                ('contact_title', models.CharField(max_length=255)),
                ('hero_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='home.homepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpeningHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('day', models.CharField(max_length=9)),
                ('hours', models.CharField(max_length=50)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='opening_hours', to='home.homepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('contact_text', models.CharField(max_length=255)),
                ('contact_type', models.CharField(choices=[('phone', 'Phone'), ('email', 'Email'), ('address', 'Address')], max_length=10)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_methods', to='home.homepage')),
                ('svg_icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.svgicon')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
