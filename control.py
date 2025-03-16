import RPi.GPIO as GPIO
import time

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
