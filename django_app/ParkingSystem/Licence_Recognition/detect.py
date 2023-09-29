import argparse
import json
from .models.experimental import *
from .utils.datasets import *
from .utils.utils import *
from .models.LPRNet import *


loaded_models = {}
def initialize_model():
    class Opt:
        pass

    # Initialize an Opt instance
    opt = Opt()

    # Load parameters from a JSON file
    json_file_path = './config.json'  # Replace with the path to your JSON file
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Update the opt variable with JSON values
    for key, value in json_data.items():
        setattr(opt, key, value)

    # Now, you can access the parameters as attributes of the opt variable
    global loaded_models

    # Check if the models are already loaded
    if 'model' in loaded_models and 'modelc' in loaded_models:
        return loaded_models['model'], loaded_models['modelc'], loaded_models['imgsz']

    # Initialize
    device = torch_utils.select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load yolov5 model
    model = attempt_load(opt.det_weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier (recognition model)
    modelc = LPRNet(lpr_max_len=8, phase=False, class_num=len(CHARS), dropout_rate=0).to(device)
    modelc.load_state_dict(torch.load(opt.rec_weights, map_location=torch.device('cpu')))
    print("Load rec pretrained model successful!")
    modelc.to(device).eval()

    # Store the models in the cache
    loaded_models['model'] = model
    loaded_models['modelc'] = modelc
    loaded_models['imgsz'] = imgsz

    return model, modelc, imgsz, half

def detect(model, modelc, opt, imgsz, half, source):

    dataset = LoadImages(source, img_size=imgsz)
    # Run demo
    img = torch.zeros((1, 3, imgsz, imgsz), device=opt.device)  # init img
    _ = model(img.half() if half else img) if opt.device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(opt.device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img, augment=opt.augment)[0]
        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)


        # Apply Classifier
        pred, plat_num = apply_classifier(pred, modelc, img, im0s)


        # Process detections
        results = []
        for i, det in enumerate(pred):
            if det is not None and len(det):
                result_per_image = []
                for de, lic_plat in zip(det, plat_num):
                    *xyxy, conf, cls = de
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    lb = ""
                    for a, i in enumerate(lic_plat):
                        lb += CHARS[int(i)]
                    label = '%s %.2f' % (lb, conf)
                    result_per_image.append({
                        "class": int(cls),
                        "xywh": xywh,
                        "label": label
                    })
            results.append(result_per_image)
        # Convert the list of detection results to a JSON string
        json_str = json.dumps(results)
        return json_str

def predict_api(source):
    model, modelc, imgsz, half= initialize_model()
    json_str = detect(model=model, modelc=modelc, imgsz=imgsz,source=source,half=half)
    return json_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classify', nargs='+', type=str, default=True, help='True rec')
    parser.add_argument('--det-weights', nargs='+', type=str, default='./weights/yolov5_best.pt', help='model.pt path(s)')
    parser.add_argument('--rec-weights', nargs='+', type=str, default='./weights/lprnet_best.pth', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='./demo/images/', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='demo/rec_result', help='rec_result folder')  # rec_result folder
    parser.add_argument('--img-size', type=int, default=640, help='demo size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented demo')
    parser.add_argument('--update', action='store_true', help='update all models')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt', 'yolov3-spp.pt']:
                detect()
                create_pretrained(opt.weights, opt.weights)
        else:
            detect()
