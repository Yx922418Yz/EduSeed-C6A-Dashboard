# C6A AAR 复盘

## 做了什么
- 写了三个 Python 脚本：扫描真实提交、生成 Excel、生成 HTML 仪表盘。
- 扫描了桌面 C2A/C2G/C4 三个真实文件夹，识别出李亚轩 6 条完整提交记录。
- 构造了 10 位虚构同学的演示数据集（35 条记录），每条都明确标注。
- 生成了 5-sheet Excel（总览矩阵/按学生/按挑战/时间线/缺失项），缺失单元格红底。
- 生成了 ECharts 静态仪表盘：总览柱状图 + 状态环形图 + 可筛选明细表 + 导出 CSV。

## 学了什么
- 数据工程管线：磁盘扫描 → JSON → Excel → HTML，每一步都可独立重跑。
- 诚实标注的重要性：真实数据和演示数据必须在 JSON 字段、数据说明文档、仪表盘横幅三处都讲清楚。
- openpyxl 的条件样式：用 PatternFill 直接给缺失单元格上红底，不用条件格式规则。

## 怎么验证的
- `build_excel.py` 末尾用 `load_workbook` 重新打开 report.xlsx，打印 sheet 名和行数，确认 5 个 sheet 齐全可开。
- headless Edge 截图：总览页 + 筛选"部分提交"页，肉眼确认图表渲染、缺失高亮、真实/演示标签。
- GitHub REST API `get` 验证 data/submissions.json 内容正确。

## 失败经验
- 最初想让仪表盘 HTML 运行时 fetch JSON，但 file:// 协议下浏览器会拦 XHR，改为把 JSON 内嵌为 JS 变量，双击即开。
- headless 截图第一次没等到 ECharts CDN 加载，白图；加大 `--virtual-time-budget` 到 8000ms 后正常。

## 改进方向
- Level 4：自动监听桌面文件夹变化、自动重跑扫描；嵌入 C4A 评审标准做初步质量打分。
