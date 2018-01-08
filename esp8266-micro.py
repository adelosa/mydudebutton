import machine
import socket
import ure
import time

def wait_pin_change(pin):
    cur_value = pin.value()
    active = 0
    while active < 10:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        time.sleep_ms(1)

def http_get(host, path):
    return_data = ''
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            return_data = return_data + str(data, 'utf8')
        else:
            break
    s.close()
    return return_data

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

pin0 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
while True:
    wait_pin_change(pin0)
    if pin0.value() == 0:  # trig on press only
        print(pin0.value(), time.time())
        web_data = http_get('www.pangloss.com','')
        msg = get_text(web_data)
        print(msg)
