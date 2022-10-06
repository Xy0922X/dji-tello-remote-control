import socket
import sys
import cv2
import numpy as np
import time
address = ('39.108.68.235', 5005)  # 服务端地址和端口
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cli.connect(address)  # 尝试连接服务端
except Exception:
    print('[!] Server not found or not open')
    sys.exit()

frame_count = 1
while True:
    time1 = time.time() if frame_count == 1 else time1
    trigger = 'ok'
    cli.sendall(trigger.encode())
    data = cli.recv(1024*1024*20)
    image = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    cv2.imshow('video',image)
    cv2.waitKey(1)
    end_time = time.time()
    time2 = time.time()
    print(image.shape[:2], int(frame_count / (time2 - time1)))
    frame_count += 1
cli.close()

