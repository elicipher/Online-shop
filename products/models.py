from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey("self",on_delete=models.CASCADE, null=True,blank=True,related_name="scategory")
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 , unique=True)

    class Meta :
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:categoty_url",args=[self.slug ,])

from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'   

class Product(models.Model):

    category = models.ManyToManyField(Category , related_name="p_category")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200 , unique= True)
    imge = models.ImageField(storage=MediaStorage(),upload_to='product/%Y/%m/%d')#نمایش سال و ماه و روزی که عکس آپلود شده
    description = models.TextField()
    price = models.IntegerField()
    availble = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ('name',)
       

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:product_detail' , args=[self.slug ,])