from django.db import models

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

