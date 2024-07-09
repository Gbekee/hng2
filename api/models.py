from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, password=None):
        if not email:
            raise ValueError('Email required')
        if not password:
            raise ValueError('Password required')
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.organisations.exists():
            org = Organisation.objects.create(name=f"{self.first_name}'s Organisation")
            org.user.add(self)
            org.save()
    
    def has_module_perms(self, app_label):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

class Organisation(models.Model):
    user = models.ManyToManyField(User, related_name='organisations')
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
