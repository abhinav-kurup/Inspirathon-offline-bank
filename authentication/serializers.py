from rest_framework import serializers
from .models import *

# class AddBankUser(serializers.ModelSerializer):
#     class Meta:
#         model = BankUser
#         fields = ["email", "name", "phone"]

class AddBankUser(serializers.Serializer):
    email = serializers.EmailField(required = True)
    name = serializers.CharField(required = True)
    phone = serializers.CharField(required = True)


class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    # password = serializers.CharField(required = True)

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required = True)

class dataserializer(serializers.Serializer):
    enc_data = serializers.CharField(required = True)

class MoneySerializer(serializers.Serializer):
    amount = serializers.FloatField(required = True)

class BankMoneySerializer(serializers.Serializer):
    amount = serializers.FloatField(required = True)
    password = serializers.CharField(required = True)

class AddWalletTransaction(serializers.Serializer):
    amount = serializers.FloatField(required = True)
    receiver = serializers.CharField(required = True)
    sender = serializers.CharField(required = True)
    transaction_id = serializers.CharField(required = True)

class AddBankTransaction(serializers.Serializer):
    amount = serializers.FloatField(required = True)
    receiver = serializers.CharField(required = True)
    type = serializers.CharField(required = True)
    transaction_id = serializers.CharField(required = True)

class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        exclude = ["created_at","updated_at"]

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ["created_at","updated_at","password","is_active"]

class WalletBankSerializer(serializers.Serializer):
    wallet = serializers.CharField(required = True)
    amount = serializers.FloatField(required = True)

class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        exclude = ["id","created_at","updated_at"]