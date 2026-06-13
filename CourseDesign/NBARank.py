import pymysql
import requests
import matplotlib.pyplot as plt
import numpy as np
# 爬取东西部战队排行
headers={'user-agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
url = "https://matchweb.sports.qq.com/match/api/v2/statistic/rankings?competition_id=100000&season_id=&season_type=&type=0&scene=pc&qimei=3799863a36ec750f91c3814702000000917910"
response = requests.get(url, headers=headers)
datas = response.json()['data']
east_rows = datas['groups'][0]['tables'][0]['rows']
west_rows = datas['groups'][0]['tables'][1]['rows']
east_columns = []
teams_url = []
for value in range(0,len(east_rows)):
    rows = {}
    for column in east_rows[value]['values']:
        if column['code'] == "team":
            rows[column['code']]=column['value']['cnName']
            teams_url.append(column['value']['jumpData']['param']['url'])
        else:
            rows[column['code']]=column['value']
    east_columns.append(rows)
west_columns = []
for value in range(0,len(west_rows)):
    rows = {}
    for column in west_rows[value]['values']:
        if column['code'] == "team":
            rows[column['code']] = column['value']['cnName']
            teams_url.append(column['value']['jumpData']['param']['url'])
        else:
            rows[column['code']] = column['value']
    west_columns.append(rows)
east_data = [list(data.values()) for data in east_columns]
west_data = [list(data.values()) for data in west_columns]
print(east_data)
print()
# 保存到数据库
# connect=pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='datacollection',
#     charset='utf8'
# )
# cursor=connect.cursor()
# sql="INSERT INTO nbarank VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# for data in east_data:
#     cursor.execute(sql,data)
# for data in west_data:
#     cursor.execute(sql,data)
# connect.commit()
# connect.close()
# 设置中文字体支持
# plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'sans-serif']
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# # 数据准备 - 东部战区
# east_teams = [team[1] for team in east_data]
# east_win_rates = [winRate[5] for winRate in east_data]
# east_net_rates = [pointsDifference[11] for pointsDifference in east_data]
# # 数据准备 - 西部战区
# west_teams = [team[1] for team in west_data]
# west_win_rates = [winRate[5] for winRate in west_data]
# west_net_rates = [pointsDifference[11] for pointsDifference in west_data]
# # 转换数据格式
# def convert_data(teams, win_rates, net_rates):
#     win_rates_float = [float(rate.strip('%')) for rate in win_rates]
#     net_rates_float = [float(rate) for rate in net_rates]
#     sorted_idx = np.argsort(win_rates_float)[::-1]
#     return (
#         [teams[i] for i in sorted_idx],
#         [win_rates_float[i] for i in sorted_idx],
#         [net_rates_float[i] for i in sorted_idx]
#     )
# # 处理东西部数据
# east_teams, east_win, east_net = convert_data(east_teams, east_win_rates, east_net_rates)
# west_teams, west_win, west_net = convert_data(west_teams, west_win_rates, west_net_rates)
# # 创建图表 - 1行2列
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
# plt.subplots_adjust(wspace=0.3)  # 调整子图间距
# def setup_plot(ax, teams, win_rates, net_rates, title):
#     x = np.arange(len(teams))
#     width = 0.35
#     # 绘制胜率折线图
#     line = ax.plot(x, win_rates, 'o-', color='#e63946', linewidth=2,
#                    markersize=6, markerfacecolor='white', markeredgewidth=1.5,
#                    label='胜率 (%)')
#     # 添加胜率数据标签
#     for i, rate in enumerate(win_rates):
#         offset = 1.5 if i != 0 else -3.5  # 避免重叠
#         ax.text(i, rate + offset, f'{rate:.1f}%',
#                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='#e63946')
#     # 创建第二个Y轴（净胜率）
#     ax2 = ax.twinx()
#     colors = ['#457b9d' if rate >= 0 else '#e63946' for rate in net_rates]
#     bars = ax2.bar(x, net_rates, width, color=colors, edgecolor='black', alpha=0.8, label='净胜率')
#     # 添加净胜率数据标签
#     for i, bar in enumerate(bars):
#         height = bar.get_height()
#         va = 'bottom' if height >= 0 else 'top'
#         offset = 0.2 if height >= 0 else -0.2
#         color = '#1d3557' if height >= 0 else '#e63946'
#         ax2.text(bar.get_x() + bar.get_width() / 2, height + offset,
#                  f'{height:.1f}', ha='center', va=va, fontsize=9, fontweight='bold', color=color)
#     # 设置主Y轴（胜率）
#     ax.set_ylabel('胜率 (%)', fontsize=10, color='#e63946')
#     ax.tick_params(axis='y', labelcolor='#e63946')
#     ax.set_ylim(0, 100)
#     ax.grid(True, linestyle=':', alpha=0.5, axis='y')
#     ax.set_xticks(x)
#     ax.set_xticklabels(teams, rotation=45, fontsize=9, ha='right')
#     ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
#     ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
#     # 设置次Y轴（净胜率）
#     ax2.set_ylabel('净胜率', fontsize=10, color='#457b9d')
#     ax2.tick_params(axis='y', labelcolor='#457b9d')
#     # 添加零线
#     ax2.axhline(y=0, color='black', linewidth=0.8)
#     # 添加图例
#     from matplotlib.lines import Line2D
#     legend_elements = [
#         Line2D([0], [0], marker='o', color='w', label='胜率', markerfacecolor='#e63946', markersize=8),
#         plt.Rectangle((0, 0), 1, 1, color='#457b9d', alpha=0.8, label='净胜率(正)'),
#         plt.Rectangle((0, 0), 1, 1, color='#e63946', alpha=0.8, label='净胜率(负)')
#     ]
#     ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15),
#               ncol=3, fontsize=9, frameon=True, framealpha=0.9)
# # 绘制东部战区
# setup_plot(ax1, east_teams, east_win, east_net, 'NBA东部战区球队表现')
# # 绘制西部战区
# setup_plot(ax2, west_teams, west_win, west_net, 'NBA西部战区球队表现')
# # 添加整体标题
# plt.suptitle('NBA东西部战区球队表现对比分析', fontsize=18, fontweight='bold', y=0.98)
# # 添加分析注释
# analysis_text = (
#     "关键发现：\n"
#     "- 东部领先者：雷霆(胜率82.9%，净胜率+12.9)\n"
#     "- 西部领先者：骑士(胜率78.0%，净胜率+9.5)\n"
#     "- 东部垫底：爵士(胜率20.7%，净胜率-9.3)\n"
#     "- 西部垫底：奇才(胜率22.0%，净胜率-12.4)\n"
#     "- 东西部均有明显梯队分化"
# )
# plt.figtext(0.5, 0.01, analysis_text, ha="center", fontsize=11,
#             bbox={"facecolor": "#f8f9fa", "alpha": 0.7, "pad": 10, "boxstyle": "round,pad=0.3"})
# plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 为标题和脚注留出空间
# plt.savefig('NBA_Rank.png', dpi=300, bbox_inches='tight')
# plt.show()

