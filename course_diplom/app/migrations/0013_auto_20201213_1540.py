# Generated by Django 3.1.4 on 2020-12-13 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20201213_0257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameter',
            options={'ordering': ('name',), 'verbose_name': 'Имя параметра', 'verbose_name_plural': 'Список всех параметров'},
        ),
    ]
