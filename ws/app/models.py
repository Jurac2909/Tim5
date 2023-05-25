from django.db import models
from django.contrib.auth.models import User
CATEGORY_CHOICES=(
    ('CI', 'Čišćenje'),
    ('LO', 'Losioni'),
    ('MA', 'Maske'),
    ('IS', 'Izvorni Serumi'),
    ('CS', 'Ciljani Serumi'),
    ('KR', 'Kreme'),
    ('ZS', 'Završni Serumi'),
    ('KP', 'Kemijski Pilinzi'),
    ('GP', 'GreenPeel'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price =models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    def __str__(self):
        return self.name
    
STATUS_CHOICES= (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


