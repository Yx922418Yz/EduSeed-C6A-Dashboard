# C6A 拿来说明

## 借鉴与使用的资源

| 拿来什么 | 从哪拿 | 怎么改 |
|----------|--------|--------|
| 数据 Schema | C6A CHALLENGE.md "提交记录 Schema" / "挑战要求 Schema" | 转成 Python 字典和 list，加 is_real/is_demo 标注字段 |
| ECharts | jsDelivr CDN echarts@5.5.0 | 柱状图（按挑战完成率）+ 环形图（状态分布） |
| openpyxl 条件样式 | openpyxl 文档 | 直接 PatternFill 给缺失单元格上红底，不用条件格式规则 |
| 数据诚实原则 | C4A 评审技能 + CHALLENGE.md 要求 | JSON 字段 + 数据说明.md + 仪表盘横幅三处标注 |
| 静态 HTML 内嵌数据 | file:// 下 fetch 被拦的通用坑 | JSON.stringify 后内嵌为 `const DATA = {...}` |

## 没有使用
- 没有用 Streamlit / Flask（纯静态，双击即开）。
- 没有用真实同学数据（演示数据全部虚构并标注）。
