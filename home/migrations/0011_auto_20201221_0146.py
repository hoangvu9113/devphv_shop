# Generated by Django 3.1.2 on 2020-12-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_shippingaddress_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
