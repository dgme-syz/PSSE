from django.utils import timezone
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from .models import Car, ParkingRecord, ParkingRate, GlobalSettings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import date, datetime
from django.db.models import Sum
from .Licence_Recognition.detect import predict_api
import math
import json

# Create your views here.
@csrf_exempt
@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'success': True, 'csrf_token': csrf_token})
def calculate_parking_duration(start_time, end_time):
    # 计算停车时间（以分钟为单位）
    if start_time and end_time:
        duration = (end_time - start_time).total_seconds() / 60
        return duration
    return 0

def calculate_parking_price(parking_duration_minutes, car_type):
    try:
        # 尝试从数据库中获取给定车型的价格记录
        parking_rate = ParkingRate.objects.get(car_type=car_type)
        
        # 获取价格记录中的价格信息
        rate_per_hour = parking_rate.price_per_hour

        # 计算停车价格，四舍五入到两位小数
        parking_price = round((math.ceil(parking_duration_minutes / 60)) * rate_per_hour, 2)

        return parking_price
    except ParkingRate.DoesNotExist:
        # 如果车型不存在对应的价格记录，可以返回一个默认价格或者引发异常
        raise ValueError('未知的车型')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_car(request):
    user = request.user

    # 将请求体内容保存在变量中
    request_data=request.data
    print(request_data)
    serializer = AddCarSerializer(data=request_data)
    
    if serializer.is_valid():
        request_data = serializer.validated_data
        car_type = request_data.get('car_type')
        license_plate = request_data.get('license_plate')
        print(license_plate)
        
        existing_car = Car.objects.filter(license_plate=license_plate).first()
        
        if existing_car:
            return Response({'success': True, 'message': '车辆已存在'}, status=status.HTTP_200_OK)


        # 创建车辆并设置停车时间
        car = Car.objects.create(license_plate=license_plate, parked_at=None, car_type=car_type)

        # 将车辆与用户关联
        user.cars.add(car)

        return Response({'success': True, 'message': '车辆已添加'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def park_car(request):
    request_data=request.data
    print(request_data)
    
    serializer = ParkCarSerializer(data=request_data)
    
    if serializer.is_valid():
        request_data = serializer.validated_data
        license_plate = request_data.get('license_plate')
        existing_car = Car.objects.filter(license_plate=license_plate).first()
        
        if not existing_car:
            return Response({'success': False, 'error': '车辆不存在'}, status=status.HTTP_201_CREATED)

        if existing_car.parked_at:
            return Response({'success': False, 'error': '车辆已经停车'}, status=status.HTTP_400_BAD_REQUEST)

        global_settings = GlobalSettings.objects.first()

        if global_settings.parking_spots <= 0:
            return Response({'success': False, 'error': '停车场已满'}, status=status.HTTP_400_BAD_REQUEST)

        if global_settings:
            global_settings.parking_spots -= 1
            global_settings.save()

        existing_car.parked_at = timezone.now()
        existing_car.save()
        return Response({'success': True, 'message': '车辆已停车'}, status=status.HTTP_200_OK)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 只有认证用户可以访问此视图
def delete_car(request):
    data=request.data

    serializer = DeleteCarSerializer(data = data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        print(data)
        license_plate = data.get('license_plate')
        car_to_remove = Car.objects.filter(license_plate=license_plate).first()
        
        if car_to_remove:
            if car_to_remove.parked_at:
                return Response({'success': False, 'error': '车辆还没出库'}, status=status.HTTP_201_CREATED)
            else:
                request.user.cars.remove(car_to_remove)
                car_to_remove.delete()
                return Response({'success': True, 'message': '车辆已删除'}, status=status.HTTP_200_OK)
        else:    
            return Response({'success': False, 'error': '车辆不存在'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 只有认证用户可以访问此视图
def reset_parking_duration(request):
    data=request.data
    serializer = ResetParkingDurationSerializer(data=data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        license_plate = data.get('license_plate')
        car_to_reset = Car.objects.filter(license_plate=license_plate).first()
        
        if car_to_reset:
            start_time = car_to_reset.parked_at
            end_time = timezone.now()
            parking_duration = calculate_parking_duration(start_time, end_time)
            parking_duration = round(parking_duration, 2)
            parking_price = calculate_parking_price(parking_duration, car_to_reset.car_type)
            
            global_settings = GlobalSettings.objects.first()
            
            if global_settings:
                global_settings.parking_spots += 1
                global_settings.save()
            
            car_to_reset.parked_at = None
            car_to_reset.save()
            
            parking_record = ParkingRecord(car=car_to_reset, start_time=start_time, end_time=end_time, price=parking_price, license_plate=license_plate)
            parking_record.save()
            
            return Response({'success': True, 'message': '取车成功', 'parking_duration_minutes': parking_duration,
                             'parking_price': parking_price}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'error': '车辆不存在或者尚未停车'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)
# @login_required

@api_view(['POST'])
def update_parking_price(request):
    if not request.user.is_staff:  # 假设你的用户模型有一个 is_staff 字段来表示管理员状态
        return Response({'success': False, 'message': '只有管理员可以访问此视图'}, status=status.HTTP_403_FORBIDDEN)
    data=request.data
    car_type = data.get('car_type')
    new_price = float(data.get('new_price'))
    
    try:
        parking_rate = ParkingRate.objects.get(car_type=car_type)
        parking_rate.price_per_hour = new_price
        parking_rate.save()
        
        # 使用序列化器将响应数据序列化为JSON格式
        serializer = ParkingRateSerializer(parking_rate)
        
        response_data = {
            'success': True,
            'message': '停车价格已更新',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except ParkingRate.DoesNotExist:
        response_data = {
            'success': False,
            'message': '车型不存在'
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def query_parking_record_by_date(request):
    try:
        # 获取查询参数
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # 将日期字符串转换为日期对象
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        # 获取查询日期的开始时间（当天的最早时刻）
        start_datetime = datetime.combine(start_date, datetime.min.time())

        # 获取查询日期的结束时间（当天的最晚时刻）
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # 为查询日期的开始时间和结束时间添加时区信息
        start_datetime_with_tz = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        end_datetime_with_tz = timezone.make_aware(end_datetime, timezone.get_current_timezone())

        # 查询匹配日期范围的停车记录
        parking_records = ParkingRecord.objects.filter(
            start_time__range=(start_datetime_with_tz, end_datetime_with_tz),
            end_time__range=(start_datetime_with_tz, end_datetime_with_tz)
        )

        total_cost = parking_records.aggregate(Sum('price'))['price__sum']

        # 使用序列化器将查询到的停车记录序列化为JSON格式
        serializer = ParkingRecordSerializer(parking_records, many=True)

        return Response({
            'success': True,
            'data': serializer.data,
            'number_of_records': parking_records.count(),
            'total_cost': total_cost
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_parking_spots(request):
    global_settings = GlobalSettings.objects.first()
    serializer = GlobalSettingsSerializer({
        'number': global_settings.parking_spots,
        'origin_number': global_settings.origin_parking_spots,
    })
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_plate_number(request):

    predict_api()

