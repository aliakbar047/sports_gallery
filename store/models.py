from django.db import models
from django.conf import settings

# Create your models here.

CATEGORY_CHOICES = (
    ('sports','SPORTS'),
    ('shoes','SHOES'),
    ('jerseys','JERSEYS'),
    ('kids','KIDS'),
    ('accessories','accessories'),
)


class Product(models.Model):
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES ,default='sports')
    sub_category = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField()
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.title
        
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    complete = models.BooleanField(default=False)
    total = models.FloatField(null=True, blank=True)
    

    
    def __str__(self):
        return self.product.title


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    order_items = models.ManyToManyField(OrderItem)
    total_items = models.IntegerField(null=True)
    total = models.FloatField(null=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    transaction_complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, blank=True, null=True)
    

    def __str__(self):
        return self.customer.username


class Address(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    mobile = models.IntegerField(null=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    save_for_later = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'


    def __str__(self):
        return self.customer.username

class WishList(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.customer.username




