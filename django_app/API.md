# USER
## 发送验证码
    /api/send_verification_code
### INPUT
    {
        "email": "admin@example.com"
    }
### OUTPUT
    {
        "success": True
    }
## 登录
    /api/login
### INPUT
    {
        "email": "admin@example.com",
        "password": "admin"
    }
### OUTPUT
    {
        "success": True,
        "message": "登录成功" / "用户名或密码错误"
    }

## 注册
    /api/register
### INPUT
    {
        "email": "admin@example.com",
        "username": "admin"
        "password": "admin"
        "code": "123456"
    }
### OUTPUT
    {
        "success": True,
        "message": "注册成功" / "验证码错误" / "邮箱已被注册" / "请先获取验证码" / "验证码已过期，请重新获取"
    }
## 修改密码
    /api/change_password
### INPUT
    {
        "code": "123456",
        "old_password": "admin",
        "new_password": "admin1"
    }
### OUTPUT
    {
        "success": True,
        "message": "修改成功" / "验证码不正确或已过期。" / "旧密码不正确。"
    }

# 车辆

## 登记车辆
    /api/add_car
### INPUT
    {
        "license_plate": "京A12345",
        "car_type": "小型车", //小型车，中型车，大型车
    }
### OUTPUT
    {
        "success": True,
        "message": "登记成功"200 / "车牌号已存在"201
    }
## 停车
    /api/park_car
### INPUT
    {
        "license_plate": "京A12345"
    }
### OUTPUT
    {
        "success": True,
        "message": "停车成功"200 / "车牌号不存在"201 / "车辆已经停车" 400  / "停车场已满" 401 / "数据验证失败" 400
    }
## 取车
    /api/reset_parking_duration
### INPUT
    {
        "license_plate": "京A12345"
    }
### OUTPUT
    {
        "success": True,
        "message": "取车成功"200 / "车辆不存在或者尚未停车"404 / "数据验证失败" 400
    }
## 注销登记
    /api/delete_car
### INPUT
    {
        "license_plate": "京A12345"
    }
### OUTPUT
    {
        "success": True,
        "message": "注销成功"200 / "车辆不存在"404 / "数据验证失败" 400 / "车辆还没出库" 201
    }
## 修改停车价格
    /api/update_parking_price
### INPUT
    {
        "car_type": "小型车",
        "new_price": 10
    }
### OUTPUT
    {
        "success": True,
        "message": "修改成功"200 / "车型不存在" 400 / "不是管理员" 403
    }
# 查询
## 根据日期查记录
    /api/query_parking_record_by_date
### INPUT
    {
        "start_time": "2023-09-29"
        "end_time": "2023-09-29""
    }
### OUTPUT
    {
        'success': True,
        'data': serializer.data,
        'number_of_records': parking_records.count(),
        'total_cost': str(total_cost)
    }
    serializer.data:{
        car,
        start_time,
        end_time,
        price,
        license_plate
    }
## 停车位
    /api/get_parking_spots
### OUTPUT
    {
        "number": number,
        "origin_number": origin_number
    }