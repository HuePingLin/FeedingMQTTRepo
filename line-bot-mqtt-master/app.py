from flask import Flask
import requests
import json
import os

app = Flask(__name__)
device_ID = "34021243701"
sensor_ID = "FeederController"
device_key = os.getenv("IOTDevice_Key",None)
update_data = []
url = "https://iot.cht.com.tw/iot/v1"
    
@app.route('/callback')
def UpdateData():
   iot_url = url + "/device/" + device_ID + "/rawdata"
   data = {'id':sensor_ID, 'save':True, 'value':['168']}
   update_data.append(data)
   json_data = json.dumps(update_data)
   headers = {"Content-Type":"application/json","CK":device_key}
   response = requests.post(iot_url, data = json_data, headers = headers)
   return str(response.status_code)


@app.route('/')
def hello_world():
    return 'Hello World! I am running on Render!'

if __name__ == '__main__':
    app.run(debug=True)