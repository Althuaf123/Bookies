# Generated by Django 4.1.4 on 2023-02-22 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_order_list_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_list',
            name='pay',
        ),
    ]
