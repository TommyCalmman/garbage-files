import paho.mqtt.client as mqtt
import time
import base64
import json
import numpy as np
import os
import cv2 as cv
print('started')
#msd/event/6f5d8c9228fec651/wav
#msd/event/6f5d8c9228fec651/json
#y = json.loads(x)
if not os.path.exists('photos'):
    os.mkdir('photos')
if not os.path.exists('data'):
    os.mkdir('data')

def on_message(client, userdata, message):
    print(message.topic)
    time_= time.asctime()
    parsed_topic = message.topic.split('/')
    if parsed_topic[-1] == 'json':
        #with open(f'data/json_{time_}', 'w') as f:
        #    f.write(str(message.payload.decode("utf-8")))
        jpg_ = json.loads(message.payload.decode("utf-8"))['image_base64']
        #print(jpg_)
        with open(f'/var/www/service-energy.space/html/static/img_03.5cb1f813a3cd37debd60.jpg', 'wb') as f:
            f.write(base64.decodebytes(jpg_.encode('utf-8')))
        ir_array = json.loads(message.payload.decode("utf-8"))['data_ir']
        print(ir_array)
        ir_array = ir_array.replace('[', '')
        ir_array = ir_array.replace(']', '')
        ir_array = ir_array.replace(',', '')
        ir_array = ir_array.replace(';', '')
        ir_array = ir_array.replace('\n', ' ')
        arr = np.array(ir_array.split(' '))
        arr = arr[arr != '']
        arr = arr.astype(np.float64)
        ir_matrix = arr.reshape(24, 32)
        ir_matrix = cv.normalize(ir_matrix, None, 0, 255, cv.NORM_MINMAX)
        ir_matrix = np.uint8(ir_matrix)
        ir_matrix = cv.resize(ir_matrix, (240, 320), cv.INTER_CUBIC)
        ir_matrix = cv.applyColorMap(ir_matrix, cv.COLORMAP_JET)
        suc, img_buff_arr = cv.imencode(".jpg", ir_matrix)
        with open(f'/var/www/service-energy.space/html/static/img_04.9891c8516c6fdd2f99f2.jpg', 'wb') as f:
            f.write(img_buff_arr.tobytes())
    #elif parsed_topic[-1] == 'wav':
    #    with open(f'data/wav_{time_}.wav', 'wb') as f:
    #        f.write(message.payload)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("msd/event/6f5d8c9228fec651/json")

mqttBroker = "service-energy.space"
client = mqtt.Client("Artem")
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttBroker)
client.loop_forever()