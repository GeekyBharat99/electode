# Generated by Django 2.2.4 on 2019-11-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20191126_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_img',
            field=models.ImageField(blank=True, upload_to='productimage'),
        ),
    ]
