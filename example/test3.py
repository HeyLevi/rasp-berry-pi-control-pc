#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerNumber, BlinkerMIOT
from Blinker.BlinkerConfig import *
from Blinker.BlinkerDebug import *
import os

auth = '3bac28c1fcdf'

BLINKER_DEBUG.debugAll()

Blinker.mode('BLINKER_WIFI')
Blinker.miotType('BLINKER_MIOT_OUTLET')
Blinker.begin(auth)

button1 = BlinkerButton('btn-abc')
number1 = BlinkerNumber('num-abc')

counter = 0
oState = 'on'

def miotPowerState(state):
    global oState
    global counter
    BLINKER_LOG('need set power state: ', state)
    oState = state
    BlinkerMIOT.powerState(state)
    BlinkerMIOT.print()
    if state == 'true':
        os.system("ping -c 4 www.bing.com") # 使用系统命令ping www.bing.com
        counter += 2 # counter + 2
    elif state == 'false':
        os.system("ping -c 1 www.bing.com") # 使用系统命令ping www.bing.com
        counter -= 1 # counter + 2
    button1.text(state) # 设置按钮文字
    button1.print(state) # 发送数据，调整button1
    number1.print(counter) # 发送数据，调整number1
    
def miotQuery(queryCode):
    global oState
    BLINKER_LOG('MIOT Query codes: ', queryCode)
    BlinkerMIOT.powerState(oState)
    BlinkerMIOT.print()

def button1_callback(state):
    ''' '''

    BLINKER_LOG('get button state: ', state)

    button1.icon('icon_1')
    button1.color('#FFFFFF')
    button1.text('Your button name or describe')
    button1.print(state)

def data_callback(data):
    global counter
    
    BLINKER_LOG('Blinker readString: ', data)
    counter += 1
    number1.print(counter)

button1.attach(button1_callback)
Blinker.attachData(data_callback)

BlinkerMIOT.attachPowerState(miotPowerState)
BlinkerMIOT.attachQuery(miotQuery)

if __name__ == '__main__':

    while True:
        Blinker.run()
