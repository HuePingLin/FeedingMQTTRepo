from flask import Flask, request, abort
import requests
import json
import os
import sys
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent, UnknownEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
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
#parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#######################################################################

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    command = ''
    
    if len(text) > 0 and text.upper() == "ON":
        command = text.upper()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    
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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ON':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='Start feeding.'))
        command = event.postback.data
        iot_url = url + "/device/" + device_ID + "/rawdata"
        data = {'id':sensor_ID, 'save':True, 'value':['168']}
        data['value'].clear()
        data['value'].append(command)
        update_data.append(data)
        json_data = json.dumps(update_data)
        headers = {"Content-Type":"application/json","CK":device_key}
        response = requests.post(iot_url, data = json_data, headers = headers)
        return str(response.status_code)
    elif event.postback.data == 'VIEW':
        pass
    elif event.postback.data == 'EXIT':
        command = event.postback.data
        SendDataToIoTPlatform(command)
    else:
        pass

def SendDataToIoTPlatform(command):
    if len(message) > 0:
        iot_url = url + "/device/" + device_ID + "/rawdata"
        data = {'id':sensor_ID, 'save':True, 'value':['168']}
        data['value'].clear()
        data['value'].append(command)
        update_data.append(data)
        json_data = json.dumps(update_data)
        headers = {"Content-Type":"application/json","CK":device_key}
        response = requests.post(iot_url, data = json_data, headers = headers)
        return str(response.status_code)

'''
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
        
        command = event.message.text

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    
    iot_url = url + "/device/" + device_ID + "/rawdata"
    data = {'id':sensor_ID, 'save':True, 'value':['168']}
    if len(command) > 0:
        data['value'].clear()
        data['value'].append(command)
        update_data.append(data)
    else:
        update_data.append(data)
    json_data = json.dumps(update_data)
    headers = {"Content-Type":"application/json","CK":device_key}
    response = requests.post(iot_url, data = json_data, headers = headers)
    
    return str(response.status_code)
'''

@app.route('/')
def hello_world():
    return 'Hello World! I am running on Render!'

if __name__ == '__main__':
    app.run(debug=True)