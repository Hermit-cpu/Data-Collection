# 篮球联赛数据爬虫采集与可视化分析

​      本项目是一个基于 Python 的体育数据采集与分析工具，从腾讯体育 API 获取 CBA、NBA 以及欧洲冠军联赛（CHL）的球员数据、球队排名和赛程信息，并将数据存储到 MySQL 数据库中，同时生成多维度的可视化图表，用于对比分析不同联赛的球队表现与球员能力。

## 功能特性

- **数据采集**
  使用 `requests` 库模拟浏览器请求，从腾讯体育公开接口获取：
  - 球员个人数据（得分、篮板、助攻等）
  - 球队排名（胜率、得失分率、积分等）
  - 赛程信息（比赛时间、对阵双方、比分）
- **数据存储**
  通过 `pymysql` 将采集的数据存入本地 MySQL 数据库，支持增量更新。
- **可视化分析**
  利用 `matplotlib` 生成多种统计图表：
  - CBA 球队胜率 & 得失分率组合图（`CBA_Rank.png`）
  - 欧冠联赛积分榜 & 得失分率对比图（`CHL_Rank.png`）
  - NBA 东西部战区胜率 & 净胜率对比图（`NBA_Rank.png`，代码已注释，可取消注释生成）
  - CBA 与 NBA 球员综合得分横向条形图（`NBA_CBA_Player.png`）

## 项目结构

```tex
.
├── CBAPlayer.py          # 采集 CBA 球员数据
├── CBARank.py            # 采集 CBA 球队排名并绘制图表
├── CBASchedule.py        # 采集 CBA 赛程
├── CHLPlayer.py          # 采集欧冠球员数据
├── CHLRank.py            # 欧冠排名数据（硬编码）并绘制图表
├── CHLSchedule.py        # 采集欧冠赛程
├── NBAPlayer.py          # 采集 NBA 球员数据（仅输出简化列表）
├── NBARank.py            # 采集 NBA 东西部排名（可视化代码已注释）
├── NBASchedule.py        # 采集 NBA 赛程
├── Visualization.py      # 从数据库读取 CBA/NBA 球员数据，生成对比图
└── README.md             # 项目说明文档
```

> 注意：部分脚本中的数据库插入语句被注释，用户可根据需要取消注释以保存数据。

## 环境依赖

### Python 版本

- Python 3.11

### 第三方库

| 库           | 用途                    |
| :----------- | :---------------------- |
| `requests`   | 发送 HTTP 请求          |
| `pymysql`    | 连接和操作 MySQL 数据库 |
| `matplotlib` | 数据可视化              |
| `numpy`      | 数值计算与排序          |

安装命令：



```bash
pip install requests pymysql matplotlib numpy
```



### 中文字体支持（用于图表）

- Windows：通常已包含 `SimHei` 或 `Microsoft YaHei`
- Linux：需安装中文字体包，例如 `fonts-wqy-microhei`
- macOS：系统自带 `STHeiti` 等

如果图表中文显示为方框，请修改脚本中的 `plt.rcParams['font.sans-serif']` 列表，替换为系统可用的中文字体。

## 数据库配置

项目使用 MySQL 作为数据存储，数据库名称为 `datacollection`。请在运行脚本前完成以下步骤：

1. **安装 MySQL** 并启动服务。

2. **创建数据库**：

   ```sql
   CREATE DATABASE datacollection CHARACTER SET utf8mb4;
   ```

3. **创建数据表**（表结构需根据插入字段自行定义，参考各脚本中的 `INSERT` 语句）：

   - `cbaplayer`
   - `cbarank`
   - `cbaschedule`
   - `chlplayer`
   - `chlrank`
   - `chlschedule`
   - `nbaplayer`
   - `nbarank`
   - `nbaschedule`

4. **修改数据库连接参数**
   所有脚本中均硬编码了连接信息：

   ```python
   connect=pymysql.Connect(
       host='localhost',
       port=3306,
       user='root',
       passwd='123456',
       db='datacollection',
       charset='utf8'
   )
   ```

   请根据你的实际环境修改 `user`、`passwd` 等参数。

## 使用说明

### 1. 采集数据并存入数据库

以 CBA 球员数据为例：

- 编辑 `CBAPlayer.py`，取消注释数据库插入相关代码（约第 22–32 行）。

- 运行脚本：

  

  ```bash
  python CBAPlayer.py
  ```

同理，其他 `*Player.py`、`*Rank.py`、`*Schedule.py` 均可按需运行。

> 注意：`CHLRank.py` 未使用爬虫数据，而是内置了静态数据，可直接运行生成图表。
> `NBARank.py` 的可视化代码已被注释，如需生成图表请取消末尾注释。

### 2. 生成可视化图表

- **CBA 球队表现图**：运行 `CBARank.py`（需先取消数据库插入注释，或保留原样，可视化部分独立执行）。
- **欧冠球队分析图**：运行 `CHLRank.py`。
- **NBA 东西部对比图**：运行 `NBARank.py` 并取消末尾注释。
- **CBA vs NBA 球员得分对比**：
  - 先运行 `CBAPlayer.py` 和 `NBAPlayer.py` 将数据存入数据库（确保表中有数据）。
  - 再运行 `Visualization.py` 生成 `NBA_CBA_Player.png`。

生成的图片默认保存在脚本同级目录下。

## 注意事项

1. **API 请求限制**
   所有请求均使用静态 `User-Agent`，未设置延时。若频繁运行可能触发反爬机制，建议适当增加 `time.sleep()`。
2. **数据时效性**
   采集的 URL 中包含固定参数（如 `competition_id`、`qimei` 等），这些接口返回的是当前赛季数据。若赛季更新，可能需要修改 `season_id` 或重新获取接口地址。
3. **欧冠数据的特殊处理**
   `CHLRank.py` 中的数据为手动整理（来自欧冠官方统计），并非实时爬取。如需动态数据，请自行寻找替代 API。
4. **数据库操作风险**
   插入语句未使用 `ON DUPLICATE KEY UPDATE` 或事务回滚，重复运行会导致主键冲突或数据重复。建议在批量插入前清空相关表或改用 `REPLACE`。
5. **可视化效果调整**
   由于不同操作系统的字体和显示分辨率差异，图表中的标签位置可能偏移。可调整 `figsize`、`text` 的 `offset` 参数优化。

## 示例图表

（以下为生成的图片预览，请在实际运行后查看）

- **CBA_Rank.png**：展示 CBA 球队胜率与得失分率的关系，并标注季后赛分界线。
- **CHL_Rank.png**：欧冠球队积分柱状图叠加得失分率折线，区分争冠/中游/下游组。
- **NBA_CBA_Player.png**：横向条形图对比两联赛球员综合得分，突出顶级球员。

## 许可证

本项目仅供学习与数据分析交流使用，请勿用于商业用途。数据版权归腾讯体育及 CBA/NBA/欧冠官方所有。