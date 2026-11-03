# C6A 方案设计

## 目标
构建一个本地完整工程，把散落的课程提交数据变成结构化 JSON + 5-sheet Excel + ECharts 静态仪表盘。

## 数据模型（遵循 CHALLENGE.md Schema）
每条 record：
- `student`：name / name_pinyin / is_real_liyaxuan
- `challenge`：C2A / C2G / C4A-C4D / C5 / C6
- `submitted_at`：ISO8601
- `files[]`：{item, required, present}
- `status`：complete / partial / missing
- `completeness`：0~1
- `missing[]`：缺失的必填项
- `is_demo_data` / `note`：诚实标注

## 数据来源（诚实硬约束）
1. **李亚轩本人真实提交**：Python 脚本实际扫描桌面 `提交挑战/` 下 C2A_MetaCal-Shift、C2G_ParameterGolf、C4_技能分享与传播 三个文件夹，按文件存在性判定。
2. **同班同学演示样例**：10 位虚构同学（王小明、李思颖、张子涵、陈雨桐、刘浩然、赵欣怡、孙嘉怡、周宇航、吴梦琪、郑凯文），提交情况人工构造，每条都标注 `is_demo_data=true` 和"演示样例数据：虚构同学"。

## 技术选型
- 数据扫描：Python 3.13 + os.path
- Excel：openpyxl 3.1.5，5 个 sheet，缺失单元格红底（FFC7CE）
- 仪表盘：纯静态 HTML + ECharts 5.5（jsDelivr CDN），数据内嵌为 JS 变量（避免 file:// 下 fetch 被拦）
- 部署：GitHub Pages（dashboard/index.html），同时支持双击本地打开

## 五个 Sheet
1. 总览矩阵（学生×挑战，颜色编码）
2. 按学生（明细）
3. 按挑战（统计）
4. 时间线（按日期排序）
5. 缺失项（只列有缺失的，红底）
