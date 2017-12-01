import sys
import time
from importlib import import_module
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, Response
sys.path.append('/home/pi/networking')
from camera_pi import Camera
app = Flask(__name__, template_folder='Templates')

# Import the PCA9685 module.
import Adafruit_PCA9685
sys.path

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set frequency to 60hz
pwm.set_pwm_freq(60)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#shows index.html when root IP is selected
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#controls servos based on calls from the html
@app.route('/<pinpath>', methods=['POST'])
def rerout(pinpath):

    servo = int(pinpath)

    if servo == 1:
        print('Forwards')
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_min)

    elif servo == 2:
        print('Backwards')
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_max)

    elif servo == 3:
        print('Left')
        pwm.set_pwm(0,0,servo_max)
        pwm.set_pwm(1,0,servo_max)

    elif servo == 4:
        print('Right')
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_min)

    elif servo == 5:
        print('Hand Open')
        pwm.set_pwm(2,0,155)
        time.sleep(1)
        pwm.set_pwm(2,0,0)

    elif servo == 6:
        print('Hand Close')
        pwm.set_pwm(2,0,420)
        time.sleep(1)
        pwm.set_pwm(2,0,0)

    elif servo == 7:
        print('Stop')
        pwm.set_pwm(0,0,0)
        pwm.set_pwm(1,0,0)
        pwm.set_pwm(2,0,0)
    else:
        print('Stop')
        pwm.set_pwm(0,0,0)
        pwn.set_pwn(1,0,0)
        pwm.set_pwm(2,0,0)

    response = make_response(redirect(url_for('index')))
    return(response)
