from django.db import models


class Users(models.Model):
    userid=models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    phone = models.CharField('phone', max_length=10)
    tempphone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    tempmail = models.CharField(max_length=50)
    status = models.CharField(max_length=25, default='Inactive')
    password = models.CharField(max_length=15)

    
class Address(models.Model):
    addressid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    hname = models.CharField(max_length=25)
    hno = models.CharField(max_length=25)
    street = models.CharField(max_length=15)
    pincode = models.CharField(max_length=25)
    district = models.CharField(max_length=15)
    state = models.CharField(max_length=10)
    

class admin(models.Model):
    adminid=models.AutoField(primary_key=True)
    mail = models.CharField(max_length=50)
    password = models.CharField(max_length=15)

class category(models.Model):
    categoryid=models.AutoField(primary_key=True)
    cname=models.CharField(max_length=25)
    offer = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.cname   

class product(models.Model):
    productid=models.AutoField(primary_key=True)
    pname=models.CharField(max_length=100)
    price=models.FloatField(max_length=10)
    cid = models.ForeignKey(category, on_delete=models.CASCADE, null=False)
    stock=models.CharField(max_length=30)
    author=models.CharField(max_length=50)
    publisher=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField('image',upload_to='products')
    offer = models.PositiveIntegerField(default=0)
    offerprice  = models.PositiveIntegerField(default=0)

class cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    total = models.CharField(max_length=100,default=0)

class cart_list(models.Model):
    cartlistid = models.AutoField(primary_key=True)
    ctid = models.ForeignKey(cart, on_delete=models.CASCADE, null=False)
    pid = models.ForeignKey(product, on_delete=models.CASCADE, null=False)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.CharField(max_length=100)

class orders(models.Model):
    orderid = models.AutoField(primary_key=True)   
    aid = models.ForeignKey(Address, on_delete=models.CASCADE, null=False)
    amount = models.FloatField(max_length=10)
    # order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order_id = models.CharField(max_length=25)

class payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    oid = models.ForeignKey(orders, on_delete=models.CASCADE, null=False)
    mode = models.CharField(max_length=10, default= 'COD')
    status = models.CharField(max_length=12, default='Pending')


class order_list(models.Model):
    orderlistid = models.AutoField(primary_key=True)
    oid = models.ForeignKey(orders, on_delete=models.CASCADE,null=False)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    pid = models.ForeignKey(product, on_delete=models.CASCADE, null=False)
    order_lid = models.CharField(max_length=10)
    quantity = models.CharField(max_length=100)
    total_price = models.CharField(max_length=100)
    status = models.CharField(max_length=25, default = 'Pending')
    cancel = models.BooleanField(default=False)
    return_order = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)




class banner(models.Model):
    bannerid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image=models.ImageField('image',upload_to='banners')

class coupon(models.Model):
    couponid = models.AutoField(primary_key=True)
    coupname = models.CharField(max_length=10)
    price = models.CharField(max_length=100)
