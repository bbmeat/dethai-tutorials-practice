# Triangulation - Stereo neural inference demo

因为经常有特定于应用程序的主机端过滤要在立体音响上完成
神经推理的结果，因为这些计算是轻量级的
(例如，在ESP32上可以完成)，我们将三角定位本身留给主机。

这个3D可视化工具是用于面部地标演示，并使用OpenGL和OpenCV。在这一点上，把它当作一个草稿/参考。

演示采用两阶段推理;第一个NN模型为 [face-detection-retail-0004](https://docs.openvino.ai/2021.4/omz_models_model_face_detection_retail_0004.html)
第2
NN模型为 [landmarks-regression-retail-0009](https://docs.openvino.ai/2021.4/omz_models_model_landmarks_regression_retail_0009.html)
.

## Demo

![Stereo Inference GIF](https://user-images.githubusercontent.com/59799831/132098832-70a2d0b9-1a30-4994-8dad-dc880a803fb3.gif)

## Installation

```
sudo apt-get install python3-pygame
python3 -m pip install -r requirements.txt
```

## Usage

运行应用程序

```
python3 main.py
```

你会看到5个窗口出现:

- `mono_left`哪个将显示相机输出从左单声道相机+脸包围框和面部地标
- `mono_right`哪将显示相机输出从左单声道相机+脸边界框和面部地标，这将显示相机输出从右单声道相机+脸边界框和面部地标
- `crop_left` 这将显示48x48左裁剪图像,进入第二个NN +面部地标得到输出从第二个NN
- `crop_right` 这将显示48×48的右裁剪图像，进入第二个NN +面部地标，从第二个NN输出
- `pygame window` 哪个会显示三角测量结果
