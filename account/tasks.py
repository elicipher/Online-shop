from celery import shared_task
from utils import send_otp_code

@shared_task
def send_otp_code_task(Subject,phone_number , code):
    send_otp_code(Subject,phone_number , code)