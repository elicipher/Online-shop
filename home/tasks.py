from bucket import bucket

#نیاز به جاوا اسکریپ دارد برای  ای سینک کردن تابع
#TODO: can be async ? 
def all_bucket_object_task():
    result = bucket.get_objects()
    return result
