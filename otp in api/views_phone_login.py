from django.shortcuts import render
import random
from .permissions import CheckSessionForPermissions, LogoutRequiredPermissions
from rest_framework.response import Response
from .serializers import PhoneOTPSerializer, UserOtpLoginSerializer
from rest_framework.views import APIView
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator


class SendOTPView(APIView):
    serializer_class = PhoneOTPSerializer
    permission_classes = [LogoutRequiredPermissions]

    def get(self, request):
        serializer = PhoneOTPSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = random.randint(10000, 99999)
        number = int(request.data['phone_number'])

        request.session['otp'] = otp
        request.session['phone_number'] =  number
        request.session['number_check_otp'] =  0
        request.session['otp_time'] =  f"{datetime.now(pytz.timezone('Asia/Tehran')) + timedelta(minutes=5)}"

        number = "0"+str(number)
        msg =  f"password for login with phone in site boomilia.com {otp}"
        #send_sms(number, msg)

        return Response({'msg': 'please check your sms phone and get OTP'},status=301)


class UserOTPLoginView(APIView):    
    serializer_class = UserOtpLoginSerializer
    permission_classes = [CheckSessionForPermissions, LogoutRequiredPermissions]
    
    def get(self, request):
        serializer = UserOtpLoginSerializer()
        return Response(serializer.data)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = request.data['otp']
        number = "+98"+str(request.session['phone_number'])
        otp_check = request.session.get('otp')
        request.session['number_check_otp'] = int(request.session.get('number_check_otp')) + 1 

        if str(otp) != str(otp_check):
            return Response({"message":"otp is not correct, please check again your sms"}, status=401)
        
        user = get_object_or_404(get_user_model(), phone = number)

        login(request, user)

        return Response({'msg': 'user is login in site'},status=301)