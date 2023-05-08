from django.db import models
from django.contrib.auth.models import User

class company_details(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    contact_number = models.CharField(max_length=100,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.CharField(max_length = 100,null=True,blank=True)
    company_email = models.CharField(max_length=255,null=True,blank=True)
    business_name = models.CharField(max_length=255,null=True,blank=True)
    company_type = models.CharField(max_length=255,null=True,blank=True)
    industry_type = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/profile')

