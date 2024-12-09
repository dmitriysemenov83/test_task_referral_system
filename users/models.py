from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random
import string


NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('У пользователей должен быть номер телефона!!!')
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True,**NULLABLE, verbose_name='invite code')
    activated_invite_code = models.CharField(max_length=6, **NULLABLE, verbose_name='activated invite code')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args, **kwargs)

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE,
                                 verbose_name='referral')
    referred_user = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE,
                                      verbose_name='referred')

    class Meta:
        db_table = 'referrals'
        verbose_name = 'referral'
        verbose_name_plural = 'referrals'

    def __str__(self):
        return f"{self.referrer.phone_number} referred {self.referred_user.phone_number}"