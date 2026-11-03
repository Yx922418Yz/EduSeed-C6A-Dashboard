# C6A 教学说明

## 怎么运行
```powershell
# 1. 扫描真实提交 + 生成演示数据 → data/submissions.json
python build_dashboard.py

# 2. 生成 Excel 报表（自动 openpyxl 重载校验）
python build_excel.py

# 3. 生成静态仪表盘 HTML
python build_html.py

# 4. 双击 dashboard/index.html 即可在浏览器打开，无需服务器
```

## 依赖
- Python 3.13
- openpyxl 3.1.5（已装）
- 浏览器需要联网加载 ECharts CDN（jsDelivr）；离线时图表不渲染但表格仍可用。

## 怎么更新数据
- 新增真实提交：把新文件夹放进桌面 `提交挑战/`，在 `build_dashboard.py` 的 `scan_real_liyaxuan()` 里加一段扫描逻辑，重跑三个脚本。
- 新增演示同学：在 `DEMO_CLASSMATES` 列表里加一行。
- 新增挑战：在 `CHALLENGES` 字典里加必填项定义。

## 诚实边界
- 仪表盘里标"本人真实"的记录，确实来自本机磁盘扫描；标"演示样例"的是虚构的。
- 不要把演示数据当真汇报。
