import RPi.GPIO as GPIO
import json

def handleGPIOConfig():
    with open("./utils/config.json", encoding='utf-8') as meu_json: devices = json.load(meu_json)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(devices["outputs"][0]["gpio"], GPIO.OUT)
    GPIO.setup(devices["outputs"][1]["gpio"], GPIO.OUT)
    return devices
