from django.core.management.base import BaseCommand
from account.models import OtpCode
from datetime import timedelta , datetime
import pytz


class Command(BaseCommand):
    help = "delete all expired otp codes"
   
    def handle(self , *args , **options):
        expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt =expired_time).delete()
        #created__lt = کوچک تر از expired_time
        #tz=pytz.timezone("Asia/Tehran") = با زمان واقعی هماهنگه

        self.stdout.write(
            self.style.SUCCESS("all expired otp codes removed")
        )