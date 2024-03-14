from celery import shared_task
from .models import *
import time

@shared_task
def delete_unverified(id):
    try:
        # time.sleep(15)
        print("Entered")
        data = BankUser.objects.get(pk=id)
        if not data.verified:
            data.delete()
            print("Deleted unverified user")
    except BankUser.DoesNotExist:
        pass