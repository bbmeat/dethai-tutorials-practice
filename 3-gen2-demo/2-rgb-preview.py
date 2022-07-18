import cv2
import depthai as dai
import numpy as np

# 定义管道
pipeline = dai.Pipeline()

# 创建彩色相机流
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(False)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# 创建输出流
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# 管道已创建，现在将设备连接管道
with dai.Device(pipeline) as device:
    # 启动管道
    device.startPipeline()

    # 输出队列将用于从上面定义的输出中获取rgb帧
    q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    while True:
        in_rgb = q_rgb.get()  # 阻止呼叫，将等待直到新数据到达

        # 使用OpenCV将图像显示出来
        cv2.imshow("bgr", in_rgb.getCvFrame())

        # 按'q'退出程序
        if cv2.waitKey(1) == ord('q'):
            break
