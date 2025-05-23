# Generated by Django 5.1.6 on 2025-05-02 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_alter_post_options_alter_post_author_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Publication', 'verbose_name_plural': 'Publications'},
        ),
        migrations.AlterField(
            model_name='post',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of publication'),
        ),
    ]
