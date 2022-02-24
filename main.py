from typing import List

import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line

import process_data, get_data

# {
#     "time": "2020年1月",
#     "data": [
#         {"name": "广东", "value": [97278.0, 10.63, "广东"]},
#         {"name": "江苏", "value": [92595.0, 10.12, "江苏"]},
#
#     ],
# },

# 下载数据
get_data.main()

# 处理数据
data = process_data.read_data()

print("Begin Draw charts!")

time_list = [d['time'] for d in data]

total_num = [d['sum'] for d in data]

maxNum = 68311
minNum = 0


def get_year_chart(time: str):
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == time
    ][0]
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = 0
    for x in time_list:
        if x == time:
            data_mark.append(total_num[i])
        else:
            data_mark.append("")
        i = i + 1

    line_chart = (
        Line()
        .add_xaxis(time_list)
        .add_yaxis("", total_num)
        .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="全国新冠肺炎累计确诊总人数", pos_left="72%", pos_top="5%"
            )
        )
    )
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            series_name="",
            y_axis=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b} : {c}"
            ),
        )
        .reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                # is_calculable=True,
                is_piecewise=True,
                dimension=0,
                pos_left="10",
                # series_index=
                pos_top="top",
                pieces=[
                    {'min': 10000, 'max': 1000000, 'label': '≥10000', 'color': '#A9251B'},
                    {'min': 1000, 'max': 10000, 'label': '1000-9999', 'color': '#D4524D'},
                    {'min': 500, 'max': 999, 'label': '500-999', 'color': '#E57C6D'},
                    {'min': 100, 'max': 499, 'label': '100-499', 'color': '#F19E8A'},
                    {'min': 10, 'max': 99, 'label': '10-99', 'color': '#FBE5DD'},
                    {'min': 0, 'max': 9, 'label': '0-9', 'color': '#FFFFFF'},
                ],
                # range_text=["High", "Low"],
                # range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    map_chart = (
        Map()
            .add(
            series_name="",
            data_pair=map_data,
            zoom=1,
            center=[119.5, 34.5],
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="" + str(time) + "全国分地区累计确诊人数",
                subtitle="数据来源：国家卫健委",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                dimension=0,
                pos_left="30",
                pos_top="center",
                pieces=[
                    {'min': 10000, 'max': 1000000, 'label': '大于等于10000人', 'color': '#372a28'},
                    {'min': 1000, 'max': 10000, 'label': '大于等于1000人', 'color': '#4e160f'},
                    {'min': 500, 'max': 999, 'label': '确诊500-999人', 'color': '#FFF8DC'},
                    {'min': 100, 'max': 499, 'label': '确诊100-499人', 'color': '#974236'},
                    {'min': 10, 'max': 99, 'label': '确诊10-99人', 'color': '#ee7263'},
                    {'min': 1, 'max': 9, 'label': '确诊1-9人', 'color': '#f5bba7'},
                ],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
            ),
        )
    )

    grid_chart = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
        .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart


if __name__ == "__main__":
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK, page_title='全国分地区新冠肺炎累计确诊人数')
    )
    for y in time_list:
        g = get_year_chart(time=y)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=3000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="90",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    timeline.render("China_Covid-19_number_of_confirmed_from_202001_to_{}.html".format(get_data.date[-1][0:-2]))

    print("Draw charts success!")
