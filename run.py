#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_script import Manager
from time import time, sleep
import hardware
import threading
import config

app = Flask(__name__)
app.config.from_object(config)
manager = Manager(app)

#
# 定义全局变量
# 如果motor_status已定义，则打印它的值，若没有定义motor_status，则定义motor_status
try:
    print(motor_status)
    print("打印已定义步进动机状态值")
except:
    motor_status = "stop"



@app.route('/')
def index():
    return render_template("index.html")

def motor_run():
    global motor_status
    motor = hardware.motor()
    motor.motor_start()
    while motor_status=="start":
        pass
    

# 控制motor的URL
@app.route('/motor')
def motor():
    global motor_status
    motor_order = request.args.get("motor_order")

    if (motor_order=="start") and (motor_status!="start"):
        
        motor_status = "start"
        # 给动机启动函数分配线程
        t = threading.Thread(target=motor_run, args=())
        # 用start()方法执行线程
        t.start()
        sleep(0.002)
        print("启动电机")

    elif (motor_order=="start") and (motor_status=="start"):
        print("电机已启动")
        

    if (motor_order=="stop") and (motor_status!="stop"):

        motor = hardware.motor()
        motor.motor_stop()
        print("停止动机")
        motor_status = "stop"

    elif (motor_order=="stop") and (motor_status=="stop"):
       print("电机已停止")

    return motor_status

@app.route('/ultrasound')
def ultrasound():
    ultrasound = hardware.ultrasound()
    distance = ultrasound.get_distance_cm()
    return str(distance)


if __name__ == '__main__':
    manager.run()
