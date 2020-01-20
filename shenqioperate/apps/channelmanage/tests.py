from django.test import TestCase
import pymysql

# 111.230.137.136 线上！！！数据库 只能查询
pkmmaindb = {"host": "129.204.65.108",
             "port": 3306,
             "database": "pkm1_login",
             "user": "root",
             "password": "Xiaoji%_123!",
             "charset": "utf8"}


def getonlinedata():

    conn = pymysql.Connect(**pkmmaindb)
    cursor = conn.cursor()
    sql = "SELECT access_servers FROM platform_access_server_info WHERE platform_type = 0 AND child_platform_type = 0;"
    cursor.execute(sql)
    result = cursor.fetchone()
    district_service = result[0]
    print(district_service)
    d_s_len = int.from_bytes(district_service[0:1], byteorder='little')
    print('大区个数：', d_s_len)
    d_s_all = district_service[1:]  # 去掉表示长度的字节，剩下的就是大区信息
    i = 0
    quhao_l = []  # 为了是区号都能添加到列表，得一开始定义成空字符串
    for j in range(d_s_len):
        d_s = d_s_all[i: i + 2]
        d_s_n = int.from_bytes(d_s, byteorder='little')
        print('大区号：', d_s_n)
        quhao_l.append(d_s_n)
        i += 2

    cursor.close()
    conn.close()
    print('大区列表:', quhao_l)


if __name__ == '__main__':
    pass
