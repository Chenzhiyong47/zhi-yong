import RPi.GPIO as GPIO
from time import time, sleep


class Ultrasound_Dist():
    def __init__(self, Trig_Pin=14, Echo_Pin=15):
        self.Trig_Pin = Trig_Pin
        self.Echo_Pin = Echo_Pin


    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Echo_Pin, GPIO.IN)

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
    def distance(self):
        # 给TRIG脚一个12μs的高电平脉冲,发出一个触发信号
        GPIO.output(self.Trig_Pin, GPIO.HIGH)
        sleep(0.00012)
        GPIO.output(self.Trig_Pin, GPIO.LOW)
        while not GPIO.input(self.Echo_Pin):
            pass

        t1 = time()
        while GPIO.input(self.Echo_Pin):
            pass
        t2 = time()
        return (t2 - t1) * 34000 / 2
    
    def get_distance_cm(self):
        self.init()
        distance_cm = self.distance()
        GPIO.cleanup()

        return 'Distance: {0:.2f}'.format(distance_cm) + 'cm'

    # 这是一个在终端测试启动超声测距模块的函数
    def test_distance(self):
        try:
            self.init()
            while True:
                print('Distance:{0:.2f} cm'.format(self.distance()))
                #print('Distance:{1:.2f} cm'.format(self.checkdist()))
                sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
        print("End of test")
