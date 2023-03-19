# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
# 112.03.18加入
from flask_cors import CORS
from flask_sockets import Sockets

from linebot import (
    LineBotApi, WebhookParser,WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import paho.mqtt.client as mqtt

app = Flask(__name__)
# 112.03.18加入
CORS(app)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
#parser = WebhookParser(channel_secret)
handler = WebhookHandler('channel_secret')

#mqtt_client = Mqtt(app)
#socketio = SocketIO(app, cors_allowed_origins='*')
sockets = Sockets(app)
#bootstrap = Bootstrap(app)

@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        ws.send("Greetings from Render.com")
        time.sleep(1)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'

'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish("To/Feeder", "TEST_From_Render")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
'''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


if __name__ == "__main__":
    
    '''
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    '''
    
    # MQTT code is added on 112.03.04
    #client = mqtt.Client()
    #client.on_connect = on_connect
    #client.on_message = on_message
    #client.connect("broker.mqttdashboard.com", port = 1883)
    #client.loop_start()

    #app.run(debug=options.debug, port=options.port)
    #app.run(debug=True, port=5000)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    #socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
    print('server start')
    server.serve_forever()