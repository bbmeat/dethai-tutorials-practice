'''
此示例显示了“相机控制”消息以及ColorCamera configInput更改裁剪x和y的用法。
使用“WASD”控件移动裁剪窗口，“C”捕获静止图像，“T”触发自动对焦，“IOKL”用于手动曝光:
  Control:      key[dec/inc]  min..max
  exposure time:     I   O      1..33000 [us]
  sensitivity iso:   K   L    100..1600
  focus:             ,   .      0..255 [far..near]
返回自动控制:
  'E' - autoexposure
  'F' - autofocus (continuous)
'''

import depthai as dai
import cv2
import numpy as np

# 设置移动的步长 ('W','A','S','D' 控制项)
STEP_SIZE = 8
# 手动曝光聚焦设定步骤
EXP_STEP = 500  # us
ISO_STEP = 50
LENS_STEP = 3

pipeline = dai.Pipeline()

# 创建彩色相机流
colorCam = pipeline.createColorCamera()
# 创建连接输入流
controlIn = pipeline.createXLinkIn()
configIn = pipeline.createXLinkIn()
# 创建视频编码流
videoEncoder = pipeline.createVideoEncoder()
stillEncoder = pipeline.createVideoEncoder()
# 创建连接输出流
videoMjpegOut = pipeline.createXLinkOut()
stillMjpegOut = pipeline.createXLinkOut()
previewOut = pipeline.createXLinkOut()


# 设置流属性
colorCam.setVideoSize(640, 360)
colorCam.setPreviewSize(300, 300)
controlIn.setStreamName('control')
configIn.setStreamName('config')
videoEncoder.setDefaultProfilePreset(colorCam.getVideoSize(), colorCam.getFps(), dai.VideoEncoderProperties.Profile.MJPEG)
stillEncoder.setDefaultProfilePreset(colorCam.getStillSize(), 1, dai.VideoEncoderProperties.Profile.MJPEG)
videoMjpegOut.setStreamName('video')
stillMjpegOut.setStreamName('still')
previewOut.setStreamName('preview')


# 链接节点
colorCam.video.link(videoEncoder.input)
colorCam.still.link(stillEncoder.input)
colorCam.preview.link(previewOut.input)
controlIn.out.link(colorCam.inputControl)
configIn.out.link(colorCam.inputConfig)
videoEncoder.bitstream.link(videoMjpegOut.input)
stillEncoder.bitstream.link(stillMjpegOut.input)

def clamp(num, v0, v1): return max(v0, min(num, v1))

# 管道已定义，现在设备已连接到管道
with dai.Device(pipeline) as dev:

    # 获取数据队列
    controlQueue = dev.getInputQueue('control')
    configQueue = dev.getInputQueue('config')
    previewQueue = dev.getOutputQueue('preview')
    videoQueue = dev.getOutputQueue('video')
    stillQueue = dev.getOutputQueue('still')

    # 启动管道
    dev.startPipeline()

    # 最大crop_x和crop_y
    max_crop_x = (colorCam.getResolutionWidth() - colorCam.getVideoWidth()) / colorCam.getResolutionWidth()
    max_crop_y = (colorCam.getResolutionHeight() - colorCam.getVideoHeight()) / colorCam.getResolutionHeight()

    # 默认裁剪
    crop_x = 0
    crop_y = 0
    send_cam_config = True

    # 手动对焦控制的默认值和限制
    lens_pos = 150
    lens_min = 0
    lens_max = 255

    exp_time = 20000
    exp_min = 1
    exp_max = 33000

    sens_iso = 800
    sens_min = 100
    sens_max = 1600

    while True:

        previewFrames = previewQueue.tryGetAll()
        for previewFrame in previewFrames:
            cv2.imshow('preview', previewFrame.getData().reshape(previewFrame.getWidth(), previewFrame.getHeight(), 3))

        videoFrames = videoQueue.tryGetAll()
        for videoFrame in videoFrames:
            # 解码JPEG
            frame = cv2.imdecode(videoFrame.getData(), cv2.IMREAD_UNCHANGED)
            # 展示
            cv2.imshow('video', frame)

            # 发送新的CFG到相机
            if send_cam_config:
                cfg = dai.ImageManipConfig()
                cfg.setCropRect(crop_x, crop_y, 0, 0)
                configQueue.send(cfg)
                print('Sending new crop - x: ', crop_x, ' y: ', crop_y)
                send_cam_config = False

        stillFrames = stillQueue.tryGetAll()
        for stillFrame in stillFrames:
            # 解码JPEG
            frame = cv2.imdecode(stillFrame.getData(), cv2.IMREAD_UNCHANGED)
            # 展示
            cv2.imshow('still', frame)


        # 更新画面
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            controlQueue.send(ctrl)
        elif key == ord('t'):
            print("Autofocus trigger (and disable continuous)")
            ctrl = dai.CameraControl()
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
            ctrl.setAutoFocusTrigger()
            controlQueue.send(ctrl)
        elif key == ord('f'):
            print("Autofocus enable, continuous")
            ctrl = dai.CameraControl()
            ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.CONTINUOUS_VIDEO)
            controlQueue.send(ctrl)
        elif key == ord('e'):
            print("Autoexposure enable")
            ctrl = dai.CameraControl()
            ctrl.setAutoExposureEnable()
            controlQueue.send(ctrl)
        elif key in [ord(','), ord('.')]:
            if key == ord(','): lens_pos -= LENS_STEP
            if key == ord('.'): lens_pos += LENS_STEP
            lens_pos = clamp(lens_pos, lens_min, lens_max)
            print("Setting manual focus, lens position:", lens_pos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lens_pos)
            controlQueue.send(ctrl)
        elif key in [ord('i'), ord('o'), ord('k'), ord('l')]:
            if key == ord('i'): exp_time -= EXP_STEP
            if key == ord('o'): exp_time += EXP_STEP
            if key == ord('k'): sens_iso -= ISO_STEP
            if key == ord('l'): sens_iso += ISO_STEP
            exp_time = clamp(exp_time, exp_min, exp_max)
            sens_iso = clamp(sens_iso, sens_min, sens_max)
            print("Setting manual exposure, time:", exp_time, "iso:", sens_iso)
            ctrl = dai.CameraControl()
            ctrl.setManualExposure(exp_time, sens_iso)
            controlQueue.send(ctrl)
        elif key in [ord('w'), ord('a'), ord('s'), ord('d')]:
            if key == ord('a'):
                crop_x = crop_x - (max_crop_x / colorCam.getResolutionWidth()) * STEP_SIZE
                if crop_x < 0: crop_x = max_crop_x
            elif key == ord('d'):
                crop_x = crop_x + (max_crop_x / colorCam.getResolutionWidth()) * STEP_SIZE
                if crop_x > max_crop_x: crop_x = 0
            elif key == ord('w'):
                crop_y = crop_y - (max_crop_y / colorCam.getResolutionHeight()) * STEP_SIZE
                if crop_y < 0: crop_y = max_crop_y
            elif key == ord('s'):
                crop_y = crop_y + (max_crop_y / colorCam.getResolutionHeight()) * STEP_SIZE
                if crop_y > max_crop_y: crop_y = 0
            send_cam_config = True