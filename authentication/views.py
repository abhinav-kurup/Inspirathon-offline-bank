from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from .encryption import *
from .task import *
from .threads import *
from .models import *   
from .serializers import *
# Create your views here.





@api_view(["POST"])
def user_signup(request):
    try:
        print(request.data)
        ser = AddBankUser(data=request.data)
        if ser.is_valid():
            email = ser.validated_data["email"]
            if BankUser.objects.filter(email=email).first():
                return Response({"ERROR":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_user = BankUser.objects.create(
                email = email,
                name = ser.validated_data["name"],
                phone = ser.validated_data["phone"],
            )
            thread_obj = send_login_otp(ser.validated_data["phone"])
            thread_obj.start()
            new_user.set_password("123456")
            new_user.save()
            delete_unverified.delay(new_user.id)
            return Response({"message": "New User Added"}, status=status.HTTP_201_CREATED)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

@api_view(["POST"])
def user_signup_otp(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.validated_data["otp"]
            user_phone = cache.get(otp)
            print(user_phone)
            if not cache.get(otp):
                return Response({"ERROR":"OTP invalid or expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            obj = BankUser.objects.filter(phone=user_phone).first()
            if obj is None:
                return Response({"ERROR":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=obj.email,password=123456 )
            print("##########",user)
            if not user:
                return Response({"ERROR":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            cache.delete(otp)
            wallet = Wallet.objects.filter(bank__user=user).first()
            return Response({"message":"Login successfull","wallet":str(wallet.id), "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"ERROR":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def user_login(request):
    try:
        data = request.data
        ser = PhoneSerializer(data=data)
        if ser.is_valid():
            phone = ser.validated_data["phone"]
            if not BankUser.objects.filter(phone=phone).first():
                return Response({"ERROR":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            thread_obj = send_login_otp(ser.validated_data["phone"])
            thread_obj.start()
            # delete_unverified.delay(new_user.id)
            return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def user_login_otp(request):
    try:
        data = request.data
        ser = otpSerializer(data=data)
        if ser.is_valid():
            otp = ser.validated_data["otp"]
            user_phone = cache.get(otp)
            if not cache.get(otp):
                return Response({"ERROR":"OTP invalid or expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
            obj = BankUser.objects.filter(phone=user_phone).first()
            if obj is None:
                return Response({"ERROR":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=obj.email, password=123456)
            print("##########",user)
            jwt_token = RefreshToken.for_user(user)
            cache.delete(otp)
            wallet = Wallet.objects.filter(bank__user=user).first()
            return Response({"message":"Login successfull","wallet":str(wallet.id), "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
def decrypt_data(request):
    try:
        ser = dataserializer(data=request.data)
        if ser.is_valid():
            enc_data = ser.validated_data["enc_data"]
            data = jwt_dec(enc_data)
            return Response({"message": str(data)}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def encrypt_data(request):
    try:
        enc_data ={
            "name":"sagar",
            "email":"dha"
        }
        data = jwt_enc(enc_data)
        return Response({"message": str(data)}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def money_to_wallet(request):
    try:
        user = request.user
        print("@@@@@@@@@",user)
        ser = BankMoneySerializer(data=request.data)
        if ser.is_valid():
            amount = ser.validated_data["amount"]
            password = ser.validated_data["password"]

            if amount <= 0:
                return Response({"ERROR":"Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            ba = BankAccount.objects.get(user=user)
            if not check_password(password, ba.password):
                return Response({"ERROR":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            wa = Wallet.objects.get(bank=ba)
            if ba.balance < amount:
                return Response({"ERROR":"Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            ba.balance -= amount
            ba.save()
            return Response({"message": "Money added to wallet"}, status=status.HTTP_200_OK)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def money_to_bank(request):
    try:
        user = request.user
        ser = MoneySerializer(data=request.data)
        if ser.is_valid():
            amount = ser.validated_data["amount"]
            if amount <= 0:
                return Response({"ERROR":"Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            ba = BankAccount.objects.get(user=user)
            wa = Wallet.objects.get(bank=ba)
            ba.balance += amount
            ba.save()
            return Response({"message": "Money added to Bank"}, status=status.HTTP_200_OK)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def bank_balance(request):
    try:
        user = request.user
        ba = BankAccount.objects.get(user=user)
        ser = MoneySerializer({"amount":ba.balance})
        return Response({"balance":ser.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_wallet_transaction(request):
    try:
        user = request.user
        ser = AddWalletTransaction(data=request.data)
        if ser.is_valid():
            amount = ser.validated_data["amount"]
            receiver = ser.validated_data["receiver"]
            sender = ser.validated_data["sender"]
            transaction_id = ser.validated_data["transaction_id"]
            wa = Wallet.objects.filter(pk=sender).first()
            if Wallet.objects.filter(pk=receiver).first():
                re = Wallet.objects.filter(pk=receiver).first()
                WalletTransaction.objects.create(
                amount = amount,
                receiver = re,
                sender = wa,
                transaction_id = transaction_id
                )
                return Response({"message": "Transaction Stored"}, status=status.HTTP_200_OK)
            else:
                re = BankAccount.objects.filter(pk=receiver).first()
                BankTransaction.objects.create(
                amount = amount,
                receiver = re,
                sender = wa,
                transaction_id = transaction_id
                )
                return Response({"message": "Transaction Stored"}, status=status.HTTP_200_OK)
            
            
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_bank_transaction(request):
    try:
        user = request.user
        ser = AddBankTransaction(data=request.data)
        if ser.is_valid():
            amount = ser.validated_data["amount"]
            receiver = ser.validated_data["receiver"]
            sender = ser.validated_data["sender"]
            transaction_id = ser.validated_data["transaction_id"]
            if not BankAccount.objects.filter(pk=receiver).first():
                return Response({"ERROR":"Invalid receiver"}, status=status.HTTP_400_BAD_REQUEST)
            wa = Wallet.objects.filter(pk=sender).first()
            BankTransaction.objects.create(
                amount = amount,
                receiver = BankAccount.objects.get(pk=receiver),
                sender = wa,
                transaction_id = transaction_id
            )
            return Response({"message": "Transaction Stored"}, status=status.HTTP_200_OK)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def wallet_details(request):
    try:
        user = request.user
        wa = Wallet.objects.get(bank__user=user)
        ser = WalletDetailSerializer(wa)
        return Response({"details":ser.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def bank_details(request):
    try:
        user = request.user
        ba = BankAccount.objects.get(user=user)
        ser = BankDetailSerializer(ba)
        return Response({"details": ser.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def wallet_to_bank(request):
    try:
        user = request.user
        ser = WalletBankSerializer(data=request.data)
        if ser.is_valid():
            amount = ser.validated_data["amount"]
            if amount <= 0:
                return Response({"ERROR":"Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            ba = BankAccount.objects.get(user=user)
            wa = Wallet.objects.get(pk=ser.validated_data["wallet"])
            ba.balance += amount
            ba.save()
            return Response({"message": "Money added to Bank"}, status=status.HTTP_200_OK)
        return Response({"ERROR":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def add(request):
    user = BankUser.objects.get(email = "aryan@gmail.com")
    BankAccount.objects.create(user =user, password = make_password("1234"))
    return Response({"message": "Money added to Bank"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_wallet_transactions(request):
    try:
        user = request.user
        wa = Wallet.objects.get(bank__user=user)
        wall_transactions = WalletTransaction.objects.filter(Q(sender=wa) | Q(receiver=wa)).order_by("-created_at")
        ser = WalletTransactionSerializer(wall_transactions, many=True)
        return Response({"transactions": ser.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print("ERROR : ", e)
        return Response({"ERROR":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)