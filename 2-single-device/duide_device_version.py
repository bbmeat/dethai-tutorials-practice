#!/usr/bin/env python3
# 设备引导加载版本

import depthai as dai

(res, info) = dai.DeviceBootloader.getFirstAvailableDevice()

if res == True:
    print(f'Found device with name: {info.name}')
    bl = dai.DeviceBootloader(info)
    print(f'Version: {bl.getVersion()}')
else:
    print('No devices found')
