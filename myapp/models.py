from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    
    mobile_number = models.CharField(max_length=20)
    
   
    district = models.CharField(max_length=100)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class BathroomAppliance(models.Model):
    
    bathroom_name=models.CharField(max_length=100)
    appliance_name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text='Wattage in Watts')
    quantity = models.IntegerField(default=1)
    

    # Usage for each month
    jan = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feb = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mar = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    apr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    may = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jun = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jul = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    aug = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sep = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    nov = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dec = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.appliance_name
    
class KitchenAppliance(models.Model):
    kitchen_name=models.CharField(max_length=100,default='')
    appliance_name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text='Wattage in Watts')
    quantity = models.IntegerField(default=1)
   
    
    jan = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feb = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mar = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    apr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    may = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jun = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jul = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    aug = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sep = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    nov= models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dec = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.appliance_name
    
class BedroomAppliance(models.Model):
    bedroom_name=models.CharField(max_length=100)
    appliance_name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text='Wattage in Watts')
    quantity = models.IntegerField(default=1)
   

    jan = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feb = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mar = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    apr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    may = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jun = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jul = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    aug = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sep = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    nov= models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dec = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.appliance_name
    
class DininghallAppliance(models.Model):
    dininghall_name=models.CharField(max_length=100,default='')
    appliance_name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text='Wattage in Watts')
    quantity = models.IntegerField(default=1)
   
   
    jan = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feb = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mar = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    apr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    may = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jun = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jul = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    aug = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sep = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    nov= models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dec = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.appliance_name
    
class LivingroomAppliance(models.Model):
    livingroom_name=models.CharField(max_length=100,default='')
    
    appliance_name = models.CharField(max_length=100)
    wattage = models.IntegerField(help_text='Wattage in Watts')
    quantity = models.IntegerField(default=1)
   
    
    jan = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    feb = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    mar = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    apr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    may = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jun = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    jul = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    aug = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    sep = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    nov= models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dec = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.appliance_name