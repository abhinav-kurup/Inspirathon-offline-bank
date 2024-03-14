from django.urls import path
from .views import *


urlpatterns = [
    path('user-signup/', user_signup, name="user-signup"),
    path('user-signup-otp/', user_signup_otp, name="user-signup-otp"),
    path('user-login/', user_login, name="user-login"),
    path('user-login-otp/', user_login_otp, name="user-login-otp"),

    path('decrypt-data/', decrypt_data, name="decrypt-data"),
    path('encrypt-data/', encrypt_data, name="encrypt-data"),



    path('money-to-wallet/', money_to_wallet, name="money-to-wallet"),
    path('money-to-bank/', money_to_bank, name="money-to-bank"),

    path('get-bank-balance/', bank_balance, name="get-bank-balance"),

    path('add-wallet-transaction/', add_wallet_transaction, name="add-wallet-transaction"),
    path('add-bank-transaction/', add_bank_transaction, name="add-bank-transaction"),
    
    path('get-wallet-details/', wallet_details, name="get-wallet-details"),
    path('get-bank-details/', bank_details, name="get-bank-details"),

    path('add/', add),

    path('get-wallet-transactions/', get_wallet_transactions, name="get-wallet-transactions"),

    path('wallet-to-bank/', wallet_to_bank, name="wallet-to-bank"),
]