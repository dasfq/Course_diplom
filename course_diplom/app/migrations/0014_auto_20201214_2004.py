# Generated by Django 3.1.4 on 2020-12-14 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20201213_1540'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='iteminfo',
            constraint=models.UniqueConstraint(fields=('item', 'shop', 'external_id'), name='unique_item_info'),
        ),
    ]
