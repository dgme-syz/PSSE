from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.core.mail import send_mail
from .models import VerificationCode, ParkingSystemUser
from PIL import Image
from .serializers import UserLoginSerializer, SendVerificationCodeSerializer, RegisterSerializer, ChangeEmailSerializer, ChangePasswordSerializer

@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({'success':True}, status=status.HTTP_200_OK)
        else:
            return Response({'success':False}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'success': False, 'message': '请求数据无效'}, status=status.HTTP_400_BAD_REQUEST)

def home_view(request):
    return render(request, 'dist/index.html')
    
# 便于简单配置上传图片
def pic_solve(request):
    if request.method == 'POST':
        # 接收上传的图片文件
        file = request.FILES.get('file')
        
        # 使用 Pillow 库打开图片文件
        image = Image.open(file)
        # image.show()
        
        # 在这里进行你的图像处理逻辑
        # ...
        
        # 返回处理后的信息
        response_data = {
            'message': '图片处理成功',
            # 添加其他需要返回的信息
        }
        return Response(response_data)
    
    # 如果不是 POST 请求，返回 400 错误
    return Response({'success': False,'error': '只支持 POST 请求'}, status=400)

@api_view(['GET'])
def send_verification_code(request):
    serializer = SendVerificationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']

        # 删除旧的验证码记录（如果存在）
        VerificationCode.objects.filter(email=email).delete()

        # 生成随机验证码并保存到数据库
        verification_code = VerificationCode.generate_code(email)

        # 邮件内容
        subject = '注册验证码'
        message = f'您的验证码是：{verification_code}'
        from_email = 'your_email@example.com'  # 发件人邮箱
        recipient_list = [email]  # 收件人邮箱

        # 发送邮件
        # send_mail(subject, message, from_email,
        #           recipient_list, fail_silently=False)

        # 返回响应
        return Response({'success': True})
    return Response({'success': False, 'error': '无效的数据'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            entered_code = serializer.validated_data['code']

            # 在生成验证码之前查询数据库，检查用户是否已注册
            user_exists = ParkingSystemUser.objects.filter(email=email).exists()
            if user_exists:
                return Response({'success': False, 'error': '该邮箱已注册'}, status=status.HTTP_400_BAD_REQUEST)

            # 查询数据库中是否有该邮箱的验证码记录
            try:
                verification_code = VerificationCode.objects.get(email=email)
            except VerificationCode.DoesNotExist:
                return Response({'success': False, 'error': '请先获取验证码'}, status=status.HTTP_401_UNAUTHORIZED)

            # 检查验证码是否过期
            from django.utils import timezone
            current_time = timezone.now()
            validity_period_minutes = 5  # 假设验证码有效期为5分钟
            time_difference = current_time - verification_code.created_at

            if time_difference.total_seconds() / 60 > validity_period_minutes:
                return Response({'success': False, 'error': '验证码已过期，请重新获取'}, status=status.HTTP_401_UNAUTHORIZED)

            # 检查验证码是否正确
            if entered_code != verification_code.code:
                return Response({'success': False, 'error': '验证码不正确'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存用户密码到数据库（示例中使用了Django内置的User模型）
            user = ParkingSystemUser(username=username, email=email)
            user.set_password(password)
            user.save()

            # 注册成功，可以清理验证码记录
            verification_code.delete()

            return Response({'success': True},status=status.HTTP_201_CREATED)

        return Response({'success': False, 'error': '无效的数据'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': False, 'error': '仅支持 POST 请求'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Change User email


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    serializer = ChangeEmailSerializer(data=request.data)
    if serializer.is_valid():
        new_email = serializer.validated_data['new_email']
        entered_code = serializer.validated_data['code']
        user = request.user

        # 验证新邮箱是否合法
        if user.email == new_email:
            return Response({'success': False, 'error': '新邮箱与当前邮箱相同。'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 检查验证码是否有效
            verification_code = VerificationCode.objects.get(email=user.email, code=entered_code)
        except VerificationCode.DoesNotExist:
            return Response({'success': False, 'error': '验证码不正确或已过期。'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证通过后删除验证码
        verification_code.delete()
        
        # 修改用户邮箱
        user.email = new_email
        user.save()
        
        return Response({'success': True, 'message': '邮箱已成功修改。'})

    return Response({'success': False, 'error': '无效的数据'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            entered_code = serializer.validated_data['code']
            user = request.user

            try:
                # 验证验证码是否有效
                verification_code = VerificationCode.objects.get(email=user.email, code=entered_code)
            except VerificationCode.DoesNotExist:
                return Response({'success': False, 'error': '验证码不正确或已过期。'}, status=status.HTTP_400_BAD_REQUEST)

            # 验证旧密码是否正确
            if not user.check_password(old_password):
                return Response({'success': False, 'error': '旧密码不正确。'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                verification_code.delete()  # 验证通过后删除验证码
                user.set_password(new_password)
                user.save()
                return Response({'success': True})

        return Response({'success': False, 'error': '无效的数据'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': False, 'error': '仅支持 POST 请求。'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)