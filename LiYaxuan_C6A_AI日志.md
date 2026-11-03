# C6A AI 日志

## 阶段 1：需求对齐
- 先 Read CHALLENGE.md 和 rubric.json，明确四级任务（Bronze 数据结构化 / Silver Excel / Gold 网站 / Platinum 自动化），本交付做到 Gold（Level 3）+ 部分 Level 1-2 自动化。
- AI 帮着把 CHALLENGE.md 里的 JSON Schema 提炼成 Python dataclass 结构。

## 阶段 2：数据扫描脚本
- AI 写 `build_dashboard.py`：定义 CHALLENGES 必填项字典，`scan_real_liyaxuan()` 用 os.path.exists 判定每个文件。
- AI 构造 DEMO_CLASSMATES：10 位虚构同学，每人 3-5 条提交，故意设计一些 partial/missing 状态用来演示高亮。
- 关键约束：每条记录都加 `is_real_liyaxuan` / `is_demo_data` / `note` 字段，绝不混淆。

## 阶段 3：Excel 生成
- AI 写 `build_excel.py`：5 个 sheet，用 openpyxl，缺失单元格填 FFC7CE 红底。
- 自动重载校验：脚本末尾 `load_workbook` 打印 sheet 名和 max_row，确认可开。

## 阶段 4：HTML 仪表盘
- AI 写 `build_html.py`：把 JSON 内嵌为 JS 变量（规避 file:// fetch 限制），用 ECharts 画柱状图 + 环形图。
- 交互：学生/挑战/状态三级筛选、导出 CSV、重置按钮。
- 诚实横幅：页面顶部黄底声明真实 vs 演示数据来源。

## 阶段 5：调试
- headless 截图发现仪表盘渲染正常；筛选"部分提交"后红底高亮明显。
- GitHub 上传用 gh_helper.py，upload-dir 8/8 成功，get 验证 JSON 内容。
