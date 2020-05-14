import numpy as np
import sqlite3
from numpy.linalg import solve


# 第一段
def func1():
    return 1


# 第二段
def func2(f):
    return -2.08 * f + 124.76


# 第三段
def func3max(f):
    return -1.69565217 * f + 101.79521739


def func3min(f):
    return -2.47826087 * f + 148.55608696


# 第四段
def func4max():
    return 0.09


def func4min():
    return -0.09


# 第五段
def func5max(f):
    return -2.47826087 * f + 148.83521739


def func5min(f):
    return -1.69565217 * f + 101.68304348


# 第六段
def func6(f):
    return -2.08 * f + 124.84


# 第七段
def func7():
    return -1


# 创建数据库
def create_db():
    conn = sqlite3.connect('data.db')
    # 创建一个cursor：
    cursor = conn.cursor()
    # 执行一条SQL语句：创建user表
    #     cursor.execute('''
    #        CREATE TABLE frequency_power(
    #    ID INT PRIMARY KEY      NOT NULL,
    #    time          TimeStamp NOT NULL,
    #    frequency     double not null,
    #    maxP         double      NOT NULL,
    #    minP       double      NOT NULL
    # );
    #     ''')
    '''
       g（f）：实际功率/额定功率
       f:频率
       g(f) = 1 (f <= 59.50)
       g(f) = -2.08f + 124.76 ( 59.50<f<=59.75)
       -2.47826087f + 148.55608696 <= g(f)<= -1.69565217f + 101.79521739 ( 59.75<f<=59.98)
       -0.09<=g(f)<=0.09    ( 59.98<f < 60.02)
       -1.69565217f + 101.68304348<=g(f)<=-2.47826087f + 148.83521739 ( 60.02< f <=60.25)
       g(f) = -2.08f + 124.84 ( 60.25<f<=60.50)
       g(f) = -1 (60.50<f)
    '''
    data = np.loadtxt(r"C:\Users\Administrator\Desktop\dd.txt", delimiter=" ", dtype=float)
    count = 1
    for item in data:
        year = str(int(item[0]))

        month = int(item[1])
        if(month < 10):
            month = "0" + str(month)
        month = str(month)

        day = int(item[2])
        if (day < 10):
            day = "0" + str(day)
        day = str(day)

        hour = int(item[3])
        if (hour < 10):
            hour = "0" + str(hour)
        hour = str(hour)

        minute = int(item[4])
        if (minute < 10):
            minute = "0" + str(minute)
        minute = str(minute)

        second = int(item[5])
        if (second < 10):
            second = "0" + str(second)
        second = str(second)

        timeStr = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
        frequency = item[6]
        if frequency < 59.50:
            maxP = func1()
            minP = func1()
        elif frequency < 59.75:
            maxP = func2(frequency)
            minP = func2(frequency)
        elif frequency < 59.98:
            maxP = func3max(frequency)
            minP = func3min(frequency)
        elif frequency < 60.02:
            maxP = func4max()
            minP = func4min()
        elif frequency < 60.25:
            maxP = func5max(frequency)
            minP = func5min(frequency)
        elif frequency < 60.50:
            maxP = func6(frequency)
            minP = func6(frequency)
        else:
            maxP = func7()
            minP = func7()

        sql = "insert into frequency_power (ID, time,frequency,maxP,minP) values(%d,%s,%f,%f,%f)" % (
        count, "'" + timeStr + "'", frequency, maxP, minP)
        print(sql)
        count += 1
        cursor.execute(sql)
    # 关闭Cursor:
    cursor.close()
    conn.commit()
    # 关闭connection：
    conn.close()


if __name__ == "__main__":
    create_db()

# print(len(data))
