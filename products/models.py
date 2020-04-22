import random
import os
from django.db import models
from django.db.models.signals import pre_save,post_save
from Med_store.utils import unique_slug_generator
from django.urls import reverse
# Create your models here.
# image
def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance,filename):
    new_filename=random.randint(1,31364892494903)
    name,ext=get_filename_ext(filename)
    final_filename='{new_filename}{exit}'.format(new_filename=new_filename,ext=ext)

    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename,
       final_filename=final_filename)
class ProductManager(models.Manager):
    def get_by_id(self,id,pk):
        qs=self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None





class Category(models.Model):
    title=models.CharField(max_length=120)
    slug=models.SlugField(blank=True,unique=True)
    description=models.TextField()
    featured=models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.title
class Product(models.Model):
    category=models.ManyToManyField("Category",null=True,blank=True)
    title=models.CharField(max_length=120)
    slug=models.SlugField(blank=True,unique=True)
    description=models.TextField()
    # quantity = models.IntegerField(default=1)
    price=models.DecimalField(decimal_places=2,max_digits=20)
    image=models.ImageField(upload_to='OHM/',null=True,blank=True)
    featured=models.BooleanField(default=False)
    objects=ProductManager()
    def __str__(self):
        return self.title
        # url
    def get_absolute_url(self):
        # return '/products/{slug}/'.format(slug=self.slug)
        return reverse('products:detail', kwargs={"slug": self.slug})
''' a signal that generate unique slug'''
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect( product_pre_save_receiver, sender=Product)

def category_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect( category_pre_save_receiver, sender=Category)