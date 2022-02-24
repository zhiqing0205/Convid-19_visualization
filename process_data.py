import os
import json


def read_data():

    print("Begin Process data!")

    all_data = []
    filepath = 'data/'
    pathDir = os.listdir(filepath)  # 获取当前路径下的文件名，返回list
    for s in pathDir:
        month_data = {'time': '', 'data': [], 'sum': 0, 'sort_key': 0}
        newDir = os.path.join(filepath, s)  # 将文件名写入到当前文件路径后面
        if os.path.isfile(newDir) and os.path.splitext(newDir)[1] == ".json":  # 如果是文件
            data = json.load(open(newDir))

            data = data['features']

            file_name = os.path.splitext(newDir)[0]

            file_name = file_name[len(filepath) + len('yq_'):-2]

            month_data['sort_key'] = int(file_name)

            year, month = file_name[:4], int(file_name[-2:])

            # print(year, month)

            time = year + '年' + str(month) + '月'
            month_data['time'] = time
            # print(time)
            sum = 0
            for d in data:
                d = d['properties']
                cnt = d['累计确诊']
                sum += cnt

            month_data['sum'] = sum
            all = []
            for d in data:
                d = d['properties']
                name = d['省份'][:2]

                if name == '黑龙' or name == '内蒙':
                    name = d['省份'][:3]

                t = {'name': name, 'value': []}
                t['value'].append(d['累计确诊'])
                t['value'].append(round(d['累计确诊'] / sum * 100, 2))
                t['value'].append(name)
                all.append(t)
                # print(t)

            all.sort(key=lambda x: (x['value'][0]), reverse=True)
            # print(all)
            month_data['data'] = all

        all_data.append(month_data)

    all_data.sort(key=lambda x: (x['sort_key']))
    # all_data = all_data[1:]

    print("Process data success!")
    return all_data


# data = read_data()
# print(data)
