import cv2, json, operator
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from models.Nodes import *
support_chinese()


"""
1. 得到所有道路转折点的坐标
2. 得到所有停车位标志点的坐标
3. 得到点与点之间的边
"""

def GetRoadPts():
    # 读取图像
    image = cv2.imread('./saveImg/raw.jpg')

    # 将图像转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义绿色的HSV范围
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # 根据阈值创建掩膜
    mask = cv2.inRange(hsv, lower_green, upper_green)
    height, width = mask.shape

    # 寻找连通块
    connectivity = 4  # 或8，具体根据你的需求来确定
    output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)

    imshow(mask, title="匹配绿色点")
    
    # 获取连通块属性
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    # print(stats[:, -1])

    threshold = 5

    for label in range(1, output[0]):
        if stats[label, cv2.CC_STAT_AREA] < threshold:  
            # 如果连通块的像素点数小于阈值，则将对应像素赋值为 0
            labels[labels == label] = 0
    new_mask = np.where(labels > 0, 255, labels).astype(np.uint8)

    imshow(new_mask, title="去除噪声连通块")

    List = []
    th_right = 1100

    # 去除图片中右边的绿植
    for y in range(height):
        for x in range(width):
            if x > th_right:
                new_mask[y, x] = 0  # 将对应位置的像素标签设为 0，即赋值为黑色

    imshow(new_mask, title="去除绿植")

    # 重新获得上图的连通块
    new_output = cv2.connectedComponentsWithStats(new_mask, connectivity, cv2.CV_32S)
    print(len(new_output[3]))

    # 写入json文件
    with open('./config/settings.json', 'r') as f:
        data = json.load(f)
    with open('./config/data_road.json', 'w') as f:
        data['cnt'] = len(new_output[3])

        res = [{"x": x, "y": y, "is_entrance": 0, "is_empty": 0, "id" : None, 
                    "is_parking": 0, "direction": 0} 
            for x, y in new_output[3]]
        # 特判两个入口
        # 一个入口靠最左边，一个靠最下边
        # x < 4.66 or y > 708
        for dict in res :
            if dict['x'] < 4.66 or dict['y'] > 708:
                dict['is_entrance'] = 1

        json.dump(res, f, indent=4)
    with open('./config/settings.json', 'w') as f:
        json.dump(data, f, indent=4)

