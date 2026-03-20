from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using 
    either their email or their phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Look for a user where the email OR phone_number matches the input
            user = User.objects.get(Q(email=username) | Q(phone_number=username))
        except User.DoesNotExist:
            return None

        # Check the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None