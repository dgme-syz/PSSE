from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    code = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    code = serializers.CharField()