def GetCarPts():
    # 使用matplotlib显示（rgb）图像，(注意，cv2读取的图片为bgr格式)
    img_bgr = cv2.imread('saveImg/scene1380.jpg')
    print(img_bgr.shape)
    imshow(img_bgr)
    image = img_bgr.copy()
    
    binary_img = binary_filter(image)  # 1）二值过滤，将图像mask 2）转灰度图
    edge_out = edge_detection(binary_img)  # 边缘检测,Canny边缘检测
    image_choose_pake = choose_pake(edge_out)  # 根据图片特征人为选取车库位置,通过固定的顶点绘制区域
    lines = hoff_lines(image_choose_pake)  # 霍夫变换，直线检测
    draw_line_image, cleaned_lines = draw_line(image, lines)  # 绘制直线
    line_group_image, line_group = line_grouping(image, cleaned_lines)
    seg_line_image, stop_dict = draw_seg_line(image, line_group)  # 切割每一个停车位
    gap = 15.5
    total= []
    img = img_bgr.copy()
    for x1, y1, x2, y2, key in stop_dict.keys():
        x, y = 0, 0
        if key == 1:
            # 标志点在右侧，则取矩形右上角坐标代表该个车位
            x = x2
            y = int(y2)
            cv2.circle(img, (x2, int(y2)), 3, (0, 0, 255), 2)  
        else:
            # 标志点在左侧，则取矩形左上角坐标代表该个车位
            x = x1
            y = int(y1 - gap)
            cv2.circle(img, (x1, int(y1 - gap)), 3, (0, 0, 255), 2)  
        total.append({"x": x, "y": y, "is_entrance": 0, "is_empty": 1, "id" : None, 
                    "is_parking": 1, "direction": key, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
        # 绘制位置,参数（图，图标大小，线粗细，颜色，图标编号）
    imshow(img)
    # 添加到文件
    with open('./config/settings.json', 'r') as f:
        data = json.load(f)
    with open('./config/data_lot.json', 'w') as f:
        data['cnt'] += len(total)
        json.dump(total, f, indent=4)
    with open('./config/settings.json', 'w') as f:
        json.dump(data, f, indent=4)

def GetEdge():
    # 读取图像
    img = cv2.imread('./saveImg/raw.jpg')

    # 转换为 HSV 颜色空间
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_lower1 = np.array([0, 70, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 70, 50])
    red_upper2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_img, red_lower1, red_upper1)
    mask2 = cv2.inRange(hsv_img, red_lower2, red_upper2)
    red_mask = mask1 + mask2

    # 使用形态学操作去除噪点
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    imshow(red_mask)

    rows, cols = red_mask.shape[:2]
    pot1 = [cols*0.2, rows*0.8]
    pot2 = [cols*0.2, rows*0.7]
    pot3 = [cols*0.34, rows*0.60]
    pot4 = [cols*0.57, rows*0.15]
    pot5 = [cols*0.8, rows*0.25]
    pot6 = [cols*0.8, rows*0.7]
    vertice = np.array([[pot1, pot2, pot3, pot4, pot5, pot6]], dtype = np.int32)
    cp_image = red_mask.copy()
    cp_image = cv2.cvtColor(cp_image, cv2.COLOR_GRAY2BGR)  # 灰度转BGR
    for pt in vertice[0]:
        cv2.circle(cp_image, (pt[0], pt[1]), 10, (0, 0, 255), 4)  
        # 绘制位置,参数（图，图标大小，线粗细，颜色，图标编号）
    print('choose_pake: 根据图片特征人为选取车库位置,通过固定的顶点绘制区域')
    imshow(cp_image)

    mask = np.ones_like(red_mask)
    if len(mask.shape) == 2:
        cv2.fillPoly(mask, vertice, 0)
        print('choose_pake: 绘制车库mask')
        imshow(mask)
    image_choose_pake = cv2.multiply(cv2.bitwise_and(red_mask, mask), 255)
    imshow(image_choose_pake)

    image = image_choose_pake.copy()
    imshow(image)
    # 寻找轮廓
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 找到所有连通分量的最左下方和最右上方的点
    components = []
    for contour in contours:
        left = min(contour[:, 0, 0])
        right = max(contour[:, 0, 0])
        bottom = min(contour[:, 0, 1])
        top = max(contour[:, 0, 1])
        
        components.append([[left, top], [right, bottom]])
    result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # 输出每个连通分量的最左下方和最右上方的点
    for i, (c1, c2) in enumerate(components):
        cv2.circle(result, c1, 5, (0, 0, 255), -1)
        cv2.circle(result, c2, 5, (0, 255, 0), -1)
    imshow(result)
    Nodes = read('./config/data.json') 
    Nodes_road = [x for x in Nodes if x.is_parking == 0]
    Nodes_lot = [x for x in Nodes if x.is_parking == 1]

    with open("./config/edge.txt", 'w') as f:
        for c1, c2 in components:
            L = Get_Nearest_Node(Nodes_road, c1)
            R = Get_Nearest_Node(Nodes_road, c2)
            f.write(f"{L}  {R}\n")
        for node in Nodes_lot:
            Nodes_up = [x for x in Nodes if x.y < node.y]
            Nodes_dn = [x for x in Nodes if x.y > node.y]
            U = Get_Nearest_Node(Nodes_up, node)
            D = Get_Nearest_Node(Nodes_dn, node)
            f.write(f"{U}  {node.id}\n")
            f.write(f"{D}  {node.id}\n")
    image_test = cv2.imread("./saveImg/scene1380.jpg")

    dic = {}
    for node in Nodes:
        dic[node.id] = node
        cv2.circle(image_test, (int(node.x), int(node.y)), 5, (0, 0, 255), thickness=2)
    imshow(image_test)

    edges = []

    with open("./config/edge.txt", "r") as f:
        for line in f:
            edges.append(map(int, line.strip().split()))

    for x, y in edges:
        cv2.line(image_test, (int(dic[x].x), int(dic[x].y)), (int(dic[y].x), int(dic[y].y)), 
                (0, 0, 255), thickness=2)
    imshow(image_test)
    print("cnt of edges: ", len(edges))

def GetId():
    """
    前面的点为车位标志点，后面所有点为道路转折点
    """
    # 整合 data_road data_lot 得到所有节点的 json 并赋予标号
    total = 0

    with open("./config/settings.json", 'r') as f:
        total = json.load(f)['cnt']
    data = []

    with open("./config/data_lot.json", "r") as f:
        data.extend(json.load(f))
    with open("./config/data_road.json", "r") as f:
        data.extend(json.load(f))
        
    assert(len(data) == total)

    # 给予连续标号从0开始
    idx = 0

    for i in range(total):
        data[i]['id'] = idx
        idx += 1
    # 写入 data.json
    with open("./config/data.json", "w") as f:
        json.dump(data, f, indent=4)
    # 写一个文件记录，起点1映射到哪个id
    START = []
    for item in data:
        if item['is_entrance']:
            START.append(item['id'])
    with open("./config/START.json", "w") as f:
        json.dump(START, f, indent=4)

if __name__ == '__main__':
    GetRoadPts()
    GetCarPts()
    GetId()
    GetEdge()