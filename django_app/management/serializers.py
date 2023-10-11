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

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    def create(self, validated_data):
        # 这里可以不实现任何逻辑，只需返回一个空的实例即可
        return self