import cv2
import depthai as dai
import numpy as np

# 开始定义管道
pipeline = dai.Pipeline()

# 创建彩色相机流
cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(300, 300)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(True)
cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# 创建输出
xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
xout_preview = pipeline.createXLinkOut()
xout_preview.setStreamName("preview")

cam_rgb.preview.link(xout_preview.input)
cam_rgb.video.link(xout_video.input)

# 管道已定义，现在设备已连接到管道
with dai.Device(pipeline) as device:
    # 启动管道
    device.startPipeline()

    while True:
        # 获取预览和视频帧
        preview = device.getOutputQueue('preview').get()
        video = device.getOutputQueue('video').get()

        # 按原样显示“预览”图像（格式正确，未复制）
        cv2.imshow("preview", preview.getFrame())
        # 从NV12编码的视频帧中获取BGR帧以使用opencv进行显示
        cv2.imshow("video", video.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
