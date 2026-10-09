# EduSeed C6A 提交数据仪表盘

Elite20 课程提交数据的本地完整工程：扫描真实提交 + 构造演示数据集 → JSON / Excel / 静态 HTML 仪表盘。

## 数据来源（务必阅读）

本工程包含两类数据，**绝不混淆**：

1. **李亚轩本人真实提交**（`is_real_liyaxuan=true`）：由 `build_dashboard.py` 实际扫描本机桌面
   `C:\Users\lenovo\Desktop\提交挑战\` 下的 C2A / C2G / C4 三个文件夹得出。
2. **同班同学演示样例数据**（`is_demo_data=true`）：10 位虚构同学（王小明、李思颖、张子涵 等），
   仅用于演示仪表盘的筛选、高亮、统计功能，**不代表任何真实同学的提交状态**。

数据说明详见 `data/数据说明.md`，仪表盘页面顶部也有醒目声明。

## 工程结构

```
├─ build_dashboard.py   # 扫描真实提交 + 构造演示数据 → data/submissions.json
├─ build_excel.py       # 读取 JSON → report.xlsx（5 sheet，缺失单元格标红）
├─ build_html.py        # 读取 JSON → dashboard/index.html（ECharts 静态仪表盘）
├─ data/
│   ├─ submissions.json # 结构化数据
│   └─ 数据说明.md
├─ dashboard/
│   └─ index.html       # 双击即可在浏览器打开，无需服务器
└─ report.xlsx          # 5-sheet Excel 报表
```

## 运行

```powershell
python build_dashboard.py
python build_excel.py
python build_html.py
# 然后双击 dashboard/index.html
```

依赖：Python 3.13 + openpyxl 3.1.5。

## Excel 五个 Sheet

| Sheet | 内容 |
|-------|------|
| 总览矩阵 | 学生 × 挑战矩阵（完整/部分/缺失/未交） |
| 按学生 | 每个学生的所有提交详情 |
| 按挑战 | 每个挑战的提交统计 |
| 时间线 | 按提交日期排序 |
| 缺失项 | 只列有缺失的记录，缺失单元格红底 |
