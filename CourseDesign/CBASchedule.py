import requests
import pymysql.cursors
headers={'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
url = "https://matchweb.sports.qq.com/matchUnion/list?today=2025-06-17&startTime=2024-10-16&endTime=2025-05-20&columnId=100008&index=6&isInit=true&timestamp=1750153591161&callback=fetchScheduleListCallback100008"
response = requests.get(url, headers=headers)
json_data=response.json()
datas=json_data['data']
connect=pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='datacollection',
    charset='utf8'
)
cursor=connect.cursor()
sql="INSERT INTO cbaschedule VALUES (null,%s, %s, %s, %s, %s)"
for data in json_data['data']:
    titles=json_data['data'][data][0]
    schedule=(titles['leftName'],int(titles['leftGoal']),titles['rightName'],int(titles['rightGoal']),titles['startTime'])
    cursor.execute(sql,schedule)
connect.commit()
connect.close()
print("插入成功！")