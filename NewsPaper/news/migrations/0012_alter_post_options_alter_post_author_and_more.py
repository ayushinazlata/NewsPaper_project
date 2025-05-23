# Generated by Django 5.1.6 on 2025-05-02 11:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_postcategory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(help_text='Author of publication', on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of creation'),
        ),
        migrations.AlterField(
            model_name='post',
            name='publication',
            field=models.CharField(choices=[('NW', 'News'), ('AR', 'Article')], default='NW', max_length=2, verbose_name='Publication'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.SmallIntegerField(default=0, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_en',
            field=models.TextField(null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_en',
            field=models.CharField(max_length=256, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=256, null=True, verbose_name='Title'),
        ),
    ]
