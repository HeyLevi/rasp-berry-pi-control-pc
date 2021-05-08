#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker import Blinker, BlinkerButton, BlinkerNumber
from Blinker.BlinkerDebug import *
import os

auth = 'Secret Key'

BLINKER_DEBUG.debugAll()

Blinker.mode("BLINKER_WIFI")
Blinker.begin(auth)

button1 = BlinkerButton("btn-abc")
number1 = BlinkerNumber("num-abc")

counter = 0

def button1_callback(state):
    global counter # 引入counter变量
    BLINKER_LOG('get button state: ', state)
    a = os.system("ping -c 1 www.bing.com") # 使用系统命令ping www.bing.com
    counter += 1 # counter + 1
    button1.text(a) # 设置按钮文字
    button1.print(state) # 发送数据，调整button1
    number1.print(counter) # 发送数据，调整number1

def data_callback(data):
    global counter
    
    BLINKER_LOG("Blinker readString: ", data)
    counter += 1
    number1.print(counter)

button1.attach(button1_callback)
Blinker.attachData(data_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
