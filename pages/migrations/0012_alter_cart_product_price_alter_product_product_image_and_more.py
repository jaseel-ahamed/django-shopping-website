# Generated by Django 4.1.3 on 2023-09-06 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(),
        ),
    ]