# Generated by Django 4.1.4 on 2023-02-22 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_list',
            name='pay',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.payment'),
            preserve_default=False,
        ),
    ]