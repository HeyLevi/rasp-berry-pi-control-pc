import winrm

win = winrm.Session('http://ip:5985/wsman',auth=('username','password'))
r = win.run_cmd('shutdown -s -t 0')
print("Shutdown over!")