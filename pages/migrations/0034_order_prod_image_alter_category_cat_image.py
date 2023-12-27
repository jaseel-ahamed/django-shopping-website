# Generated by Django 4.2.5 on 2023-09-30 05:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0033_alter_category_cat_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="prod_image",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="cat_image",
            field=models.ImageField(null=True, upload_to="uploads"),
        ),
    ]