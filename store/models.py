from django.db import models
from django.db.models.fields import CharField
import datetime


# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    category=models.ForeignKey("store.Category",on_delete=models.CASCADE,default=1)
    description=models.CharField( max_length=200)
    image=models.ImageField(upload_to='uploads/products/')


    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)


    @staticmethod
    def get_all_product():
        return Product.objects.all()


    @staticmethod
    def get_all_product_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)

        else:
            return Product.get_all_product()
        

class Category(models.Model):
    name=models.CharField( max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    phone= models.CharField(max_length=15)
    email= models.EmailField()
    password=models.CharField(max_length=500)


    def Register(self):
        self.save()
    
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

            
    
    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField( max_length=500,default="",blank=True)
    phone=models.CharField( max_length=50,default="",blank=True)
    date=models.DateField(default= datetime.datetime.today)
    status=models.BooleanField(default=False)

    def placeorder(self):
        self.save()


    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    

    
    







    


