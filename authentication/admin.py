from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(BankUser)
admin.site.register(Wallet)
admin.site.register(BankAccount)
admin.site.register(WalletTransaction)
admin.site.register(BankTransaction)
