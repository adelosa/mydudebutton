import requests
from flask import Flask

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
    return get_text(r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)