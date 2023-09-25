from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string


# Registration Code Model
class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def generate_code(cls, email):
        code = get_random_string(length=6, allowed_chars='0123456789')
        verification_code, created = cls.objects.get_or_create(email=email)
        verification_code.code = code
        verification_code.save()
        return code

# User Model and Car Model
class ParkingSystemUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('邮箱地址是必需的')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class ParkingSystemUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    cars = models.ManyToManyField('Car', blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = ParkingSystemUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Car(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.license_plate
