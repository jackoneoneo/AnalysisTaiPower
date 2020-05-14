# coding=utf-8
import os
import sqlite3
from sys import argv

import numpy as np
import plotly
import plotly.graph_objs as go

# db_file_path = argv[1]
# db_file_path = "./01bcms1.db"
# db_store_dir = "./"
# 画图

conn = sqlite3.connect("./data.db")
c = conn.cursor()



#获取数据
sql = "select time, frequency,minP,maxP ,(minP + maxP) / 2 from frequency_power  where " \
      "time > '2018-12-01 13:00:00' and time <'2018-12-01 14:00:00'order by time;"
data_result_list = c.execute(sql)
data_list = []
for item in data_result_list:
    data_list.append(list(item))
data_list = np.array(data_list)


c.close()
conn.close()

colors = ['#39bedf', '#ebb200', '#fe4e01', '#bebada',
          '#B23AEE', '#000000', '#fdb462',
          '#b3de69', '#fccde5', '#d9d9d9',
          '#bc80bd', '#ccebc5', '#ffed6f', '#000000']
colorsX = ['#FF0000', '#8B0000', '#000000', '#B23AEE', '#bebada']
traces = []

# 频率
traces.append(go.Scatter(
            mode='lines', line=dict(color=colors[0], width=0.5),
            connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
            x=data_list[:, 0],
            y=list(map(float, data_list[:, 1])),
            yaxis='y',  # 标注轴名称
            name="频率",  # 标注鼠标移动时的显示点信息
            marker=dict(color=colors[0], size=12, ),
            showlegend=True,
        ))

# 最大功率比例
traces.append(go.Scatter(
    mode='lines', line=dict(color=colors[1], width=1),
    connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
    x=data_list[:, 0],
    y=list(map(float, data_list[:, 3])) ,
    name="最大功率比例 ",  # 标注鼠标移动时的显示点信息
    marker=dict(color=colors[1], size=12, ),
    yaxis='y2',
    showlegend=True,
))
# 最小功率比例
traces.append(go.Scatter(
    mode='lines', line=dict(color=colors[2], width=1),
    connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
    x=data_list[:, 0],
    y=list(map(float, data_list[:, 2]) ),
    name="最小功率比例",  # 标注鼠标移动时的显示点信息
    marker=dict(color=colors[2], size=12, ),
    yaxis='y2',
    showlegend=True,
))

# 平均功率比例
traces.append(go.Scatter(
    mode='lines', line=dict(color=colors[3], width=1),
    connectgaps=False,  # 对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
    x=data_list[:, 0],
    y=list(map(float, data_list[:, 4]) ),
    name="平均功率比例",  # 标注鼠标移动时的显示点信息
    marker=dict(color=colors[3], size=12, ),
    yaxis='y2',
    showlegend=True,
))


layout = go.Layout(
    width=2000,
    xaxis=dict(
        domain=[0.1, 0.9],
        showline=True,
        showgrid=True,
        showticklabels=True,
        linewidth=2,
        # autotick=True,
        ticks='outside',
        tickwidth=2,
        ticklen=5,
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
        hoverformat="%Y/%m/%d %H:%M:%S",
    ),
    # 第一个y轴
    yaxis=dict(
        title='频率',
        linecolor=colors[0],
        showgrid=True,
        zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
        showline=True,
        showticklabels=True,
        titlefont=dict(color=colors[0]),
        tickfont=dict(color=colors[0]),
    ),
    # 第二个y轴
    yaxis2=dict(
        title='功率比例',
        linecolor=colors[1],
        showgrid=True,
        zeroline=False,  # 是否显示基线,即沿着(0,0)画出x轴和y轴
        showline=True,
        showticklabels=True,
        titlefont=dict(color=colors[1]),
        tickfont=dict(color=colors[1]),
        range=[0, 100],
        anchor='x',
        overlaying='y',
        side='right',
    ),

    # autosize=True,
    margin=dict(
        autoexpand=False,
        l=20,
        r=20,
        t=100,
    ),
    showlegend=True,
    legend=dict(
        x=0.95,
        y=1.1
    )
)
annotations = []
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                        xanchor='left', yanchor='bottom',
                        text="频率与功率比例图",
                        font=dict(family='Arial',
                                  size=30,
                                  color='rgb(37,37,37)'),
                        showarrow=False))

annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.05,
                        xanchor='center', yanchor='top',
                        text='数据来源：文本',
                        # '调频数据',
                        font=dict(family='Arial',
                                  size=12,
                                  color='rgb(150,150,150)'),
                        showarrow=False))
layout['annotations'] = annotations
fig = go.Figure(data=traces, layout=layout)
plotly.offline.plot(fig, filename='frequency_power.html', auto_open=False)
