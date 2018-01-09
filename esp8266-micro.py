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

def http_get(host, path, port=80):
    return_data = ''
    addr = socket.getaddrinfo(host, port)[0][-1]
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

pin0 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
while True:
    wait_pin_change(pin0)
    if pin0.value() == 0:  # trig on press only
        print(pin0.value(), time.time())
        msg_data = http_get('192.168.1.130', '', port=5000)
        print(msg_data)
