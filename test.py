import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as m_dates
from datetime import datetime

# 构造数据
names = ['v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
         'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
         'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
         'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0']

dates = ['2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
         '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
         '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
         '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
         '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
         '2014-10-26', '2014-10-18', '2014-08-26']

# 转换类型 date strings (e.g. 2014-10-18) to datetime
dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
print(dates)

# Choose some nice levels  定义纵轴长度
levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(dates) / 6)))[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
# 标题
ax.set(title="Matplotlib release dates")

# 添加线条, basefmt设置中线的颜色，linefmt设置线的颜色以及类型
markerline, stemline, baseline = ax.stem(dates, levels,
                                         linefmt="C3-", basefmt="k-",
                                         )
# 交点空心,zorder=3设置图层,mec="k"外黑 mfc="w"内白
plt.setp(markerline, mec="k", mfc="w", zorder=3)

# 通过将Y数据替换为零，将标记移到基线
markerline.set_ydata(np.zeros(len(dates)))

# 构造描述底部、顶部的array
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
print(np.array(['top', 'bottom']))
print(levels > 0)
print([(levels > 0).astype(int)])
print(vert)

# 添加文字注释
for d, l, r, va in zip(dates, levels, names, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                textcoords="offset points", va=va, ha="right")

# 设置x轴间隔为每四个月
ax.get_xaxis().set_major_locator(m_dates.MonthLocator(interval=4))
ax.get_xaxis().set_major_formatter(m_dates.DateFormatter("%b %Y\n"))
# 逆时针30度，刻度右对齐
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# 隐藏y轴线
ax.get_yaxis().set_visible(False)
# 隐藏左、上、右的边框
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)
# 边距仅设置y轴
ax.margins(y=0.1)
plt.show()
