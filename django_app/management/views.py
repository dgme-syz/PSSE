import json
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # 导入登录装饰器
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
import hashlib
import random

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})
#
@csrf_protect  # 使用@csrf_protect装饰器来启用CSRF保护
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data.get('name')
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


@csrf_protect  # 使用@csrf_protect装饰器来启用CSRF保护
def register_user(request):
    if request.method == 'POST':
        # 从请求数据中获取用户名和密码
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        # 生成随机盐值
        salt = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()[:16]

        # 使用盐值对密码进行加盐哈希
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        # 创建用户
        user = User.objects.create_user(username=username, password=hashed_password)

        # 在这里可以添加其他用户相关的操作，例如设置用户属性等

        return JsonResponse({'message': 'Registration successful'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
