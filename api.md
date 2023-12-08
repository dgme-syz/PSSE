### 1.  进入

*拍摄车辆 => 前端发送带图片的 post 请求 => 后端调用模型识别车辆图片的车牌号 => 车牌信息传回前端*

接下来，前端发送一个 `post` 请求到  `/api/in/`，发送信息为 ：

```
{
    'license_plate' : 'XXXXXXX',
}
```



> 使用 `response.data` 访问上面的数据

* `license_plate` : 暂设定为 **NU123456** (2英文 + 6数字)


> 你将上传数据添加到现有停车场数据库，然后做其它处理，至于为什么不在得到车牌号直接处理，如果你把 **识别图片** 与 **这个api** 合起来写也可以

后端顺便返回一个表单 :

```
{
    BOHI : 1122, // 近一小时内收入
    BODI : 1233, // 近一天收入
    BOMI : 114514, // 近一月收入
}
```
> 希望我直接能通过类似 `response.BOHI` 访问数据

### 2. 出去

*拍摄车辆 => 前端发送带图片的 post 请求 => 后端调用模型识别车辆图片的车牌号 => 车牌信息传回前端*

接下来，前端发送一个 `post` 请求到  `/api/out/`，发送信息为 ：

```
{
    'license_plate' : 'XXXXXXX',
}
```

然后，希望后端返回一个 `json` 形式的表单 

```
{
    'cost' : xxx,
    'success' : True,
     BOHI : 1122, // 近一小时内收入
     BODI : 1233, // 近一天收入
     BOMI : 114514, // 近一月收入
}
```



* `cost ` : 本次收费多少，浮点数
* `success` : 是否成功收到请求



### 3. 其它


#### 3.0 提供一个能返回某一时间段的具体到每一月的收入总额

前端会发送一个 `post` 请求到  `/api/monthly_income_api/`，发送信息为 ：

``` query_param 不是body
{
    'start_date' : 'xxxxxxx'
    'end_date' : 'xxxxxxx'
}
```
> `times` 考虑为最完整的时间 **2023-10** (具体到月份)

返回： 不包括end_date

```
[
	{
		'date' : '2023-01',
		'income' : 112313,
	}
	{
		'date' : '2023-02',
		'income' : 112313,
	}
	...
]
```

#### 3.1 提供一个能返回某一时间段的具体到每一天的收入情况

前端会发送一个 `post` 请求到  `/api/daily_income_and_state_api/`，发送信息为 ：

```
{
    'start_date' : 'xxxxxxx'
    'end_date' : 'xxxxxxx'
}
```

* 时间的格式为 :  **2023-10-09** (具体到天，不是秒)

希望后端返回的是类似 ：
包括end_date

```
[
	{
    "date": "2023-10-01",
    "income": 0,
    "state": "差",
    "park_times": 0
  },
  {
    "date": "2023-10-02",
    "income": 0,
    "state": "差",
    "park_times": 0
  },
	...
]
```

* `income` : 2位小数浮点数
* `state` : 后端自己设 2 个阈值，**if-else** 判断一下，输出到表单
* `park_times` : 整型



#### 3.2 提供现在停车场内车辆信息

前端会发送一个 `get` 请求到  `/api/unpaid_cars/`

希望后端返回，当前停车场内车辆的以下数据 
```
[
  {
    "license_plate": "苏1234567",
    "car_type": "小型车",
    "parked_at": "11:57"
  }
	...
]
```

> 希望能截断没用的时间，只留下 `24h` 时间制 的字符串



#### 3.3 提供今天所有的停车记录

前端会发送一个 `get` 请求到  `/api/query_parking_record_by_date_day/`

希望后端返回，今天内停车场内所有类似下面的停车记录

```
{
  "success": true,
  "data": [
    {
      "start_time": "11:39",
      "end_time": "11:40",
      "price": "5.00",
      "license_plate": "苏1234567"
    },
    {
      "start_time": "11:40",
      "end_time": "11:40",
      "price": "5.00",
      "license_plate": "苏1234567"
    }
  ],
  "number_of_records": 2,
  "total_cost": 10.0,
  "max_cost": 5.0
}



```
* `number_of_records` ： 今天停车记录的条数
* `total_cost` : 该条停车记录得到的收入
* `max_cost` ： 今天停车记录中收入最大值



#### 3.4 提供近30天停车数据的下载链接

前端会发送一个 `get` 请求到  `/api/export_parking_data/`

希望后端会返回一个下载链接指向这个文件，下载的文件包括 **30天停车数据** ，基本内容形式与 `3.3` 描述内容一致，只有data部分，是个excel文件



















