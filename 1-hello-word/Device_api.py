import numpy as np
import cv2
import depthai
import blobconverter

pipeline = depthai.Pipeline()
# 创建节点，并配置节点，将节点连接

# 上传pipeline到设备
with depthai.Device(pipeline) as device:
    # 在device上输出myriad id，USB速度， 可用的相机
    print('MxId:', device.getDeviceInfo().getMxId())
    print('USB speed:', device.getUsbSpeed())
    print('Connected cameras', device.getConnectedCameras())

    # 输入队列，将消息从主机发送到设备
    input_q = device.getInputQueue("input_name", maxSize=4, blocking=False)

    # 输出队列，在主机上收到设备上的信息
    output_q = device.getOutputQueue("output_name", maxSize=4, blocking=False)

    while True:
        # 从队列上获取数据
        output_q.get()  # output_q.tryGet() for non-blocking

        # 给设备发送信息
        cfg = device.ImageManipConfig()
        input_q.send(cfg)

# 连接指定设备
device_info = depthai.DeviceInfo("14442C108144F1D000")  # mxid
# device_info = depthai.DeviceInfo(“192.168.1.44”)  # ip地址
# device_info = depthai.DeviceInfo(“3.3.3”)  # USB端口号

# 多台设备 需要选中 multiple DepthAI per host
