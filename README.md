# DataTool 

*created 2016.12.27 ; updated 2016.02.12*

*author： hezhichao、mashuai*

用于数据预处理、结果处理、模型合并等等。

python为代码文件夹；rule为规则文件夹，以做参考。

## Python

### 1.pre
用来做数据预处理。

#### json2label.py
将来自深图厦门的存储label的json格式文件转换为用于训练的groudtruth文件。

#### data_process.py
用于数据的上采样、合并、分离等等。

### 2.post
训练完成之后的一些操作。

#### review_rate.py
根据classify的结果文件，计算各个类别的复审率。
提供了image、video等多种复审率计算方式。

#### recog_rate.py
带阈值的图片复审率。

#### models_modify.py
对训练完成后的模型做一些修改操作。

#### models_merge.py
对多个模型做合并操作。

#### cls/cls2dir.py
根据classify结果文件,把图片按类别分别存储到不同label_index的文件夹。

#### cls/cls2falsegt.py
根据分类结果文件和gt文件，找出分错的样本。

### 3.imgcut
和标框图片有关的操作。

#### cut_image.py
把深图厦门包围盒数据做图片切分处理，然后可以应用到图片分类的任务里面。

#### cut_image_v2.py
同 cut_image.py,但是支持多个输入。

#### label2gt.py
把label文件的第2列替换成其他值。

### 4.imgaug
数据扩增的一些方法。


### 5.other
其他的一些功能。

#### dedup_data.py
去除重复的 整行（lst）或者 第一列（gt）。