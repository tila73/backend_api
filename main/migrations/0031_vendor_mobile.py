# Generated by Django 4.1.5 on 2023-04-01 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_remove_cart_customer_cart_cart_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='mobile',
            field=models.PositiveBigIntegerField(null=True, unique=True),
        ),
    ]
