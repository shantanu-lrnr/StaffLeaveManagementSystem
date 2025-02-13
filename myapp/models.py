from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManger(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        # Creates and saves an User with the given email and password.
        if not email:
            raise ValueError("User must have an valid email address")
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Creates and saves a superuser with the given email and password.
        user = self.create_user(email, password,**extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    username = models.CharField(max_length=255,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staffmember = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to="images",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManger() 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Only Superuser have permission to access all data
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return self.is_superuser
    
class Staff(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True)
    gender = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class StaffLeave(models.Model):
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE,related_name="all_leaves")
    leave_type = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    message = models.TextField()
    status = models.CharField(max_length=100,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff.user.first_name + self.staff.user.last_name