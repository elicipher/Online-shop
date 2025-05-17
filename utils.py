from kavenegar import *

def send_otp_code(phone_number , code):
   
   try:
      api = KavenegarAPI('376E74376E3643392F4B63655858796F7154674838363834733179727A4C4D6D48763447313377473452493D')
      params = {
         'sender': '2000660110',#optional
         'receptor': phone_number,#multiple mobile number, split by comma
         'message': f' «فروشگاه الی سایفر» \n کد تایید عضویت شما : \n {code}   ',
      } 
      response = api.sms_send(params)
      print(response)
      
   except APIException as e: 
      print(e)
   except HTTPException as e: 
      print(e)