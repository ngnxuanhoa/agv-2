from flask import Flask, render_template, request, Response
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import cv2
import time
import atexit

app = Flask(__name__)

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Chân điều khiển động cơ
IN1, IN2 = 17, 18  # Motor trái
IN3, IN4 = 22, 23  # Motor phải
ENA, ENB = 12, 13  # PWM điều khiển tốc độ

# Thiết lập GPIO là output
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)
GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

# Tạo PWM
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(0)
pwmB.start(0)

# Khởi tạo camera (Picamera2)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

def generate_frames():
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(70)

def move_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(70)

def stop():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    command = request.form.get('command')
    if command == 'forward':
        move_forward()
    elif command == 'backward':
        move_backward()
    elif command == 'stop':
        stop()
    return "OK"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

def cleanup():
    print("Đang dừng camera và giải phóng GPIO...")
    picam2.stop()
    GPIO.cleanup()

atexit.register(cleanup)

