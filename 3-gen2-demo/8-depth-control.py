#!/usr/bin/env python3

"""
此示例显示了在修剪模式下使用深度相机的可能性，可以移动修剪对象。
使用“ WASD”可以做到这一点。
"""

import cv2
import depthai as dai
import numpy as np

stepSize = 0.02

# 开始定义管道
pipeline = dai.Pipeline()

# 定义源-两个单（灰度）相机
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# 作用范围
topLeft = dai.Point2f(0.4, 0.4)
bottomRight = dai.Point2f(0.6, 0.6)

manip = pipeline.createImageManip()
manip.initialConfig.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
manip.setMaxOutputFrameSize(right.getResolutionHeight() * right.getResolutionWidth() * 3)

# 创建一个将产生深度图的节点
stereo = pipeline.createStereoDepth()
stereo.setConfidenceThreshold(200)

left.out.link(stereo.left)
right.out.link(stereo.right)

# 控制运动
controlIn = pipeline.createXLinkIn()
controlIn.setStreamName('control')
controlIn.out.link(manip.inputConfig)

# 创建输出
xout = pipeline.createXLinkOut()
xout.setStreamName("depth")
stereo.depth.link(manip.inputImage)
manip.out.link(xout.input)

# 连接并启动管道
with dai.Device(pipeline) as device:
    # 输出队列将用于从上面定义的输出中获取深度帧
    q = device.getOutputQueue(xout.getStreamName(), maxSize=4, blocking=False)

    sendCamConfig = False

    while True:
        inDepth = q.get()  # 阻塞，将等待直到新数据到达
        # 数据最初表示为平面1D数组，需要将其转换为HxW形式
        depthFrame = inDepth.getFrame()
        # 框架变形后，将应用颜色图以突出显示深度信息
        depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
        depthFrameColor = cv2.equalizeHist(depthFrameColor)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)
        controlQueue = device.getInputQueue(controlIn.getStreamName())

        # 显示显示深度图像
        cv2.imshow("depth", depthFrameColor)

        # 更新画面
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('w'):
            if topLeft.y - stepSize >= 0:
                topLeft.y -= stepSize
                bottomRight.y -= stepSize
                sendCamConfig = True
        elif key == ord('a'):
            if topLeft.x - stepSize >= 0:
                topLeft.x -= stepSize
                bottomRight.x -= stepSize
                sendCamConfig = True
        elif key == ord('s'):
            if bottomRight.y + stepSize <= 1:
                topLeft.y += stepSize
                bottomRight.y += stepSize
                sendCamConfig = True
        elif key == ord('d'):
            if bottomRight.x + stepSize <= 1:
                topLeft.x += stepSize
                bottomRight.x += stepSize
                sendCamConfig = True

        if sendCamConfig:
            cfg = dai.ImageManipConfig()
            cfg.setCropRect(topLeft.x, topLeft.y, bottomRight.x, bottomRight.y)
            controlQueue.send(cfg)
            sendCamConfig = False
