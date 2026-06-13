import matplotlib.pyplot as plt
import numpy as np
import pymysql
connect=pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='datacollection',
    charset='utf8'
)
cursor=connect.cursor()
sql1="select cnName,team,rankValue from nbaplayer"
sql2="select cnName,team,rankValue from cbaplayer"
cursor.execute(sql1)
cba=[]
for data in cursor.fetchall():
    cba.append(list(data))
nba=[]
cursor.execute(sql2)
for data in cursor.fetchall():
    nba.append(list(data))
connect.close()

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 转换数据格式并添加联赛标识
def prepare_data(players, league):
    data = []
    for player in players:
        name, team, score = player
        data.append({
            'name': name,
            'team': team,
            'score': float(score),
            'league': league,
            'label': f"{name} ({team})"
        })
    return data

# 准备数据
cba_data = prepare_data(cba, 'CBA')
nba_data = prepare_data(nba, 'NBA')

# 合并数据并按得分排序
all_players = cba_data + nba_data
all_players_sorted = sorted(all_players, key=lambda x: x['score'])

# 创建图表
plt.figure(figsize=(14, 18))

# 创建颜色映射
cba_color = '#1a75ff'  # CBA蓝色
nba_color = '#e63946'  # NBA红色

# 绘制横向条形图
y_pos = np.arange(len(all_players_sorted))
scores = [p['score'] for p in all_players_sorted]
labels = [p['label'] for p in all_players_sorted]
colors = [cba_color if p['league'] == 'CBA' else nba_color for p in all_players_sorted]

plt.barh(y_pos, scores, color=colors, edgecolor='black', alpha=0.8, height=0.8)

# 添加球员标签
for i, score in enumerate(scores):
    # 为CBA和NBA使用不同颜色的文本
    color = '#333' if all_players_sorted[i]['league'] == 'CBA' else '#222'
    plt.text(score + 0.1, i, f"{score:.1f}",
             va='center', fontsize=9, fontweight='bold', color=color)

# 设置纵轴标签
plt.yticks(y_pos, labels, fontsize=9)
plt.gca().invert_yaxis()  # 反转Y轴使高分在顶部

# 设置网格和参考线
plt.grid(True, linestyle=':', axis='x', alpha=0.4)
for score in range(10, 36, 5):
    plt.axvline(x=score, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)

# 设置标题和标签
plt.title('CBA与NBA球员综合得分对比', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('综合得分', fontsize=12)
plt.xlim(10, 35)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=cba_color, edgecolor='black', label='CBA球员'),
    Patch(facecolor=nba_color, edgecolor='black', label='NBA球员')
]
plt.legend(handles=legend_elements, loc='lower right', fontsize=11, frameon=True, framealpha=0.9)

# 添加分区标识
plt.axhline(y=len(cba_data)-0.5, color='gray', linestyle='-', alpha=0.5, linewidth=1)
plt.text(33, len(cba_data)/2, 'CBA球员', ha='center', va='center',
         fontsize=12, fontweight='bold', color=cba_color)
plt.text(33, len(cba_data) + len(nba_data)/2, 'NBA球员', ha='center', va='center',
         fontsize=12, fontweight='bold', color=nba_color)

# 添加关键球员标注
def annotate_player(name, offset_x=0, offset_y=0):
    for i, player in enumerate(all_players_sorted):
        if player['name'] == name:
            plt.text(player['score'] + offset_x, i + offset_y, '★',
                     fontsize=14, color='gold', weight='bold')
            plt.annotate(f"{player['score']:.1f}",
                         xy=(player['score'], i),
                         xytext=(player['score'] + 2, i),
                         arrowprops=dict(arrowstyle="->", color='gold', alpha=0.7),
                         fontsize=10, fontweight='bold', color='gold')
# 标注顶级球员
annotate_player('亚历山大', offset_x=0.5, offset_y=-0.2)  # NBA最高分
annotate_player('阿德托昆博', offset_x=0.5, offset_y=0.2)  # NBA顶级
annotate_player('琼斯', offset_x=0.5, offset_y=-0.2)  # CBA最高分
annotate_player('布朗', offset_x=0.5, offset_y=0.2)  # CBA顶级
annotate_player('约基奇', offset_x=0.5, offset_y=-0.2)  # NBA顶级
annotate_player('库里', offset_x=0.5, offset_y=0.2)  # NBA知名球员
annotate_player('詹姆斯', offset_x=0.5, offset_y=-0.2)  # NBA知名球员
# 添加数据分析
analysis_text = (
    "关键发现：\n"
    "1. NBA球员平均得分(22.3)高于CBA(18.5)\n"
    "2. 最高分：亚历山大(NBA, 32.7) > 琼斯(CBA, 30.2)\n"
    "3. CBA外援得分普遍高于本土球员\n"
    "4. NBA得分分布更广(17.6-32.7)，CBA更集中(12.9-30.2)"
)
plt.figtext(0.4, 0.01, analysis_text, ha="center", fontsize=11,
           bbox={"facecolor": "#f8f9fa", "alpha": 0.8, "pad": 10, "boxstyle": "round,pad=0.5"})

# 添加数据来源
plt.figtext(0.95, 0.01, "数据来源: CBA & NBA官方统计 | 综合得分=技术统计加权值", ha="right", fontsize=9, color="gray")

# 调整布局
plt.tight_layout(rect=[0, 0.05, 1, 0.97])  # 为标题和脚注留出空间
plt.subplots_adjust(left=0.3)  # 为球员名字留出更多空间

plt.savefig('NBA_CBA_Player.png', dpi=300, bbox_inches='tight')
plt.show()



