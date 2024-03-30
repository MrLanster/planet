from django.db import models
import hashlib
import random
import string

class User(models.Model):
    uid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
    email_verified = models.BooleanField(default=False)  
    profile = models.CharField(max_length=100, default='none.png',null=True)
    additional_params = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    


class Verify_Email(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def generate_unique_hash(self):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        unique_hash = hashlib.sha256((self.email + random_string).encode()).hexdigest()
        self.hash = unique_hash
        self.save()

    def __str__(self):
        return self.email
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def add_item(self,filename):
        CartItem.objects.get_or_create(cart=self, filename=filename)

    def remove_item(self, item_name):
        self.cartitem_set.filter(item=item_name).delete()

    def get_quantity(self, item_name):
        item = self.cartitem_set.filter(item=item_name).first()
        return item.quantity if item else 0



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.quantity} x {self.item} in cart for {self.cart.user.username}"