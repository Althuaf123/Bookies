# Generated by Django 4.1.4 on 2023-02-21 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('addressid', models.AutoField(primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=25)),
                ('hno', models.CharField(max_length=25)),
                ('street', models.CharField(max_length=15)),
                ('pincode', models.CharField(max_length=25)),
                ('district', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='admin',
            fields=[
                ('adminid', models.AutoField(primary_key=True, serialize=False)),
                ('mail', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='banner',
            fields=[
                ('bannerid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='banners', verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('cartid', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.CharField(default=0, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('categoryid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=25)),
                ('offer', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='coupon',
            fields=[
                ('couponid', models.AutoField(primary_key=True, serialize=False)),
                ('coupname', models.CharField(max_length=10)),
                ('price', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(max_length=10)),
                ('order_id', models.CharField(max_length=25)),
                ('aid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.address')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=10, verbose_name='phone')),
                ('tempphone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('tempmail', models.CharField(max_length=50)),
                ('status', models.CharField(default='Inactive', max_length=25)),
                ('password', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('productid', models.AutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=100)),
                ('price', models.FloatField(max_length=10)),
                ('stock', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='products', verbose_name='image')),
                ('offer', models.PositiveIntegerField(default=0)),
                ('offerprice', models.PositiveIntegerField(default=0)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('paymentid', models.AutoField(primary_key=True, serialize=False)),
                ('mode', models.CharField(default='COD', max_length=10)),
                ('status', models.CharField(default='Pending', max_length=12)),
                ('oid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.orders')),
            ],
        ),
        migrations.CreateModel(
            name='order_list',
            fields=[
                ('orderlistid', models.AutoField(primary_key=True, serialize=False)),
                ('order_lid', models.CharField(max_length=10)),
                ('quantity', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=100)),
                ('status', models.CharField(default='Pending', max_length=25)),
                ('cancel', models.BooleanField(default=False)),
                ('return_order', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('oid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.orders')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.users')),
            ],
        ),
        migrations.CreateModel(
            name='cart_list',
            fields=[
                ('cartlistid', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('total_price', models.CharField(max_length=100)),
                ('ctid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.cart')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.users'),
        ),
        migrations.AddField(
            model_name='address',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.users'),
        ),
    ]
