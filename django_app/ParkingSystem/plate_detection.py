# lpr_api/plate_detection.py
import argparse
import torch
from models.experimental import *
from utils.datasets import *
from utils.utils import *
from models.LPRNet import *

# 加载模型
def load_models():
    # 车牌字符识别的参数设置
    parser = argparse.ArgumentParser()
    parser.add_argument('--classify', nargs='+', type=str, default=True, help='True rec')
    parser.add_argument('--det-weights', nargs='+', type=str, default='./weights/yolov5_best.pt', help='model.pt path(s)')
    parser.add_argument('--rec-weights', nargs='+', type=str, default='./weights/lprnet_best.pth', help='model.pt path(s)')
    parser.add_argument('--output', type=str, default='demo/rec_result', help='rec_result folder')  # rec_result folder
    parser.add_argument('--img-size', type=int, default=640, help='demo size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    opt = parser.parse_args()

    # Load yolov5 model
    device = torch_utils.select_device(opt.device)
    model = attempt_load(opt.det_weights, map_location=device)  # load FP32 model
    print("load det pretrained model successful!")

    # Second-stage classifier 也就是rec 字符识别
    if opt.classify:
        modelc = LPRNet(lpr_max_len=8, phase=False, class_num=len(CHARS), dropout_rate=0).to(device)
        modelc.load_state_dict(torch.load(opt.rec_weights, map_location=torch.device('cpu')))
        print("load rec pretrained model successful!")
        modelc.to(device).eval()

    return model, modelc

# 执行车牌字符识别
def run_plate_detection(opt, source):
    model, modelc = load_models()

    # 这里可以将您的字符识别代码整合进来
    # ...

    return "识别结果"  # 替换为实际的识别结果

