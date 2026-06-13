import pymysql
import requests
headers={'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
url = "https://matchweb.sports.qq.com/match/api/v2/statistic/rankings?competition_id=5&season_id=&season_type=&type=0&scene=pc&qimei=3799863a36ec750f91c3814702000000917910"
response = requests.get(url, headers=headers)
datas = response.json()['data']
rows = datas['groups'][0]['tables'][0]['rows']
columns = []
for value in range(0, len(rows)):
    row = {}
    for column in rows[value]['values']:
        if column['code'] == "team":
            row[column['code']]=column['value']['cnName']
        else:
            row[column['code']]=column['value']
    columns.append(row)
data = [list(data.values()) for data in columns]
# connect=pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='datacollection',
#     charset='utf8'
# )
# cursor=connect.cursor()
# sql="INSERT INTO chlrank VALUES(%s,%s,%s,%s,%s,%s)"
# for datas in data:
#     cursor.execute(sql,datas)
# connect.commit()
# connect.close()
# print("插入成功！")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 数据准备
teams = ['利物浦', '巴塞罗那', '阿森纳', '国际米兰', '马德里竞技', '勒沃库森', '里尔', '阿斯顿维拉', '亚特兰大', '多特蒙德',
         '皇家马德里', '拜仁慕尼黑', 'AC米兰', '埃因霍温', '巴黎圣日耳曼', '本菲卡', '摩纳哥', '布雷斯特', '费耶诺德', '尤文图斯',
         '凯尔特人', '曼城', '葡萄牙体育', '布鲁日', '萨格勒布迪纳摩', '斯图加特', '顿涅茨克矿工', '博洛尼亚', '贝尔格莱德红星',
         '格拉茨风暴', '布拉格斯巴达', 'RB莱比锡', '赫罗纳', '萨尔茨堡', '布拉迪斯拉发', '青年人']
goals_conceded = ['17/5', '28/13', '16/3', '11/1', '20/12', '15/7', '17/10', '13/6', '20/6', '22/12',
                  '20/12', '20/12', '14/11', '16/12', '14/9', '16/12', '13/13', '10/11', '18/21', '9/7',
                  '13/14', '18/14', '13/12', '7/11', '12/19', '13/17', '8/16', '4/9', '13/22', '5/14',
                  '7/21', '8/15', '5/13', '5/27', '7/27', '3/24']
points = ['21', '19', '19', '19', '18', '16', '16', '16', '15', '15',
          '15', '15', '15', '14', '13', '13', '13', '13', '13', '12',
          '12', '11', '11', '11', '11', '10', '7', '6', '6', '6',
          '4', '3', '3', '3', '0', '0']

# 转换数据格式
points_int = [int(p) for p in points]
# 计算得失分率
gain_loss_rates = []
for gc in goals_conceded:
    goals, conceded = map(int, gc.split('/'))
    rate = goals / conceded if conceded != 0 else goals  # 避免除零错误
    gain_loss_rates.append(rate)

# 按积分排序
sorted_idx = np.argsort(points_int)[::-1]
teams_sorted = [teams[i] for i in sorted_idx]
points_sorted = [points_int[i] for i in sorted_idx]
gain_loss_sorted = [gain_loss_rates[i] for i in sorted_idx]

# 创建图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14), gridspec_kw={'height_ratios': [3, 1]})
plt.subplots_adjust(hspace=0.3)  # 增加子图间距

# ========== 主图表区域 ==========
# 主Y轴（积分）
x = np.arange(len(teams_sorted))

# 绘制积分柱状图
colors = ['#1a75ff' if pt >= 15 else '#ff6b6b' if pt < 10 else '#ffa500' for pt in points_sorted]
bars = ax1.bar(x, points_sorted, color=colors, edgecolor='black', alpha=0.8, width=0.7)

# 添加积分数据标签
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# 设置积分Y轴
ax1.set_ylabel('积分', fontsize=12, color='#333')
ax1.set_ylim(0, 25)
ax1.grid(True, linestyle=':', alpha=0.3, axis='y')
ax1.set_xticks(x)
ax1.set_xticklabels(teams_sorted, rotation=45, fontsize=9, ha='right')
ax1.set_title('欧冠球队积分榜与得失分率分析', fontsize=16, fontweight='bold', pad=15)

# 次Y轴（得失分率）
ax3 = ax1.twinx()
line = ax3.plot(x, gain_loss_sorted, 'o-', color='#28a745', linewidth=2,
               markersize=6, markerfacecolor='white', markeredgewidth=1.5)

# 设置得失分率Y轴
ax3.set_ylabel('得失分率 (进球/失球)', fontsize=12, color='#28a745')
ax3.tick_params(axis='y', labelcolor='#28a745')
ax3.set_ylim(0, 12)  # 国际米兰得失分率11.0，设置上限为12

# 添加得失分率数据标签（只标注关键点）
for i, rate in enumerate(gain_loss_sorted):
    # 只标注特别高或特别低的得失分率
    if rate > 5 or rate < 0.5:
        ax3.text(i, rate + 0.2, f'{rate:.2f}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='#28a745')

# 添加分区标识
ax1.axvline(x=7.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax1.axvline(x=15.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(3.5, -3, '争冠组', ha='center', va='center', fontsize=10, fontweight='bold')
ax1.text(11.5, -3, '中游组', ha='center', va='center', fontsize=10, fontweight='bold')
ax1.text(23.5, -3, '下游组', ha='center', va='center', fontsize=10, fontweight='bold')

# 添加图例
legend_elements = [
    plt.Rectangle((0,0), 1, 1, color='#1a75ff', alpha=0.8, label='积分≥15'),
    plt.Rectangle((0,0), 1, 1, color='#ffa500', alpha=0.8, label='10≤积分<15'),
    plt.Rectangle((0,0), 1, 1, color='#ff6b6b', alpha=0.8, label='积分<10'),
    plt.Line2D([0], [0], marker='o', color='w', label='得失分率', markerfacecolor='#28a745', markersize=8)
]
ax1.legend(handles=legend_elements, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), ncol=4, fontsize=10, frameon=True)

# ========== 得失分率详情区域 ==========
# 禁用底部图表的坐标轴
ax2.axis('off')

# 添加关键发现
analysis_text = (
    "关键发现：\n"
    "1. 利物浦以21分领先积分榜，得失分率3.40\n"
    "2. 国际米兰得失分率最高(11.0，进11球仅失1球)\n"
    "3. 布拉迪斯拉发和青年人积0分，得失分率仅0.19和0.13\n"
    "4. 得失分率与积分呈现强正相关关系\n\n"
    "分区说明：\n"
    "- 争冠组(前8名)：欧冠淘汰赛资格区\n"
    "- 中游组(9-16名)：欧联杯资格区\n"
    "- 下游组(17名以后)：淘汰区"
)
ax2.text(0.02, 0.6, analysis_text, ha="left", fontsize=11,
        bbox={"facecolor": "#f8f9fa", "alpha": 0.8, "pad": 10, "boxstyle": "round,pad=0.5"},
        transform=ax2.transAxes)

# 添加得失分率排行榜
top_text = "得失分率排行榜：\n"
top_rates = sorted(enumerate(gain_loss_sorted), key=lambda x: x[1], reverse=True)[:5]
for idx, (i, rate) in enumerate(top_rates):
    top_text += f"{idx+1}. {teams_sorted[i]}: {rate:.2f} ({goals_conceded[sorted_idx[i]]})\n"

bottom_text = "\n得失分率榜尾：\n"
bottom_rates = sorted(enumerate(gain_loss_sorted), key=lambda x: x[1])[:5]
for idx, (i, rate) in enumerate(bottom_rates):
    bottom_text += f"{idx+1}. {teams_sorted[i]}: {rate:.2f} ({goals_conceded[sorted_idx[i]]})\n"

ax2.text(0.6, 0.5, top_text + bottom_text, ha="left", fontsize=10,
        transform=ax2.transAxes)

# 添加数据来源
ax2.text(0.98, 0.02, "数据来源: 欧冠官方统计", ha="right", fontsize=9, color="gray", transform=ax2.transAxes)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(bottom=0.1)  # 增加底部空间

plt.savefig('CHL_Rank.png', dpi=300, bbox_inches='tight')
plt.show()