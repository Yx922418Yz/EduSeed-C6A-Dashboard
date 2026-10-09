# -*- coding: utf-8 -*-
"""读取 submissions.json，用 openpyxl 生成 5-sheet report.xlsx，缺失单元格标红。"""
import os, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "data", "submissions.json"), encoding="utf-8") as f:
    data = json.load(f)
records = data["records"]
challenges = list(data["meta"]["challenges"].keys())
students = sorted(set(r["student"]["name"] for r in records),
                  key=lambda n: (n != "李亚轩", n))

RED = PatternFill("solid", fgColor="FFC7CE")
GREEN = PatternFill("solid", fgColor="C6EFCE")
YELLOW = PatternFill("solid", fgColor="FFEB9C")
HEAD = PatternFill("solid", fgColor="0F6E6E")
HEAD_FONT = Font(bold=True, color="FFFFFF", size=11)
THIN = Side(style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def style_header(ws, row=1):
    for c in ws[row]:
        c.fill = HEAD; c.font = HEAD_FONT; c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BORDER

def auto_width(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

wb = Workbook()

# ---- Sheet 1: 总览矩阵 ----
ws1 = wb.active; ws1.title = "总览矩阵"
header = ["学生"] + challenges + ["完成数", "总数", "完成率"]
ws1.append(header)
for stu in students:
    row = [stu]
    done = 0; total = len(challenges)
    for cid in challenges:
        rec = next((r for r in records if r["student"]["name"] == stu and r["challenge"] == cid), None)
        if rec is None:
            row.append("—")  # 未提交
        else:
            row.append(rec["status"])
            done += 1
    rate = round(done / total, 2) if total else 0
    row += [done, total, rate]
    ws1.append(row)
# 染色
for r in range(2, ws1.max_row + 1):
    for c in range(2, 2 + len(challenges)):
        cell = ws1.cell(row=r, column=c)
        if cell.value == "complete": cell.fill = GREEN
        elif cell.value == "partial": cell.fill = YELLOW
        elif cell.value == "missing": cell.fill = RED
        elif cell.value == "—": cell.fill = PatternFill("solid", fgColor="F2F2F2")
style_header(ws1); auto_width(ws1, [12] + [8]*len(challenges) + [8, 8, 10])
ws1.freeze_panes = "B2"

# ---- Sheet 2: 按学生 ----
ws2 = wb.create_sheet("按学生")
ws2.append(["学生", "真实/演示", "挑战", "挑战标题", "提交时间", "状态", "完成度", "缺失项"])
for r in records:
    ws2.append([
        r["student"]["name"],
        "本人真实" if r["student"]["is_real_liyaxuan"] else "演示样例",
        r["challenge"], r["challenge_title"], r["submitted_at"][:10],
        r["status"], r["completeness"],
        "、".join(r["missing"]) if r["missing"] else "—",
    ])
for r in range(2, ws2.max_row + 1):
    st = ws2.cell(row=r, column=6).value
    fill = GREEN if st == "complete" else YELLOW if st == "partial" else RED
    ws2.cell(row=r, column=6).fill = fill
    if ws2.cell(row=r, column=8).value != "—":
        ws2.cell(row=r, column=8).fill = RED
style_header(ws2); auto_width(ws2, [10, 10, 8, 24, 12, 10, 8, 30])
ws2.freeze_panes = "A2"

# ---- Sheet 3: 按挑战 ----
ws3 = wb.create_sheet("按挑战")
ws3.append(["挑战", "标题", "应交人数", "完整提交", "部分提交", "未交/缺失", "完成率"])
for cid in challenges:
    subs = [r for r in records if r["challenge"] == cid]
    n = len(students)
    comp = sum(1 for r in subs if r["status"] == "complete")
    part = sum(1 for r in subs if r["status"] == "partial")
    miss = n - comp - part
    rate = round(comp / n, 2) if n else 0
    ws3.append([cid, data["meta"]["challenges"][cid]["title"], n, comp, part, miss, rate])
for r in range(2, ws3.max_row + 1):
    ws3.cell(row=r, column=6).fill = RED if ws3.cell(row=r, column=6).value > 0 else GREEN
style_header(ws3); auto_width(ws3, [8, 28, 10, 10, 10, 10, 10])

# ---- Sheet 4: 时间线 ----
ws4 = wb.create_sheet("时间线")
ws4.append(["提交日期", "学生", "挑战", "状态", "完成度", "备注"])
timeline = sorted(records, key=lambda r: r["submitted_at"])
for r in timeline:
    ws4.append([r["submitted_at"][:10], r["student"]["name"], r["challenge"],
                r["status"], r["completeness"], r.get("note", "")[:40]])
for r in range(2, ws4.max_row + 1):
    st = ws4.cell(row=r, column=4).value
    ws4.cell(row=r, column=4).fill = GREEN if st == "complete" else YELLOW if st == "partial" else RED
style_header(ws4); auto_width(ws4, [12, 10, 8, 10, 8, 40])
ws4.freeze_panes = "A2"

# ---- Sheet 5: 缺失项（只列有缺失的） ----
ws5 = wb.create_sheet("缺失项")
ws5.append(["学生", "真实/演示", "挑战", "缺失的必填项", "完成度", "备注"])
missing_rows = [r for r in records if r["missing"]]
for r in missing_rows:
    ws5.append([
        r["student"]["name"],
        "本人真实" if r["student"]["is_real_liyaxuan"] else "演示样例",
        r["challenge"], "、".join(r["missing"]), r["completeness"],
        r.get("note", "")[:40],
    ])
for row in ws5.iter_rows(min_row=2, max_row=ws5.max_row, min_col=4, max_col=4):
    for cell in row:
        cell.fill = RED; cell.font = Font(bold=True, color="9C0006")
style_header(ws5); auto_width(ws5, [10, 10, 8, 30, 8, 40])
ws5.freeze_panes = "A2"

out = os.path.join(ROOT, "report.xlsx")
wb.save(out)
print(f"Excel saved: {out}, sheets={wb.sheetnames}")

# 校验：openpyxl 重新加载
from openpyxl import load_workbook
wb2 = load_workbook(out)
print(f"Reload OK: {wb2.sheetnames}, dims={[wb2[s].max_row for s in wb2.sheetnames]}")
