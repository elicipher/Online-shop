from kavenegar import *

def send_otp_code(Subject,phone_number , code):
   
   try:
      api = KavenegarAPI('41463741336C447569467271653658576F33634E545152477459317331586735572B7466446C7734432B4D3D')
      params = {
         'sender': '2000660110',#optional
         'receptor': phone_number,#multiple mobile number, split by comma
         'message': f' «فروشگاه الی سایفر» \n کد تایید {Subject} شما : \n {code}   ',
      } 
      response = api.sms_send(params)
      print(response)
      
   except APIException as e: 
      print(e)
   except HTTPException as e: 
      print(e)