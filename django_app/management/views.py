import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import VerificationCode, ParkingSystemUser
from PIL import Image


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        username = data.get('username')
        password = data.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': '登录成功'})
        else:
            return JsonResponse({'success': False, 'message': '用户名或密码错误'})

    return JsonResponse({'success': False, 'message': '请求方法错误'})


def home_view(request):
    return render(request, 'dist/index.html')
    
# 便于简单配置上传图片
@csrf_exempt 
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
        return JsonResponse(response_data)
    
    # 如果不是 POST 请求，返回 400 错误
    return JsonResponse({'success': False,'error': '只支持 POST 请求'}, status=400)

@csrf_exempt
def send_verification_code(request):
    if request.method == 'GET':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')

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
        return JsonResponse({'success': True, "message": "验证码发送成功"})

    return JsonResponse({'success': False, 'error': '仅支持 GET 请求'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        entered_code = data.get('code')

        # 在生成验证码之前查询数据库，检查用户是否已注册
        from django.contrib.auth.models import User
        user_exists = ParkingSystemUser.objects.filter(email=email).exists()
        if user_exists:
            return JsonResponse({'success': False, 'error': '该邮箱已注册'})


        # 查询数据库中是否有该邮箱的验证码记录
        try:
            verification_code = VerificationCode.objects.get(email=email)
        except VerificationCode.DoesNotExist:
            return JsonResponse({'success': False, 'error': '请先获取验证码'})

        # 检查验证码是否过期
        from django.utils import timezone
        current_time = timezone.now()
        validity_period_minutes = 5  # 假设验证码有效期为5分钟
        time_difference = current_time - verification_code.created_at

        if time_difference.total_seconds() / 60 > validity_period_minutes:
            return JsonResponse({'success': False, 'error': '验证码已过期，请重新获取'})

        # 检查验证码是否正确
        if entered_code != verification_code.code:
            return JsonResponse({'success': False, 'error': '验证码不正确'})

        # 保存用户密码到数据库（示例中使用了Django内置的User模型）
        user = ParkingSystemUser(username=email, email=email)
        user.set_password(password)
        user.save()

        # 注册成功，可以清理验证码记录
        verification_code.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': '仅支持 POST 请求'})

# Change User email


@login_required
@csrf_exempt
def change_email(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        new_email = data.get('new_email')
        entered_code = data.get('code')
        user = request.user

        # 验证新邮箱是否合法

        if user.email == new_email:
            return JsonResponse({'success': False, 'error': '新邮箱与当前邮箱相同。'})
        else:
            try:
                # 检查验证码是否有效
                verification_code = VerificationCode.objects.get(
                    email=user.email, code=entered_code)
            except VerificationCode.DoesNotExist:
                return JsonResponse({'success': False, 'error': '验证码不正确或已过期。'})
            else:
                verification_code.delete()  # 验证通过后删除验证码
                user.email = new_email
                user.save()
                return JsonResponse({'success': False, 'message': '邮箱已成功修改。'})
    return JsonResponse({'success': False, 'error': '仅支持 POST 请求'})


@login_required
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        entered_code = data.get('code')
        user = request.user

        try:
            # 验证验证码是否有效
            verification_code = VerificationCode.objects.get(
                email=user.email, code=entered_code)
        except VerificationCode.DoesNotExist:
            return JsonResponse({'success': False, 'error': '验证码不正确或已过期。'})

        # 验证旧密码是否正确
        if not user.check_password(old_password):
            return JsonResponse({'success': False, 'error': '旧密码不正确。'})
        else:
            verification_code.delete()  # 验证通过后删除验证码
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': '仅支持 POST 请求。'})
