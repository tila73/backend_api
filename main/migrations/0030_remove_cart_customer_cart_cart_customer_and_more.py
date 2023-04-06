# Generated by Django 4.1.5 on 2023-03-31 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_remove_cart_user_cart_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='customer',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='main.customer'),
        ),
        migrations.AddField(
            model_name='customer',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.cart'),
        ),
    ]
