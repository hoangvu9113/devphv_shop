from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class Category(models.Model):
    category_parent_id = models.IntegerField(null=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    image = models.TextField()
    detail = models.TextField()
    detail_features = models.TextField(null=True)
    status = models.NullBooleanField()
    digital = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'Product'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_path = models.TextField()
    image_detail = models.TextField(null=True)
    image_features = models.TextField(null=True)
    image_small = models.TextField(null=True)

    class Meta:
        db_table = 'ProductImage'


class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.TextField()

    class Meta:
        db_table = 'Promotion'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Order'

    @property
    def shipping(self):
        shipping = False
        orderdetails = self.orderdetail_set.all()
        for i in orderdetails:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderdetails = self.orderdetail_set.all()
        total = sum([item.get_total for item in orderdetails])
        return total

    @property
    def get_cart_detail(self):
        orderdetails = self.orderdetail_set.all()
        total = sum([item.quantity for item in orderdetails])
        return total


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'OrderDetail'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.address
