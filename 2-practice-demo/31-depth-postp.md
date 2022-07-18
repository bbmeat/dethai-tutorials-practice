#  中值滤波器
>这是一个非边缘保留的中值滤波器，可用于降低噪声和平滑深度图。  
中值滤波器是在硬件中实现的，因此它是最快的滤波器。

`enumdai::MedianFilter`  
>用于视差后处理  的中值滤波器配置

Values:

`enumeratorMEDIAN_OFF`  
`enumeratorKERNEL_3x3`  
`enumeratorKERNEL_5x5`  
`enumeratorKERNEL_7x7`


# 散斑滤波器
>散斑滤波器用于减少散斑噪声。散斑噪声是相邻视差/深度像素之间具有巨大差异的区域，  
散斑滤波器试图过滤该区域。

`structdai::RawStereoDepthConfig::PostProcessing::SpeckleFilter`  
>散斑过滤。去除散斑噪声。

Public Members

`bool enable = false`
>是否启用或禁用过滤器。

std::uint32_t speckleRange = 50
>散斑搜索范围。

# 时间过滤器
>时间过滤器旨在通过基于先前帧操作每个像素值来提高深度数据的持久性。  
过滤器对数据执行单次传递，调整深度值，同时更新跟踪历史。  
在像素数据丢失或无效的情况下，过滤器使用用户定义的持久性模式来决定是  
否应该使用存储的数据来纠正丢失的值。请注意，由于它依赖于历史数据，  
过滤器可能会引入可见的模糊/拖尾伪影，因此最适合静态场景。


`structdai::RawStereoDepthConfig::PostProcessing::TemporalFilter`  
>具有可选持久性的时间过滤。

### Public Types

`enumPersistencyMode`
>持久性算法类型。

### Values:

`enumeratorPERSISTENCY_OFF`  
`enumeratorVALID_8_OUT_OF_8`  
`enumeratorVALID_2_IN_LAST_3`  
`enumeratorVALID_2_IN_LAST_4`  
`enumeratorVALID_2_OUT_OF_8`  
`enumeratorVALID_1_IN_LAST_2`  
`enumeratorVALID_1_IN_LAST_5`  
`enumeratorVALID_1_IN_LAST_8`  
`enumeratorPERSISTENCY_INDEFINITELY`


### Public Members

`bool enable = false`
>是否启用或禁用过滤器。

`PersistencyModepersistencyMode = PersistencyMode::VALID_2_IN_LAST_4`
>持久性模式。如果当前视差/深度值无效，则会根据持久性模式将其替换为较旧的值。

`float alpha = 0.4f`  

>Alpha=1 的指数移动平均线中的 Alpha 因子 - 无过滤器。Alpha = 0 - 无限滤波器。确定应平均的时间历史的范围。

`std::int32_t delta = 0`  

>步长边界。建立用于保留表面（边缘）的阈值。如果相邻像素之间的视差值超过此 delta 参数设置的视差阈值，则将暂时禁用过滤。默认值 0 表示自动：3 个差异整数级别。在子像素模式的情况下，它是 3* 子像素级别数。


# 空间边缘保留过滤器
>空间边缘保留过滤器将用有效的相邻深度像素填充无效的深度像素。它执行一系列 1D 水平和垂直传递或迭代，以增强重建数据的平滑度。它基于这篇[研究论文](https://www.inf.ufrgs.br/~eslgastal/DomainTransform/)。

`structdai::RawStereoDepthConfig::PostProcessing::SpatialFilter`  

>使用高阶域变换的一维边缘保留空间滤波器。

### Public Members

`bool enable = false`  

>是否启用或禁用过滤器。

`std::uint8_t holeFillingRadius = 2`  

>在过滤器通过期间水平应用的就地启发式对称孔填充模式。  
旨在纠正对性能影响最小的次要伪影。孔填充的搜索半径。

`float alpha = 0.5f`  

>Alpha=1 的指数移动平均线中的 Alpha 因子 - 无过滤器。Alpha = 0 - 无限滤波器。确定平滑量。

`std::int32_t delta = 0`  

>步长边界。建立用于保留“边缘”的阈值。如果相邻像素之间的视差值超过此 delta 参数设置的视差阈值，   
则将暂时禁用过滤。默认值 0 表示自动：3 个差异整数级别。  
在子像素模式的情况下，它是 3* 子像素级别数。

`std::int32_t numIterations = 1`  

>图像在水平和垂直方向上的迭代次数。


# 阈值过滤器
>阈值过滤器过滤掉配置的最小/最大阈值之外的所有视差/深度像素。


`classdepthai.RawStereoDepthConfig.PostProcessing.ThresholdFilter`  

>阈值过滤。过滤掉给定间隔之外的距离。

`propertymaxRange`  

>深度单位的最大范围。超过此值的深度值无效。

`propertyminRange`  

>深度单位的最小范围。此值以下的深度值无效。


# 抽取过滤器
>抽取过滤器将对深度图进行子采样，这意味着它降低了深度场景的复杂性并允许其他过滤器运行得更快。设置decimationFactor为 2 会将 1280x800 深度图缩小到 640x400。

`structdai::RawStereoDepthConfig::PostProcessing::DecimationFilter`  

>抽取过滤器。降低深度场景的复杂性。过滤器在内核大小 [2x2] 到 [8x8] 像素上运行。

### Public Types

`enumDecimationMode`  

抽取算法类型。

### Values:

`enumeratorPIXEL_SKIPPING`  
`enumeratorNON_ZERO_MEDIAN`  
`enumeratorNON_ZERO_MEAN`  

### Public Members

`std::uint32_t decimationFactor = 1`  
>抽取因子。有效值为 1、2、3、4。视差/深度图 x/y 分辨率将使用该值进行抽取。

`DecimationModedecimationMode = DecimationMode::PIXEL_SKIPPING`
>抽取算法类型。    