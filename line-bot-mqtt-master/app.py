from flask import Flask
#import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_CLIENT_ID'] = 'myMqttClient'
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'SmartTaiwan'  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = 'SmartTaiwan'  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True
topic = 'hello/world'
topic2 = 'hello/world'

mqtt_client = Mqtt(app)

'''
def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    client.publish(topic2, "STARTING SERVER")
    client.publish(topic2, "CONNECTED")
    print("return code is {0}".format(str(rc)))


def on_message(client, userdata, msg):
    client.publish(topic2, "MESSAGE")
'''
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)
       
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    topic=message.topic,
    payload=message.payload.decode()
    print('Received message on topic: {} with payload: {}'.format(topic,payload))
    
@app.route('/publish')
def publish_message():
    mqtt_client.publish(topic2,"Hello")
    return "send message OK!"


@app.route('/')
def hello_world():
    return 'Hello World! I am running on Render!'

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=5000)