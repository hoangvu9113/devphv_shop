# Generated by Django 3.1.2 on 2020-12-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20201220_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
