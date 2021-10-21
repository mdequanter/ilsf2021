import paho.mqtt.client as mqttclient
import time
import naoqi
from naoqi import ALProxy

action = "sleep"

nao_host = "localhost"
nao_port = 9559


def on_message(client, userdata, message):
    action = str(message.payload.decode("utf-8"))
    message =  str(message.payload.decode("utf-8"))

    if (message.topic == "POSTURE"):
        if ()


    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

def index():
    return "Hello, I am Nao"


broker = "192.168.0.9"
client=mqttclient.Client("Client1")
client.connect(broker)
client.publish("NAO","HELLO")
client.loop_start() #start the loop
client.subscribe("NAO")
client.subscribe("POSTURE")
client.on_message=on_message #attach function to callback
time.sleep(1000)
client.loop_stop() #stop the loop

