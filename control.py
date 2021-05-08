#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Blinker.Blinker import Blinker, BlinkerButton, BlinkerMIOT, BlinkerText
from Blinker.BlinkerDebug import *
import socket # 和struct一起为发送魔术数据包（网络唤醒）提供支持
import struct 
import winrm # 远程控制windows客户端
import os # os库：调用系统命令

auth = '3bac28c1fcdf' # 设备Secret Key
mac = '00D861D913A0' # 电脑有线网卡的MAC地址
ip = '192.168.1.2' #电脑的IP地址
BROADCAST = "192.168.1.255" # 广播网段，前三段和你电脑的内网ip一样，一般是192.168.1.255
user = ('levi.yang.1999@qq.com', 'Yzy19990828') # 远程关机需要使用的windows账户和密码
data = ''.join(['FFFFFFFFFFFF', mac * 20])  # 构造原始数据格式
send_data = b''
# 把原始数据转换为16进制字节数组，
for i in range(0, len(data), 2):
    send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

BLINKER_DEBUG.debugAll()
Blinker.mode('BLINKER_WIFI')
Blinker.miotType('BLINKER_MIOT_OUTLET')
Blinker.begin(auth)
button = BlinkerButton("btn-power") #注册按键
oState = 'on' # 树莓派记录电脑在线状态的变量

# 远程开机函数，将MAC地址转换得到的16进制字节数组send_data在局域网内广播
def wake_up():
    # 通过socket广播出去，为避免失败，间隔广播三次
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        print("Done")
    except Exception as e:
        print(e)

# 远程关机函数
def shut_down():
    try:
        win = winrm.Session('http://' + ip + ':5985/wsman',user)
        r = win.run_cmd('shutdown -s -t 0')
        print("Shutdown over!")
    except Exception as e:
        print(e)

# 语音控制开关函数
def miotPowerState(state):
    global oState
    BLINKER_LOG('need set power state: ', state)
    oState = state
    BlinkerMIOT.powerState(state)
    BlinkerMIOT.print() # 给小爱反馈设备受控状态
    if oState == 'true':
        button.text('已开机') # 更新文本
        wake_up()
    elif oState == 'false':
        button.text('已关机')
        shut_down()
    button.print() # 更新数据到云端

def miotQuery(queryCode):
    global oState
    BLINKER_LOG('MIOT Query codes: ', queryCode)
    BlinkerMIOT.powerState(oState)
    BlinkerMIOT.print()

# 按钮控制开关函数
def button_callback(state):
    global oState
    BLINKER_LOG('get button state: ', state)
    oState = state
    if state == "on":
        button.text('已开机')
        wake_up()
    elif state == "off":
        button.text('已关机')
        shut_down()
    button.print(state)

# 心跳包函数，30秒到60秒发送一次数据包，激活这个函数，主要是为了查看电脑是否在线。
def heartbeat_callback():
    global oState
    a = os.system("ping -c 1 " + ip) # 树莓派ping电脑
    if a == 0: # ping通，电脑在线
        oState = 'on'
        button.text('已开机')
    else: # ping不通，电脑离线
        oState = 'off'
        button.text('已关机')
    button.print(oState)

def data_callback(data):
    BLINKER_LOG("Blinker readString: ", data)

BlinkerMIOT.attachPowerState(miotPowerState)
BlinkerMIOT.attachQuery(miotQuery)
button.attach(button_callback)
Blinker.attachData(data_callback)
Blinker.attachHeartbeat(heartbeat_callback)

if __name__ == '__main__':

    while True:
        Blinker.run()
