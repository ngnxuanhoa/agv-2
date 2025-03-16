import os
import time
import RPi.GPIO as GPIO
from flask import Flask, request, jsonify

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Chân điều khiển động cơ
IN1, IN2 = 17, 18  # Motor trái
IN3, IN4 = 22, 23  # Motor phải
ENA, ENB = 12, 13  # PWM điều khiển tốc độ

# Thiết lập GPIO là output
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

# PWM để điều khiển tốc độ
pwm_A = GPIO.PWM(ENA, 1000)
pwm_B = GPIO.PWM(ENB, 1000)
pwm_A.start(0)
pwm_B.start(0)

def set_motor_speed(speed):
    duty_cycle = max(0, min(100, speed))  # Giới hạn từ 0 - 100%
    pwm_A.ChangeDutyCycle(duty_cycle)
    pwm_B.ChangeDutyCycle(duty_cycle)

def move_forward(speed=50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_motor_speed(speed)

def move_backward(speed=50):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_motor_speed(speed)

def turn_left(speed=50):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_motor_speed(speed)

def turn_right(speed=50):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_motor_speed(speed)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    set_motor_speed(0)

app = Flask(__name__)

@app.route('/control', methods=['POST'])
def control_agv():
    data = request.json
    command = data.get('command')
    speed = data.get('speed', 50)
    
    if command == 'forward':
        move_forward(speed)
    elif command == 'backward':
        move_backward(speed)
    elif command == 'left':
        turn_left(speed)
    elif command == 'right':
        turn_right(speed)
    elif command == 'stop':
        stop()
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'}), 400
    
    return jsonify({'status': 'success', 'command': command, 'speed': speed})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()
