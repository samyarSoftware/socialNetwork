from .models import User

class PhoneAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
            return None
        except (User.MultipleObjectsReturned, User.DoesNotExist):
            return None
        
    def get_user(request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None