from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

import requests
import time

from .ai.detect_char import detectChar

import threading
import subprocess

import queue

PARKING_PRICE_PER_HOUR = 60000.000

ip_address = "192.168.74.123"

def create_ticket(request):
    url = 'http://' + ip_address + ':8000/api/tickets/create/'

    urlcam = 'http://192.168.74.182'

    fileName = 'img_cam1.jpg'
    r = requests.get(f'{urlcam}/capture?_cb={int(round(time.time() * 1000))})', stream = True)
    print(r.status_code)
    open(fileName, 'wb').write(r.content)

    q = queue.Queue()
    event = threading.Event()
    t = threading.Thread(target=run_detect, args=(q, fileName, event))
    t.start()

    event.wait()

    license_plate = q.get()

    if (license_plate == ""):
        return HttpResponse("0")

    else :
        time_in = datetime.now()
        data = {
            'license': license_plate,
            'timein': time_in,
            'ispaid': '0'
        }
        
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("hehe")

        remove_data(fileName)

        if response.status_code == 201:
            print("hehe")
            return HttpResponse("1")
        else:
            return HttpResponse("0")
        
    
def update_ticket(request):

    urlcam = 'http://192.168.74.20'

    fileName = 'img_cam2.jpg'

    r = requests.get(f'{urlcam}/capture?_cb={int(round(time.time() * 1000))})', stream = True)
    print(r.status_code)
    open(fileName, 'wb').write(r.content)

    q = queue.Queue()

    event = threading.Event()
    t = threading.Thread(target=run_detect, args=(q, fileName, event))
    t.start()

    event.wait()

    license_plate = q.get()

    get_ticket_url = 'http://' + ip_address + ':8000/api/tickets/get/' + license_plate + '/'

    response = requests.get(get_ticket_url)

    if response.status_code == 200:
        ticket_data = response.json()
        ticket_id = ticket_data['id']
        time_in = datetime.strptime(ticket_data['timein'], '%Y-%m-%dT%H:%M:%SZ')

        update_ticket_url = 'http://' + ip_address + ':8000/api/tickets/update/' + str(ticket_id) + '/'

        time_out = datetime.now()

        totaltime = time_out - time_in
        totalhours = totaltime.total_seconds() / 3600
        totalmoney = totalhours * PARKING_PRICE_PER_HOUR
        total = round(totalmoney, -3)

        data = {
                'timeout': time_out,
                'total': total,
                'ispaid': '1'
            }

        response = requests.put(update_ticket_url, data)

        remove_data(fileName)

        if response.status_code == 200:
            return HttpResponse("1")
        else:
            return HttpResponse("0")
    
    else:
        return HttpResponse("0")



def run_detect(q, path, event):

    e = threading.Event()
    q1 = queue.Queue()

    weight = "E:/PBL5/server/hardware/ai/models/last.pt"
    img_size = 416
    conf = 0.25
    source = path
    command = f"python E:/PBL5/server/hardware/ai/yolov5/detect.py --weight {weight} --img {img_size} --conf {conf} --source {source}"
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True, text=True)

    img_path = "E:/PBL5/server/hardware/ai/yolov5/images.jpg"

    t = threading.Thread(target=detectChar, args=(q1, img_path, e))
    t.start()
    e.wait()

    license = q1.get()

    print(license)
    event.set()
    q.put(license)

def remove_data(path):

    file_path = [path,
                 "E:/PBL5/server/hardware/ai/yolov5/images.jpg"]

    for i in file_path:
        with open(i, 'w') as f:
            f.seek(0)
            f.truncate()


