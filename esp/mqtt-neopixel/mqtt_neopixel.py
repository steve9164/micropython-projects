import logging
from umqtt.simple import MQTTClient
import ubinascii
import machine
import json
import time
import micropython
micropython.alloc_emergency_exception_buf(100)


# Specifically for ESP32 with screen
import ssd1306
disp_reset = machine.Pin(16, machine.Pin.OUT)
disp_reset.value(0)
time.sleep_ms(100)
disp_reset.value(1)

i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4)) # Don't set Pins as Pin.OUT
display = ssd1306.SSD1306_I2C(128, 64, i2c)

import quokka_radio
hspi = machine.SPI(1, 1000000, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
nrf_slave_select = machine.Pin(27, machine.Pin.OUT)
nrf_slave_select.value(1)
r = quokka_radio.QuokkaRadio(nrf_slave_select, hspi)
r.config(channel=15)

_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
_THING_NAME = 'ESP8266-Quokka-LED'

# Subscription topics
_FULL_STATE_ON_UPDATE_TOPIC = '$aws/things/{}/shadow/update/documents'.format(
    _THING_NAME)
_DELTA_ON_UPDATE_TOPIC = '$aws/things/{}/shadow/update/delta'.format(
    _THING_NAME)

# Publish topics
_UPDATE_TOPIC = '$aws/things/{}/shadow/update'.format(_THING_NAME)


def connect():
    from aws_iot_private import keyfile, certfile, server, ca_cert
    with open(keyfile, 'r') as f:
        key = f.read()
    with open(certfile, 'r') as f:
        cert = f.read()
    client = MQTTClient(client_id=_CLIENT_ID, server=server, port=8883,  keepalive=4000,
                        ssl=True, ssl_params={"key": key, "cert": cert, "server_side": False})
    client.connect()

    return client


def generate_set_led_esp8266():
    led_pwm = machine.PWM(machine.Pin(2))
    led_pwm.freq(500)
    led_pwm.duty(1023)
    return lambda level: led_pwm.duty(1023-2**level)

def generate_set_led_esp32():
    led_pwm = machine.PWM(machine.Pin(25), freq=1000, duty=0)
    return lambda level: led_pwm.duty(2**level-1)


def report_updated(client, report):
    # Report back to AWS a successful state change
    report_dict = {
        "state": {
            "reported": report
        }
    }
    client.publish(_UPDATE_TOPIC, json.dumps(report_dict))
    
def wrap_text(text):
    display.fill(0)
    text_cropped = text[:16*8]
    for row in range(0, len(text_cropped)//16+1):
        display.text(text_cropped[row*16:(row+1)*16], 0, row*8)
    display.show()

def subscribe_to_delta(client, set_led):
    def sub_cb(topic, msg):
        print('{}: {}'.format(topic, msg))
        if topic.decode('utf-8') == _DELTA_ON_UPDATE_TOPIC:
            print('updating state')
            delta = json.loads(msg)['state']
            update_report = {}
            if 'led' in delta:
                set_led(delta['led'])
                update_report['led'] = delta['led']
            if 'text' in delta:
                wrap_text(delta['text'])
                update_report['text'] = delta['text']
            if 'neopixels' in delta:
                update_quokka_neopixels(delta['neopixels'])
                update_report['neopixels'] = delta['neopixels']
            report_updated(client, update_report)

    client.set_callback(sub_cb)

    print('Subscribing to topic {}'.format(_DELTA_ON_UPDATE_TOPIC))
    client.subscribe(_DELTA_ON_UPDATE_TOPIC)

    initial_state = '''
    {
        "state": {
            "reported": {
                "led": 1
            }
        }
    }
    '''

    client.publish(_UPDATE_TOPIC, initial_state)


def update_led(client, level):
    update_led_dict = {
        "state": {
            "desired": {
                "led": level
            }
        }
    }
    msg = json.dumps(update_led_dict)
    print('Publishing: {}'.format(msg))
    client.publish(_UPDATE_TOPIC, msg)

def update_quokka_neopixels(neopixel_bytes):
    r.send(neopixel_bytes)

def cs():
    client = connect()
    set_led = generate_set_led_esp32()
    subscribe_to_delta(client, set_led)
    return client

def check_messages(client):
    while True:
        client.check_msg()
        time.sleep_ms(20)

if __name__ == '__main__':
    # Run with `ampy run`
    print('Running as __main__')
    client = cs()
    check_messages(client)
    
