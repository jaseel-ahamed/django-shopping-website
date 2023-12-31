# Generated by Django 4.2.5 on 2023-09-29 05:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0029_order_delete_checkout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="deliv_status",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="deliv_type",
            field=models.CharField(default="cod", max_length=255),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.IntegerField(default=0),
        ),
    ]
