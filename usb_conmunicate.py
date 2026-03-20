# -*- coding: utf-8 -*-
#LINUX上运行
#sudo pip3 install pyserial 
#sudo python3 serialwrite.py
import serial
import time

def usb_init(serial_port="/dev/ttyUSB0", baud_rate=9600, timeout=0.5):
  # 打开串口并返回串口对象
  return serial.Serial(serial_port, baud_rate, timeout=timeout)

def usb_write(s, cmd):
  # 发送 16 进制指令字符串
  d = bytes.fromhex(cmd)
  s.write(d)
  print("发送命令：{0}".format(cmd))

def relay_set(s, channel=1, on=True):
  # 单函数控制开关：on=True 打开，on=False 关闭
  op = 0x01 if on else 0x00
  check = 0xA0 + channel + op
  cmd = "A0 {0:02X} {1:02X} {2:02X}".format(channel, op, check)
  usb_write(s, cmd)

def usb_close(s):
  if s and s.is_open:
    s.close()


if __name__ == "__main__":
  s = usb_init()

  try:
    while True:
      cmd = input("请输入 '0' 打开继电器, '1' 关闭继电器 (输入 'q' 或 'exit' 退出): ")
      if cmd == '0':
        relay_set(s, 1, True)
        
        print("继电器吸起")
      elif cmd == '1':
        relay_set(s, 1, False)
        print("继电器落下")
      elif cmd.lower() in ['q', 'exit']:
        print("程序退出。")
        break
      else:
        print("无效输入，请重新输入。")
  finally:
    usb_close(s)
