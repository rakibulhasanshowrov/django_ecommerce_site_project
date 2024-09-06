from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy



# Create your models here.
class MyUserManager(BaseUserManager):
  # A custom Manager to deal with emails as unique identifier
  def _create_user(self, email, password,**extra_fields):
    # Create and save a user with a given email and Password
    
    if not email:
      raise ValueError('The Email must be set')
    
    email=self.normalize_email(email)
    user=self.model(email=email,**extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self,email,password,**extra_fields):
    extra_fields.setdefault('is_staff',True)
    extra_fields.setdefault('is_superuser',True)
    extra_fields.setdefault('is_active',True)
    
    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True')
    
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True')
    return self._create_user(email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
  email=models.EmailField(unique=True,null=False)
  is_staff = models.BooleanField(
    ugettext_lazy('staff Status'),
    default=False,
    half_text=ugettext_lazy('Designates wheather the user can log in this site')
  )    
  is_active=models.BooleanField(
     ugettext_lazy('active')
     
  )