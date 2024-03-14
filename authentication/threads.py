import threading, random
from django.conf import settings
from django.core.cache import cache


context = {}


class send_login_otp(threading.Thread):
    def __init__(self, phone):
        self.phone = phone
        threading.Thread.__init__(self)
    def run(self):
        try:
            otp = random.randint(10001, 99999)
            cache.set(otp, self.phone, 350)
            print(otp)
            subject = "OTP to login into your account"
            message = f"The OTP to log in into your email is {otp} \nIts valid only for 2 mins."
            email_from = settings.EMAIL_HOST_USER
            print("started sending")
            # send_mail(subject , message ,email_from ,[self.email])
            print("finished sending")
        except Exception as e:
            print(e)


class SendForgotOTP(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            otp = random.randint(100001, 999999)
            cache.set(otp, self.email, 350)
            print(otp)
            subject = "OTP to reset your account password"
            message = f"The OTP to reset your password is {otp} \nIts valid only for 2 mins."
            email_from = settings.EMAIL_HOST_USER
            print("started sending")
            # send_mail(subject , message ,email_from ,[self.email])
            print("finished sending")
        except Exception as e:
            print(e)
