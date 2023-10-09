from django.utils import timezone
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncMonth
from datetime import date, datetime, timedelta
from django.db.models import Sum, Max, Count
from .models import *
from .serializers import *
import math
import csv

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token': csrf_token})


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
        parking_price = round(
            (math.ceil(parking_duration_minutes / 60)) * rate_per_hour, 2)

        return parking_price
    except ParkingRate.DoesNotExist:
        # 如果车型不存在对应的价格记录，可以返回一个默认价格或者引发异常
        raise ValueError('未知的车型')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_car(request):
    user = request.user

    # 将请求体内容保存在变量中
    request_data = request.data
    print(request_data)
    serializer = AddCarSerializer(data=request_data)

    if serializer.is_valid():
        request_data = serializer.validated_data
        license_plate = request_data.get('license_plate')
        existing_car = Car.objects.filter(license_plate=license_plate).first()

        if not existing_car:
            return Response({'success': True, 'message': '车辆不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 将车辆与用户关联
        user.cars.add(existing_car)
        return Response({'success': True, 'message': '车辆已添加'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def park_car(request):
    request_data = request.data

    serializer = ParkCarSerializer(data=request_data)

    if serializer.is_valid():
        request_data = serializer.validated_data
        license_plate = request_data.get('license_plate')
        existing_car = Car.objects.filter(license_plate=license_plate).first()

        if not existing_car:
            existing_car = Car.objects.create(
                license_plate=license_plate, parked_at=None, car_type='小型车')

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
    data = request.data
    user = request.user
    user_cars = user.cars.all()
    serializer = DeleteCarSerializer(data=data)

    if serializer.is_valid():
        data = serializer.validated_data
        license_plate = data.get('license_plate')
        car_to_remove = Car.objects.filter(license_plate=license_plate).first()

        if car_to_remove.parked_at:
            return Response({'success': False, 'error': '车辆还没出库'}, status=status.HTTP_201_CREATED)
        else:
            if car_to_remove in user_cars:
                user.cars.remove(car_to_remove)
                return Response({'success': True, 'message': '车辆已删除'}, status=status.HTTP_200_OK)
            return Response({'success': False, 'error': '车辆不存在'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'success': False, 'error': '数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 只有认证用户可以访问此视图
def reset_parking_duration(request):
    data = request.data
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
            parking_price = calculate_parking_price(
                parking_duration, car_to_reset.car_type)

            global_settings = GlobalSettings.objects.first()

            if global_settings:
                global_settings.parking_spots += 1
                global_settings.save()

            car_to_reset.parked_at = None
            car_to_reset.save()

            parking_record = ParkingRecord(car=car_to_reset, start_time=start_time,
                                           end_time=end_time, price=parking_price, license_plate=license_plate)
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
    if not request.user.is_superuser:  # 假设你的用户模型有一个 is_staff 字段来表示管理员状态
        return Response({'success': False, 'message': '只有管理员可以访问此视图'}, status=status.HTTP_403_FORBIDDEN)
    data = request.data
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


def convert_timeisoformat_to_querystring(timeisoformat,max_or_min:bool=False):
    time_object = date.fromisoformat(timeisoformat)
    if max_or_min:
        time_object = datetime.combine(time_object, datetime.max.time())
    else:
        time_object = datetime.combine(time_object, datetime.min.time())
    return timezone.make_aware(time_object,timezone=timezone.get_current_timezone())


@api_view(['GET'])
def query_parking_record_by_date_day(request):
    try:
        # 获取查询参数
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        start_datetime_with_tz = convert_timeisoformat_to_querystring(start_date_str,max_or_min=False)
        end_datetime_with_tz = convert_timeisoformat_to_querystring(end_date_str)
        # 查询匹配日期范围的停车记录
        parking_records = ParkingRecord.objects.filter(
            start_time__range=(start_datetime_with_tz, end_datetime_with_tz),
            end_time__range=(start_datetime_with_tz, end_datetime_with_tz)
        )

        total_cost = parking_records.aggregate(Sum('price'))['price__sum']
        max_cost = parking_records.aggregate(Max('price'))['price__max']
        
        # 使用序列化器将查询到的停车记录序列化为JSON格式
        serializer = ParkingRecordSerializer(parking_records, many=True)

        data = [item for item in serializer.data]
        for item in data:
            item['start_time'] = item['start_time'][11:16]
            item['end_time'] = item['end_time'][11:16]
            
        return Response({
            'success': True,
            'data': serializer.data,
            'number_of_records': parking_records.count(),
            'total_cost': total_cost,
            'max_cost': max_cost
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def monthly_income_api(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    # 将传入的日期字符串转换为日期对象
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    # 创建包含所有月份的日期范围
    date_range = [start_date_obj + timedelta(days=x*30) for x in range((end_date_obj - start_date_obj).days // 30 + 1)]
    
    start_date = convert_timeisoformat_to_querystring(start_date)
    end_date = convert_timeisoformat_to_querystring(end_date)

    # 查询指定时间段内每个月的收入总额
    monthly_income = ParkingRecord.objects.filter(
        start_time__gte=start_date,
        end_time__lte=end_date
    ).annotate(month=TruncMonth('start_time')).values('month').annotate(total_income=Sum('price'))
    
    # 创建包含所有月份的字典列表，初始化为0收入
    result = [{'date': date.strftime('%Y-%m'), 'income': 0} for date in date_range]
    
    # 更新结果中存在收入的月份的收入值
    for entry in monthly_income:
        month = entry['month'].strftime('%Y-%m')
        income = entry['total_income']
        for item in result:
            if item['date'] == month:
                item['income'] = income
    
    return Response(result)
    
@api_view(['GET'])
def daily_income_and_state_api(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    # 将传入的日期字符串转换为日期对象
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # 创建日期范围
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # 查询指定时间段内每一天的收入总额和停车次数
    daily_income = ParkingRecord.objects.filter(
        start_time__date__gte=start_date,
        end_time__date__lte=end_date
    ).values('start_time__date').annotate(
        total_income=Sum('price'),
        park_times=Count('id')
    )

    # 构建返回的字典列表，包括所有日期，即使收入为0
    result = []
    for date in date_range:
        matching_entry = next((entry for entry in daily_income if entry['start_time__date'] == date), None)
        if matching_entry:
            income = matching_entry['total_income']
            park_times = matching_entry['park_times']
        else:
            income = 0
            park_times = 0

        # 根据收入和停车次数计算"state"
        if income >= 100 and park_times >= 20:
            state = '优'
        elif income >= 50 and park_times >= 10:
            state = '良'
        else:
            state = '差'

        result.append({
            'date': date.strftime('%Y-%m-%d'),
            'income': income,
            'state': state,
            'park_times': park_times
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_parking_records(request):
    # Retrieve the currently authenticated user's parking records
    user = request.user
    user_cars = user.cars.all()
    parking_records = ParkingRecord.objects.filter(car__in=user_cars)

    serializer = ParkingRecordSerializer(parking_records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parking_spots(request):
    global_settings = GlobalSettings.objects.first()
    data = {
        'number': global_settings.parking_spots,
        'origin_number': global_settings.origin_parking_spots,
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def unpaid_cars(request):
    # Find cars with unpaid parking records
    unpaid_cars = Car.objects.filter(parked_at__isnull=False).distinct()

    # Serialize the unpaid cars and return as JSON
    serializer = CarSerializer(unpaid_cars, many=True)

    data = [item for item in serializer.data]
    for item in data:
        item['parked_at'] = item['parked_at'][11:16]
    return Response(data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def get_plate_number(request):

#     predict_api()
def export_parking_data(request):
    # 计算开始日期（当前日期向前推30天）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # 查询近30天的停车数据
    parking_data = ParkingRecord.objects.filter(
        start_time__date__gte=start_date,
        end_time__date__lte=end_date
    )

    # 创建CSV响应
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="parking_data.csv"'

    # 创建CSV写入器
    writer = csv.writer(response)

    # 写入CSV文件头
    writer.writerow(['start_time', 'end_time', 'price', 'license_plate'])

    # 写入停车数据
    for record in parking_data:
        writer.writerow([
            record.start_time,
            record.end_time,
            record.price,
            record.license_plate
        ])

    return response
