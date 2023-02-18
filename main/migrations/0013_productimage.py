# Generated by Django 4.1.5 on 2023-02-04 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='main.product')),
            ],
        ),
    ]
