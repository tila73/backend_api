# Generated by Django 4.1.5 on 2023-04-17 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_order_address_order_total_cost_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
