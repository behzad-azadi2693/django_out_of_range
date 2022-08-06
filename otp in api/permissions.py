from rest_framework.permissions import BasePermission
from datetime import datetime
import pytz


class LogoutRequiredPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


class CheckSessionForPermissions(BasePermission):
    def has_permission(self, request, view):
        phone_number = request.session.get('phone_number', None)
        otp_time = request.session.get('otp_time', None)
        number_check = request.session.get('number_check_otp', None)

        if (phone_number is None):
            return False

        elif (number_check is None) and (int(number_check) >= 5):
            return False
        
        elif (str(otp_time) < str(datetime.now(pytz.timezone('Asia/Tehran')))):
            return False

        return True