import os
import requests
import time
import datetime


def getDate():
    dateList = []
    today = datetime.date.today()
    now = today.strftime('%Y%m%d')

    year = 2020
    while True:
        for month in [str(i).zfill(2) for i in range(1, 13)]:
            s = str(year) + month + '16'
            if s > now:
                return dateList
            dateList.append(s)
        year = year + 1


date = getDate()
print(date)


# 进度条模块
def progressbar(url, path, file_name):
    if not os.path.exists(path):  # 看是否有该文件夹，没有则创建文件夹
        os.mkdir(path)

    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True)
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start download!  [File name]:{}  [File size]:{size:.2f} MB'.format(
                file_name,
                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小

            filepath = path + file_name  # 设置图片name，注：必须加上扩展名

            if os.path.exists(filepath):
                print("File already exist!")
                return

            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % (
                        '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
        end = time.time()  # 下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
    except:
        print('Error!')


def main():
    print("Begin Download data!")

    path = r'data/'  # 设置下载到本地的地址
    # 下载主地址
    main_url = 'http://49.4.25.117/JKZX/'
    for d in date:
        print(d)
        file_name = 'yq_' + d + '.json'
        url = main_url + file_name
        progressbar(url, path, file_name)

    print("Download data success!")
