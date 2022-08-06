from rest_framework import serializers
import re
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model


class PhoneOTPSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(required=True)
    
    def validate_phone_number(self, value):
        if not re.findall(r'^9\d{9}$', str(value)):
            raise serializers.ValidationError('please check your phone number fields')

        return value   

    def validate(self, data):
        number = "+98"+str(data['phone_number'])
        user = get_user_model().objects.filter(phone = number).exists()
        if not user:
            raise serializers.ValidationError('phone number is not exists')

        return data['phone_number']



class UserOtpLoginSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    
    def validate_otp(self, value):

        if len(str(value)) != 5 and isinstance(value, int):
            raise serializers.ValidationError('please check your sms for otp')

        return value    

    
