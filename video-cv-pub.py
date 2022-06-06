# Importing Libraries
import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time# Raspberry PI IP address
MQTT_BROKER = "service-energy.space"
MQTT_SEND = "test123"
cap = cv.VideoCapture(0)
client = mqtt.Client()
client.connect(MQTT_BROKER)
try:
 while True:
  start = time.time()
  time.sleep(0.45)
  _, frame = cap.read()
  _, buffer = cv.imencode('.jpg', frame)
  jpg_as_text = base64.b64encode(buffer)
  client.publish(MQTT_SEND, jpg_as_text)
  end = time.time()
  t = end - start
  fps = 1/t
  print(fps)
except:
 cap.release()
 client.disconnect()