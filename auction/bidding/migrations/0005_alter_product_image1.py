# Generated by Django 4.1 on 2022-08-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0004_alter_product_image1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
