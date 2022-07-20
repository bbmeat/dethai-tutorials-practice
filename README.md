# depth-yolov4-tiny-tf2-strawberry-git
### To detect strawberry with [OAK-D](https://opencv.org/opencv-ai-competition-2021/#introSection)
### Our video is provided in this [Youtube Channel](https://youtu.be/BGaOO0MzBv0).

---

### 0. 准备python环境。
tensorflow2 and depthai (newest)

### 1. 准备水果数据集。
我们的草莓数据集包含两个类:即, MatureStrawberry 和 GreenStrawberry. 所有数据都是从 [Kobayashi Farm](https://kobayashifarm-mitaka.tokyo/) 在日本三高市。非常感谢果园老板支持我们收集水果数据。<br><br>
<img src="./img/rgb-00007-16160356916470.jpeg" alt="drawing" width="400"/>
<img src="./img/rgb-00357-16160404199341.jpeg" alt="drawing" width="400"/>
<br><br>
您可以通过下载一些开放数据集或自己收集数据集来准备数据集。虽然我们收集的颜色和深度图像大致与彩色图像对齐，但我发现在神经网络的输入中加入深度通道似乎并没有明显提高精度。可能是由于深度和rgb图像之间的不精确对齐。<br><br>
我手动调整相机内部参数，然后使用图像处理方法来对齐深度图像。但最近官方发布了深度和颜色图像对齐的代码。如果想同时收集两种类型的图像，可以参考[depthai-python](https://github.com/luxonis/depthai-python/blob/main/examples/31_rgb_depth_aligned.py).
### 2. 准备水果数据集。更改model_data目录中的文件。
改变类信息和锚的大小，可以计算使用 `kmeans_for_anchors.py`
### 3. 根据您的需要在`train_prune_eager.py` 微调参数
批量大小、初始学习速率和学习速率衰减应该是最需要调整的部分。<br><br>
您还可以使用`train.py` 训练你的网络，这比渴望模式更快。<br><br>
我根据属性修剪方法分析了每一层可以修剪的通道数量 ([paper](https://www.sciencedirect.com/science/article/pii/S0168169919313717), [code](https://github.com/GlowingHorse/Fast-Mango-Detection))，所以网络大小比原来的yolov4-tiny小得多。如果需要检测更多的图像类，网络也需要重新设计。
### 4.手动或自动保存最佳训练模型。
经验上有效的损失小于2是好的(或者对于非急于求成的模型是10)<br>
我们的培训代码主要是指的代码[here](https://github.com/bubbliiiing/yolov4-tiny-tf2/blob/master/train.py)。在非即时模式下训练的模型在试图将其转换为IR模型时总是出错，所以我只在即时模式下训练模型。但是，非即时模式可能更快，因此，您也可以使用非即时模式进行训练以提高效率，然后在即时模式中加载权重并保存它。
### 5. 上传模型文件到你的谷歌驱动器，像:
<img src="./img/drive_files.png" alt="drawing" width="800"/>

### 6.运行 `convertPbModel-evalData-yolov4.ipynb` 在你的合作中生成 `.blob`文件.
在运行之前，您需要修改上传的模型文件存放的目录。
或者你也可以引用 [**Converting model to MyriadX blob**](https://docs.luxonis.com/en/latest/pages/model_conversion/)来转换你的模型。

### 7. 下载.blob文件到models目录用`detDepthStrawb-prunedYolov4Tiny-plainNN.py` 去检测您的水果。
运行`. blob`在你的深度相机中涂抹模型，并使用一些打印的图像或真实的水果来测试它。<br><br>
<img src="./img/detect_strawberry.png" alt="drawing" width="800"/>

