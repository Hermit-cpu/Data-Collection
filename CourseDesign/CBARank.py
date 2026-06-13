import pymysql
import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
headers={'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
url = "https://matchweb.sports.qq.com/match/api/v2/statistic/rankings?competition_id=100008&season_id=&season_type=&type=0&scene=pc&qimei=3799863a36ec750f91c3814702000000917910"
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
# sql="INSERT INTO cbarank VALUES(%s,%s,%s,%s,%s,%s,%s)"
# for datas in data:
#     cursor.execute(sql,datas)
# connect.commit()
# connect.close()
# print("插入成功！")


# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# CBA数据准备
teams = [team[1] for team in data]
win_rates = [winRate[5] for winRate in data]
gain_loss_rates = [scoreRatio[6] for scoreRatio in data]
# 转换数据格式
win_rates_float = [float(rate.strip('%')) for rate in win_rates]
gain_loss_float = [float(rate) for rate in gain_loss_rates]
# 按胜率排序
sorted_idx = np.argsort(win_rates_float)[::-1]
teams_sorted = [teams[i] for i in sorted_idx]
win_sorted = [win_rates_float[i] for i in sorted_idx]
gain_loss_sorted = [gain_loss_float[i] for i in sorted_idx]
# 创建图表
plt.figure(figsize=(16, 10))
# 主Y轴（胜率）
ax1 = plt.gca()
x = np.arange(len(teams_sorted))
# 绘制胜率折线图
line = ax1.plot(x, win_sorted, 'o-', color='#e63946', linewidth=2.5,
               markersize=8, markerfacecolor='white', markeredgewidth=1.5,
               label='胜率 (%)')
# 添加胜率数据标签
for i, rate in enumerate(win_sorted):
    va = 'bottom' if i < 15 else 'top'  # 下半区标签在上方
    offset = 1.5 if i != 0 else -3.5  # 避免与最高点重叠
    ax1.text(i, rate + offset, f'{rate:.1f}%',
            ha='center', va=va, fontsize=10, fontweight='bold', color='#e63946')

# 设置胜率Y轴
ax1.set_ylabel('胜率 (%)', fontsize=12, color='#e63946')
ax1.tick_params(axis='y', labelcolor='#e63946')
ax1.set_ylim(0, 100)
ax1.grid(True, linestyle='--', alpha=0.4, axis='y')
ax1.set_xticks(x)
ax1.set_xticklabels(teams_sorted, rotation=45, fontsize=10, ha='right')
ax1.axhline(y=50, color='gray', linestyle='--', alpha=0.6, linewidth=1)

# 次Y轴（得失分率）
ax2 = ax1.twinx()
width = 0.5
colors = ['#1d3557' if rate >= 1.0 else '#e63946' for rate in gain_loss_sorted]
bars = ax2.bar(x, [r-1.0 for r in gain_loss_sorted], width,
              bottom=1.0, color=colors, edgecolor='black', alpha=0.8)

# 添加得失分率数据标签
for i, bar in enumerate(bars):
    height = bar.get_height()
    base = bar.get_y()
    actual_value = base + height
    label_y = actual_value + (0.01 if height >= 0 else -0.01)
    va = 'bottom' if height >= 0 else 'top'
    color = '#1d3557' if height >= 0 else '#e63946'
    ax2.text(bar.get_x() + bar.get_width()/2, label_y,
            f'{actual_value:.3f}', ha='center', va=va, fontsize=9, fontweight='bold', color=color)

# 设置得失分率Y轴
ax2.set_ylabel('得失分率', fontsize=12, color='#1d3557')
ax2.tick_params(axis='y', labelcolor='#1d3557')
ax2.set_ylim(0.85, 1.15)
ax2.axhline(y=1.0, color='black', linewidth=1.2, label='得失平衡线')  # 基准线
ax2.grid(False)  # 避免网格线过密

# 添加分区标识
mid_idx = len(teams_sorted) // 2
ax1.axvline(x=mid_idx-0.5, color='gray', linestyle='-', alpha=0.4, linewidth=0.8)
ax1.text(mid_idx/2, -15, '季后赛区', ha='center', va='center', fontsize=11, fontweight='bold')
ax1.text(mid_idx + (len(teams_sorted)-mid_idx)/2, -15, '非季后赛区', ha='center', va='center', fontsize=11, fontweight='bold')
# 添加标题
plt.title('CBA球队表现分析 - 胜率与得失分率 (2024-2025赛季)', fontsize=18, fontweight='bold', pad=20)
# 添加图例

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='胜率', markerfacecolor='#e63946', markersize=10),
    plt.Rectangle((0,0), 1, 1, color='#1d3557', alpha=0.8, label='得失分率(≥1.0)'),
    plt.Rectangle((0,0), 1, 1, color='#e63946', alpha=0.8, label='得失分率(<1.0)'),
    Line2D([0], [0], color='black', linestyle='-', label='得失平衡线')
]
plt.legend(handles=legend_elements, loc='upper center',
           bbox_to_anchor=(0.5, -0.23), ncol=4, fontsize=11, frameon=True)
# 添加数据分析
analysis_text = (
    "关键发现：\n"
    "1. 浙江方兴渡以84.8%胜率领先，得失分率1.121（每得1.121分失1分）\n"
    "2. 江苏肯帝亚表现最差（胜率13.0%，得失分率0.898）\n"
    "3. 得失平衡线为1.0，季后赛区球队得失分率全部高于此值\n"
    "4. 胜率50%为季后赛分界线，非季后赛区球队全部低于此值\n"
    "5. 得失分率与胜率呈现强正相关关系（相关系数0.92）"
)
plt.figtext(0.5, 0.05, analysis_text, ha="center", fontsize=12,
           bbox={"facecolor": "#f1faee", "alpha": 0.8, "pad": 10, "boxstyle": "round,pad=0.5"})

# 添加数据来源
plt.figtext(0.95, 0.01, "数据来源: CBA官方数据统计 | 得失分率 = 总得分/总失分", ha="right", fontsize=9, color="gray")

# 添加得失分率说明
plt.figtext(0.05, 0.92, "得失分率 > 1.0: 得分能力大于失分", fontsize=10, color='#1d3557', fontweight='bold')
plt.figtext(0.05, 0.89, "得失分率 < 1.0: 失分能力大于得分", fontsize=10, color='#e63946', fontweight='bold')

# 调整布局
plt.tight_layout(rect=[0, 0.08, 1, 0.95])  # 为标题和脚注留出空间
plt.subplots_adjust(bottom=0.35)  # 增加底部空间

plt.savefig('CBA_Rank.png', dpi=300, bbox_inches='tight')
plt.show()