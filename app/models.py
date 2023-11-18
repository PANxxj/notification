from django.db import models
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import datetime
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail 

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, unique=True)
    first_name = models.CharField(max_length=50,null=True, verbose_name="First Name ")
    last_name = models.CharField(max_length=50, null=True, verbose_name="Last Name ")
    date_joined = models.DateTimeField(default=datetime.datetime.now)
    phone_number = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Phone Number ", help_text="Optional")
    address = models.CharField(max_length=150,null=True, blank=True, verbose_name="Address")
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Country")
    city = models.CharField(max_length=150,null=True, blank=True, verbose_name="City")
    state = models.CharField(max_length=150,null=True, blank=True, verbose_name="State")
    profile_image = models.FileField(default="",upload_to="profile image",null=True,blank=True, verbose_name="Profile Image")
    # user_type = models.CharField(max_length=30, choices=USER_TYPES, null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # company = models.ForeignKey(CompanyRegistration, models.CASCADE, null=True, blank=True)
    otp = models.IntegerField(blank=True,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "All Users"
        verbose_name_plural = "All Users"

    def __str__(self):
        return f"{self.email}"    
    

class MultiToken(Token):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_token',
            on_delete=models.CASCADE, verbose_name=_("User"))
    
