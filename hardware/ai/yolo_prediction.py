import torch
import cv2
import numpy as np
import os

def yoloPrediction(img_path):
    weight_file_path = "./models/last.pt"
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight_file_path)
    img = cv2.imread(img_path)
    results = model(img)
    license_plate_box = results.xyxy[0][0].cpu().numpy().astype(np.int)[:4]
    x1, y1, x2, y2 = license_plate_box
    detected_license_plate = img[y1:y2, x1:x2]
    return detected_license_plate