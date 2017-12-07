#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import time, sleep


# 设置树莓派IO引脚模式
class IO_Model:
    def model_init(self):
        GPIO.setmode(GPIO.BCM)
        print("IO设置为BCM模式")

    def model_clear(self):
        GPIO.cleanup()
        print("清除IO模式")


# 步进电机的操作
class motor:
    def __init__(self, PUL_FRE=10000, DIR_FRE=100, PUL_IN=20, DIR_IN=21):
        # PUL_FRE: 给端口PUL-的脉冲信号(/s)  PUL_IN: PUL-接的引脚编号
        # DIR_FRE: 给端口DIR-的脉冲信号(/s)  DIR_IN: DIR-接的引脚编号
        self.PUL_FRE = PUL_FRE
        self.DIR_FRE = DIR_FRE
        self.PUL_IN = PUL_IN
        self.DIR_IN = DIR_IN

        self.motor_init()

        # 设置PUL-和DIR-的PWM脉冲值
        self.PUL_PWM = GPIO.PWM(self.PUL_IN, self.PUL_FRE)
        self.DIR_PWM = GPIO.PWM(self.DIR_IN, self.DIR_FRE)

    def motor_init(self):
        GPIO.setup(self.PUL_IN, GPIO.OUT)
        GPIO.setup(self.DIR_IN, GPIO.OUT)
        # print("电机接线引脚初始化完毕")

    def motor_start(self):
        self.PUL_PWM.start(50)
        self.DIR_PWM.start(50)
        print("启动步进动机")

    def motor_stop(self):
        self.PUL_PWM.stop()
        self.DIR_PWM.stop()
        print("停止步进动机")


# 超声测距操作
class ultrasound:
    def __init__(self, TRIG_IN=14, ECHO_IN=15):
        # TRIG_IN、ECHO_IN 是超声连接树莓派IO的引脚
        self.TRIG_IN = TRIG_IN
        self.ECHO_IN = ECHO_IN

        self.ultrasound_init()

    def ultrasound_init(self):
        GPIO.setup(self.TRIG_IN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ECHO_IN, GPIO.IN)
        # print("超声接线引脚初始化完毕")
        sleep(0.1)

    '''
    这是一个超声测距模块的测量转换函数，它的原理是先向TRIG脚输入至少10us的触发信号,
    该模块内部将发出 8 个 40kHz 周期电平并检测回波。一旦检测到有回波信号则ECHO输出
    高电平回响信号。回响信号的脉冲宽度与所测的距离成正比。由此通过发射信号到收到的回
    响信号时间间隔可以计算得到距离。公式: 距离=高电平时间*声速(34000cm/S)/2。返回一个
    测量值（单位是cm）
    其中：
        t1是发现Echo脚收到高电平时的瞬时时间
        t2是发现Echo脚由高电平变为低电平时的瞬时时间
        t2-t1 就是Echo检测到高电平的时间
    '''
    def get_distance_cm(self):
        # 给TRIG脚一个12μs的高电平脉冲,发出一个触发信号
        GPIO.output(self.TRIG_IN, GPIO.HIGH)
        sleep(0.00012)
        GPIO.output(self.TRIG_IN, GPIO.LOW)
        while not GPIO.input(self.ECHO_IN):
            pass

        t1 = time()
        while GPIO.input(self.ECHO_IN):
            pass
        t2 = time()
        distance = (t2 - t1) * 34000 / 2

        # 返回一个距离数值，保留两位小数
        return float('%.2f' % distance)

# 当导入模块的时候，就设置引脚模式
IO_MODEL = IO_Model()
IO_MODEL.model_init()

