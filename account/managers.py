from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    #We can create custom methods.

    def create_user(self , phone_number , email ,full_name, password ):
        if not phone_number:
            raise ValueError("User must be have phone number")
        if not email :
            raise ValueError("User must be have email")
        if not full_name:
            raise ValueError("User must be full name")
        
        #Django validates the password.

        #creates a new user object form the model class connected to the manager. 
        user = self.model(phone_number = phone_number, email = self.normalize_email(email) ,full_name = full_name ) 
        user.set_password(password)
        user.save(using = self._db)#save the user in the database
        return user
    
    def create_superuser(self , phone_number , email , full_name , password):

        user = self.create_user(phone_number ,email , full_name , password)
        user.is_admin = True
        user.save(using = self._db)
        return user