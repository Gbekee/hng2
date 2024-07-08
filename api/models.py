from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, password):
        if not email:
            raise ValueError('Email required')
        if not password:
            raise ValueError('password required')
        user=self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
            )
        user.set_password(password)
        user.save()
        
        return user
    def create_superuser(self, first_name, last_name, email,  phone, password):
        if not email:
            raise ValueError('Email required')
        if not password:
            raise ValueError('password required')
        user=self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone, 
            password=password
            )
    
        user.is_admin=True
        user.is_active=True
        user.is_superadmin=True
        user.is_staff=True
        user.save()
        return User
    
class User(AbstractBaseUser):
    first_name=models.CharField(verbose_name='First name', max_length=50)
    last_name=models.CharField(verbose_name='Last name', max_length=50)
    email=models.EmailField(unique=True)
    phone=models.CharField(verbose_name='Phone number', max_length=20)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name',  'phone', 'password']
    def save( self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            org=Organisation.objects.create(name=self.first_name+"'s Organisation")
            org.user.add(self)
            org.save()
            return self
        super().save(*args, **kwargs)
    def has_module_perms(self, perm, obj=None):
        return self.is_admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

class Organisation(models.Model):
    user=models.ManyToManyField(User, related_name='organisations')
    name=models.CharField(max_length=30)
    description=models.TextField(null=True)