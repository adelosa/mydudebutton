import os
import boto3
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_text(web_data):
    lines = web_data.split('\n')
    nextline = False
    output = ''
    for line in lines:
        if line.startswith('</font>'):
            break
        if nextline:
           output = output + line
        if line.startswith('<font size="+2">'):
           nextline = True
    return output.split('<br')[0]

@app.route('/')
def index():
    r = requests.get('http://www.pangloss.com')
    message = get_text(r.text)
    if os.environ.get('MYDUDE_NUMBER'):
        send_sms(os.environ['MYDUDE_NUMBER'], message)
        print('message sent to {}'.format(os.environ['MYDUDE_NUMBER']))
    return jsonify(message=message)

def send_sms(phone, message):
    client = boto3.client('sns')
    response = client.publish(
    PhoneNumber=phone,
    Message=message,
    MessageAttributes={
        'AWS.SNS.SMS.SenderID': {
            'DataType': 'String',
            'StringValue': 'MYDUDE',
        },
        'AWS.SNS.SMS.SMSType': {
            'DataType': 'String',
            'StringValue': 'Promotional',
        },
    }
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)