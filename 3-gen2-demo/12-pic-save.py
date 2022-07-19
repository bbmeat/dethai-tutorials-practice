import time
from pathlib import Path

import cv2
import depthai as dai

# 开始定义管道
pipeline = dai.Pipeline()

# 创建彩色相机
cam_rgb = pipeline.createColorCamera()
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)  # 设置传感器分辨率
cam_rgb.setFps(40)  # 设置图像帧率

# 创建RGB输出
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")
cam_rgb.video.link(xout_rgb.input)

# 创建编码器以生成JPEG图像
video_enc = pipeline.createVideoEncoder()
video_enc.setDefaultProfilePreset(cam_rgb.getVideoSize(), cam_rgb.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
cam_rgb.video.link(video_enc.input)

# 创建JPEG输出
xout_jpeg = pipeline.createXLinkOut()
xout_jpeg.setStreamName("jpeg")
video_enc.bitstream.link(xout_jpeg.input)

# 管道已定义，现在设备已连接到管道
with dai.Device(pipeline) as device:
    # 启动管道
    device.startPipeline()

    # 输出队列将用于从上面定义的输出中获取rgb帧
    q_rgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    q_jpeg = device.getOutputQueue(name="jpeg", maxSize=30, blocking=True)

    # 开始存储示例之前，请确保目标路径存在
    Path('06_data').mkdir(parents=True, exist_ok=True)

    while True:
        in_rgb = q_rgb.tryGet()  # 非阻塞呼叫，将返回已到达的新数据，否则返回None

        if in_rgb is not None:
            # 数据最初表示为1维数组，需要将其转换为HxW形式
            shape = (in_rgb.getHeight() * 3 // 2, in_rgb.getWidth())
            frame_rgb = cv2.cvtColor(in_rgb.getData().reshape(shape), cv2.COLOR_YUV2BGR_NV12)
            # 图像已转换并使用OpenCV的imshow方法显示
            cv2.imshow("rgb", frame_rgb)

        for enc_frame in q_jpeg.tryGetAll():
            with open(f"06_data/{int(time.time() * 10000)}.jpeg", "wb") as f:
                f.write(bytearray(enc_frame.getData()))

        if cv2.waitKey(1) == ord('q'):
            break
