from pathlib import Path

import numpy as np
import cv2
import depthai
import blobconverter

pipeline = depthai.Pipeline()  # 定义新对象

cam_rgb = pipeline.create(depthai.node.ColorCamera)  # 设置调整相机参数
cam_rgb.setPreviewSize(300, 300)  # 调整输入图像大小
cam_rgb.setInterleaved(False)

detection_nn = pipeline.create(depthai.node.MobileNetDetectionNetwork)  # 定义网络结点
detection_nn.setBlobPath(blobconverter.from_zoo(name='mobilenet-ssd', shaves=6))
detection_nn.setConfidenceThreshold(0.5)

cam_rgb.preview.link(detection_nn.input)  # 彩色相机接入神经网络

# 使用xlinkout节点，将相机的帧和推理结果传输到pc
xout_rgb = pipeline.create(depthai.node.XLinkOut)  # 彩色相机帧
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

xout_nn = pipeline.create(depthai.node.XLinkOut)  # 彩色相机处理结果
xout_nn.setStreamName("nn")
detection_nn.out.link(xout_nn.input)

with depthai.Device(pipeline) as device:  # 添加助手
    # device = depthai.Device(pipeline, usb2Mode=True)
    # usb2.0带宽设置（默认3.0）

    # 定义pc输出队列
    q_rbg = device.getOutputQueue("rgb")  # rgb框架
    q_nn = device.getOutputQueue("nn")  # nn结果

    frame = None
    detections = []

    # 定义辅助函数 将<0..1>值
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)


    # 使用结果
    while True:
        # 在循环中从nn结点和彩色相机获取最新结果
        in_rgb = q_rbg.tryGet()
        in_nn = q_nn.tryGet()
        # tryget方法返回最新结果或者none队列

        # 相机结果或神经网络结果为 一维数组 提供，需要对其进行转换， frameNorm函数为转换函数
        if in_rgb is not None:
            frame = in_rgb.getCvFrame()  # 从相机接受帧

        if in_nn is not None:
            detections = in_nn.detections  # 神经网络结果
        # 默认字段为7个：image_id , label , confidence , x_min , y_min , x_max , y_max , detections

        # 显示结果
        if frame is not None:
            for detection in detections:
                bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                # 用frameNorm之前定义的边界框坐标归一化
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                # 使用cv2.rectangle绘制矩形作为指示符
            cv2.imshow("preview", frame)
            # 用imgshow显示

        if cv2.waitKey(1) == ord('q'):
            break
        # 如果系统陷入循环 按下q退出
