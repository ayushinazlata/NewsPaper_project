# Generated by Django 5.1.6 on 2025-05-01 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_category_name_category_alter_post_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication',
            field=models.CharField(choices=[('NW', 'News'), ('AR', 'Article')], default='NW', max_length=2),
        ),
    ]
