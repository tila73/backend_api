# Generated by Django 4.1.5 on 2023-02-12 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_maincategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(null=True, upload_to='sub_category_images/'),
        ),
    ]
