from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# from base.models import *
from .validators import *
from .manager import UserManager
import uuid





class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'base_user'


class BankUser(BaseUser):
    phone = models.CharField(max_length=13,unique=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'wallet_user'

class BankAccount(BaseModel):
    user = models.OneToOneField(BankUser, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0,validators=[MinValueValidator(1.0)])
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.user.email
    class Meta:
        db_table = 'bank_account'

class Wallet(BaseModel):
    bank = models.OneToOneField(BankAccount,related_name="bank", on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0,validators=[MinValueValidator(1.0)])
    def __str__(self):
        return self.bank.user.email
    class Meta:
        db_table = 'wallet'

class WalletTransaction(BaseModel):
    transaction_id = models.CharField(max_length=100,null = True,blank=True)
    receiver= models.ForeignKey(Wallet,related_name="wallet_reciever", on_delete=models.CASCADE)
    sender = models.ForeignKey(Wallet,related_name="sender_wallet", on_delete=models.CASCADE)   
    amount = models.FloatField(default=0.0,validators=[MinValueValidator(1.0)])
    class Meta:
        db_table = 'wallet_transaction'

class BankTransaction(BaseModel):
    transaction_id = models.CharField(max_length=100,null = True,blank=True)
    receiver= models.ForeignKey(BankAccount,related_name="bank_reciever", on_delete=models.CASCADE)
    sender = models.ForeignKey(Wallet,related_name="sender_bank", on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0,validators=[MinValueValidator(1.0)])
    class Meta:
        db_table = 'bank_transaction'

