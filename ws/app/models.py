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

