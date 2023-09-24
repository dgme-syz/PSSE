import json
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # 导入登录装饰器
from django.views.decorators.csrf import csrf_exempt


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
@csrf_exempt
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
