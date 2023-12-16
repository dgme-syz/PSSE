import os, sys, torch
from PIL import Image
from pathlib import Path

base_dir = Path(__file__).parent.absolute().__str__()
save_dir = os.path.join(base_dir, "Trained")

sys.path.append(base_dir)
from model import ResNet18
net = ResNet18(num_classes=2)

from datasets_.data_utils import preprocess
assert "best_model.pt" in os.listdir(save_dir)
net.load_state_dict(torch.load(os.path.join(save_dir, "best_model.pt")))
net.eval()

def dectect(img):
    if isinstance(img, str):
        out = preprocess(Image.open(img)).unsqueeze(0)
    else:
        out = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        out = net(out)
    res = torch.argmax(out, dim=1).item()
    # print(res)
    return res

if __name__ == '__main__':
    dectect(os.path.join(base_dir, "datasets_", "train_paking", "0", "spot65.jpg"))