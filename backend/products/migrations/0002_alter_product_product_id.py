# Generated by Django 4.1 on 2022-12-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(max_length=120),
        ),
    ]