# Generated by Django 5.1.9 on 2025-06-17 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_socialmedialink'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialmedialink',
            options={'verbose_name': 'Social Media Link', 'verbose_name_plural': 'Social Media Links'},
        ),
        migrations.RemoveField(
            model_name='socialmedialink',
            name='name',
        ),
    ]
