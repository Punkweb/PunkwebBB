# Generated by Django 4.2.4 on 2023-08-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punkweb_bb', '0005_alter_category_slug_alter_subcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='board/profiles'),
        ),
    ]
