from celery import shared_task
from utils import send_otp_code
from account.models import OtpCode
from datetime import timedelta , datetime
import pytz

@shared_task
def send_otp_code_task(Subject,phone_number , code):
    send_otp_code(Subject,phone_number , code)


@shared_task
def remove_expired_otp_codes():
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt =expired_time).delete()