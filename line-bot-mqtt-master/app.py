from flask import Flask, request, abort
import requests
import json
import os
import sys
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)
device_ID = "34021243701"
sensor_ID = "FeederController"
device_key = os.getenv("IOTDevice_Key",None)
update_data = []
url = "https://iot.cht.com.tw/iot/v1"

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
parser = WebhookParser(channel_secret)

@app.route('/callback', methods=['POST'])
def UpdateData():
    command = 'AAA'
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
        
        #command = event.message.text

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    '''
    if len(command) > 0:
        iot_url = url + "/device/" + device_ID + "/rawdata"
        data = {'id':sensor_ID, 'save':True, 'value':['168']}
        data['value'].clear()
        data['value'].append(command)
        update_data.append(data)
        json_data = json.dumps(update_data)
        headers = {"Content-Type":"application/json","CK":device_key}
        response = requests.post(iot_url, data = json_data, headers = headers)
        return str(response.status_code)
    else:
        return "NO COMMAND!"
    '''
    return 'OK'


@app.route('/')
def hello_world():
    return 'Hello World! I am running on Render!'

if __name__ == '__main__':
    app.run(debug=True)