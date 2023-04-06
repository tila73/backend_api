# Generated by Django 4.1.5 on 2023-04-01 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_vendor_mobile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeraddress',
            name='address',
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='province',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='street_address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='zip',
            field=models.IntegerField(null=True),
        ),
    ]
