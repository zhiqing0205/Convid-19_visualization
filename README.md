# 1 项目结构

```python
.
├── get_data.py
├── main.py
└── process_data.py
```

# 2 项目流程

项目主要依赖于`requests`库及`pyecharts`库

## 2.1 安装依赖

```python
pip install requests
pip install pyecharts
```

## 2.2 启动项目

### 2.2.1 通过pycharm启动

通过pycharm打开项目文件夹，运行main.py

### 2.2.2 通过命令行启动

`cd`到项目文件夹

```python
python main.py
```

## 2.3 流程简介

首先`main.py`会调用`get_data.py`从**国家卫健委新冠肺炎疫情发布平台**下载每个月16号的数据(有疫情数据正式记录的第一天是2020年1月16日)，下载好的数据会存放进`data`文件夹内，待数据下载完成后，通过调用`process_data.py`会处理下载好的数据，将数据封装成按照时间顺序，按照累计确诊人数逆序的数据数组，最后`main.py`根据数据数组绘制各类图像并导出成`html`文件。项目启动完成后，项目结构如下：

```python
.
├── China_Covid-19_number_of_confirmed_from_202001_to_202202.html
├── data
│   ├── yq_20200116.json
│   ├── yq_20200216.json
│   ├── yq_20200316.json
………………………………………………………………
│   ├── yq_20211216.json
│   ├── yq_20220116.json
│   └── yq_20220216.json
├── get_data.py
├── main.py
└── process_data.py
```



# 3 项目文件

## 3.1 get_data.py

首先构造时间数组，即需要下载的疫情数据的日期，即`202xxx16`，然后遍历数组对每一个日期都进行`url`的拼接，发送`request`请求并响应请求讲文件保存在本地的`data`文件夹下，如果文件夹不存在则会创建，如果需要下载的数据已经存在则会跳过。每个文件下载时会打印出文件名，文件大小和下载进度。

## 3.2 process_data.py

遍历`data`文件夹内的`json`文件，对于每一个文件，都提取出各个地区的名字简称和累计确诊人数，并统计全国累计确诊人数，及各地区确诊人数占全国的比例(结果保留两位小数)，最后的数据组间按照时间顺序排列，组内按照确诊人数逆序排列。

## 3.3 main.py

首先会调用`get_data.py`下载`json`数据，再调用`process_data.py`进行数据预处理。随后构造中国地图，柱状图，折线图，饼状图并将数据进行绑定，加上分片展示的`VisualMapOpts`使得确诊人数越多的地区颜色越深。最后加入时间轴，使得上述四种图都会每隔3秒进行更新。

# 4 项目预览

![image-20220102150656032](https://s1.328888.xyz/2022/02/25/GWFTF.jpg)
