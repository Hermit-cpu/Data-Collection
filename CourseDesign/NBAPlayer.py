import pymysql
import requests
headers={'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
url = "https://matchweb.sports.qq.com/match/api/v2/statistic/rankings?competition_id=100000&season_id=&season_type=&type=2&scene=pc&qimei=3799863a36ec750f91c3814702000000917910"
response = requests.get(url, headers=headers)
datas = response.json()['data']
rows = datas['groups'][0]['tables'][0]['rows']
columns = []
for value in range(0,len(rows)):
    row = {}
    for column in rows[value]['values']:
        if column['code'] == "team" or column['code'] == "player":
            row[column['code']]=column['value']['cnName']
        else:
            row[column['code']]=column['value']
    columns.append(row)

player = [list(data.values()) for data in columns]
connect=pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='datacollection',
    charset='utf8'
)
# cursor=connect.cursor()
# sql="INSERT INTO nbaplayer VALUES(%s,%s,%s,%s,%s)"
# for data in player:
#     cursor.execute(sql,data)
# connect.commit()
# connect.close()
# print("插入成功！")
all=[]
for data in player:
    p = []
    p.append(data[1])
    p.append(data[2])
    p.append(data[4])
    all.append(p)
print(all)