#!/usr/bin/env python3
# numpy 和 OpenCV 兼容的图像类型以便于使用。
# 它使用 ColorCamera 节点来检索 BGR 交错的“预览”和 NV12 编码的“视频”帧。
# 两者都使用函数getFrame和getCvFrame显示。

import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)
xoutPreview = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")
xoutPreview.setStreamName("preview")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(True)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Linking
camRgb.video.link(xoutVideo.input)
camRgb.preview.link(xoutPreview.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    video = device.getOutputQueue('video')
    preview = device.getOutputQueue('preview')

    while True:
        videoFrame = video.get()
        previewFrame = preview.get()

        # Get BGR frame from NV12 encoded video frame to show with opencv
        cv2.imshow("video", videoFrame.getCvFrame())
        # Show 'preview' frame as is (already in correct format, no copy is made)
        cv2.imshow("preview", previewFrame.getFrame())

        if cv2.waitKey(1) == ord('q'):
            break
