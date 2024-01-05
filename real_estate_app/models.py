from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class BaseModel(models.Model):
    """
    Base model class to inherit on other model's for avoiding multiple usage
    """
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserDetails(BaseModel):
    """
    This master table contains the details of user
    """
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    address = models.TextField(blank=False)
    choices = [('ADM', 'Admin'), ('TNT', 'Tenant')]
    user_type = models.CharField(max_length=20, choices=choices, default='TNT')
    password = models.CharField(max_length=200, default='')
    file = models.FileField(upload_to='uploads/')


class Property(BaseModel):
    """
    This master table contains the informations about property
    """
    property_name = models.CharField(max_length=150)
    address = models.TextField()
    location = models.CharField(max_length=150)
    features = models.CharField(max_length=200)


class Unit(BaseModel):
    """
    This table contains the details about the property units
    """
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = [('1BHK', '1BHK'), ('2BHK', '2BHK'), ('3BHK', '3BHK'), ('4BHK', '4BHK')]
    unit_type = models.CharField(max_length=4, choices=type_choices)
    tenant = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()

