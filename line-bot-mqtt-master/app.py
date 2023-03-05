import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Hello World!</h1>'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
if __name__ == '__main__':
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com",1883,keepalive=60)
    client.loop_start()
    
    app.run()