import threading
import time
import cv2
import socket
import sys
import numpy as np
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from djitellopy import tello


tcp_server_socket = socket(AF_INET, SOCK_STREAM)
address1 = ('', 8000)
tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcp_server_socket.bind(address1)
tcp_server_socket.listen(128)

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamon()

def fly(date):
    # print(date.lstrip())
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    all_date = []
    all_date.append(str(date))
    # print(all_date)
    if "b'b'" in all_date:
        lr = -40
        time.sleep(0.05)
        all_date.clear()
        print("左飞")
    if "b'n'" in all_date:
        lr = 40
        time.sleep(0.05)
        all_date.clear()
        print("右飞")
    if "b'w'" in all_date:
        fb = speed
        time.sleep(0.05)
        all_date.clear()
        print("前飞")
    if "b's'" in all_date:
        fb = -speed
        time.sleep(0.05)
        all_date.clear()
        print("后飞")
    if "b'h'" in all_date:
        ud = speed
        time.sleep(0.05)
        all_date.clear()
        print("升高")
    if "b'j'" in all_date:
        ud = -speed
        time.sleep(0.05)
        all_date.clear()
        print("降低")
    if "b'a'" in all_date:
        yv = -60
        time.sleep(0.05)
        all_date.clear()
        print("左转")
    if "b'd'" in all_date:
        yv = 60
        time.sleep(0.05)
        all_date.clear()
        print("右转")
    if "b'l'" in all_date:
        me.land()
        time.sleep(0.05)
        all_date.clear()
        print("降落")
    if "b't'" in all_date:
        me.takeoff()
        time.sleep(0.05)
        all_date.clear()
        print("起飞")
    return [lr, fb, ud, yv]

address = ('', 5006)  # 服务端地址和端口
# ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser = socket(AF_INET, SOCK_STREAM)
ser.bind(address)
ser.listen(5)
# 阻塞式
print('waiting...')
conn, addr = ser.accept()
print('建立连接...')
print('连接对象：', addr)

def image():
    while (True):
        try:
            data = conn.recv(1024)
            data = data.decode()
            if not data:
                break
            frame = me.get_frame_read().frame
            frame = cv2.resize(frame, (360, 240))
            cv2.imshow('send', frame)
            cv2.waitKey(1)
            # 数据打包有很多方式，也可以用json打包
            img_encode = cv2.imencode('.jpg', frame)[1]
            data_encode = np.array(img_encode)
            str_encode = data_encode.tobytes()

            conn.sendall(str_encode)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            sys.exit(0)


def con():
    print("等待连接")
    tcp_client_socket, addr = tcp_server_socket.accept()
    print('connected from', addr)
    while True:
        data = tcp_client_socket.recv(1024)
        if not data:
            break
        try:
            if data.decode().startswith('exit'):
                break
        except Exception as e:
            print(e)
            break
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        vals = fly(data)
        print(vals)
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        tcp_client_socket.send((str(now_time)+'PC1 received'+ str(me.get_battery())).encode())
    tcp_client_socket.close()

t1 = threading.Thread(target=image)
t2 = threading.Thread(target=con)
t1.start()
t2.start()
t1.join()
t2.join()