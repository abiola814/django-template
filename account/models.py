from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class for overiding default User and Admin settings is imported. ##
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.conf import settings
import uuid
from datetime import datetime
from django.utils import timezone
import json
from PIL import Image
from io import BytesIO
from django.db import transaction
from django.core.files import File
from django.urls import reverse
#from accounts.tasks import failed_identification_email
from typing import List, Tuple, Literal
# Create your models here.

AUTH_PROVIDERS: dict[str, str] = {'facebook':'facebook','google':'google','email':'email'}

POINT_CATEGORIES: tuple[tuple[str, str], ...] = (
    ("Signup","Signup"),
    ("KYC level 2","KYC level 2"),
    ("Bank details","Bank details"),
    ("Referral system","Referral system"),
    ("Gamifi savings","Gamifi savings"),
    ("Monie investment","Monie investment"),
    ("KYC level 3","KYC level 3"),
    ("Quiz Performance","Quiz Performance"),
    ("Jackpot savings","Jackpot savings")
)
CONVERSION_RATE: int = 10
POINT_ACTIVITY: tuple[tuple[str, str], ...] = (
    ("Earned tokens","Earned tokens"),
    ("Converted tokens","Converted tokens"),
    ("Bargained tokens","Bargained tokens")
)

IDENTIFIER: tuple[tuple[str, str],...] = (
    ("National ID","National ID"),
    ("Driver's License","Driver's License"),
    ("International Passport", "International Passport")
)

STATUS: tuple[tuple[str, str],...] = (
    ("Not processed","Not processed"),
    ("Processing","Processing"),
    ("Verified","Verified"),
    ("Invalid","Invalid")
)

CURRENCIES: dict[str, str] = {
    "nigerian naira":"NGN",
    "united state dollar":"USD",
    
}



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USERNAME_FIELD: str = 'email'
    email = models.EmailField(_('email_address'),blank = False,unique = True, null = True, max_length = 45)
    # wallet_id = models.CharField(max_length = 12, unique = True, blank = False, default = None )
    objects = UserManager()
    username = None
    # recommended_by = models.ForeignKey('UserReferrer', null = True, blank = True, on_delete=models.SET_NULL)
    referral_code = models.CharField(max_length = 12, blank = True, default = None, null = True, unique = False)
    first_name = models.CharField(max_length = 30, blank = False)
    last_name = models.CharField(max_length = 30, blank = False)
    REQUIRED_FIELDS = ['first_name','last_name']
    is_verified = models.BooleanField(null = True, blank = True,default = False)
    otp = models.CharField(null = True, blank = True, max_length = 9)
    uidb = models.UUIDField(default = uuid.uuid4, null  = True, blank = True)
    is_active = models.BooleanField(default = True)
    has_invested = models.BooleanField(default = False, null = True, blank = False)
    is_staff = models.BooleanField(default = False)
    t_and_c = models.BooleanField(default = False)
    auth_providers = models.CharField(default = AUTH_PROVIDERS.get('email'), null = False,max_length = 50)
    has_updated_name = models.BooleanField(default = False, null = True)
    ping_url = models.URLField(max_length = 60, default= None, null = True)
    profile_completed = models.BooleanField(default = False, null = True)
    is_subscribed = models.BooleanField(default = True, null = True)
    is_ambassador = models.BooleanField(default= False, null = True, blank = True)
    bvn = models.CharField(default = None, null = True, blank = True, max_length = 30)
    address = models.TextField(default = None, null = True, blank = True, max_length=400)
    state = models.CharField(default = None, null = True, blank = True, max_length = 50)
    middle_name = models.CharField(default = None, null = True, blank = True, max_length=40)
    class Meta:
        ordering = ('-date_joined',)
        indexes = [models.Index(fields=['id', 'email']),]
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"