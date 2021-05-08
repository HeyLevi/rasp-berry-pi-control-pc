import winrm

win = winrm.Session('http://192.168.1.3:5985/wsman',auth=('levi.yang.1999@qq.com','Yzy19990828'))
r = win.run_cmd('shutdown -s -t 0')
print("Shutdown over!")