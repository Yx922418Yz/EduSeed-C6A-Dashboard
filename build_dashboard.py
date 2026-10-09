# -*- coding: utf-8 -*-
"""
EduSeed C6A 提交数据仪表盘构建脚本
- 扫描桌面真实提交（李亚轩本人）
- 构造明确标注的同班同学演示数据集
- 输出 JSON / Excel(5 sheet) / 静态 HTML 仪表盘
"""
import os, json, datetime, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DESKTOP_SUBMIT = r"C:\Users\lenovo\Desktop\提交挑战"

# ============ 1. 挑战必填项定义 ============
CHALLENGES = {
    "C2A": {"title": "MetaCal-Shift 认知校准", "required": ["方案设计", "AI日志", "AAR复盘", "拿来说明", "核心产物"]},
    "C2G": {"title": "ParameterGolf 参数高尔夫", "required": ["方案设计", "AI日志", "AAR复盘", "拿来说明", "技术报告", "提交包"]},
    "C4A": {"title": "技能评审器", "required": ["技能包", "方案设计", "AI日志", "教学说明", "拿来说明"]},
    "C4B": {"title": "公众号文章生成", "required": ["技能包", "方案设计", "AI日志", "教学说明", "拿来说明", "输出文章"]},
    "C4C": {"title": "作业自动求解", "required": ["技能包", "方案设计", "AI日志", "教学说明", "拿来说明"]},
    "C4D": {"title": "本地大模型 Agent", "required": ["技能包", "方案设计", "AI日志", "教学说明", "拿来说明", "验证报告"]},
    "C5":  {"title": "GitHub 仓库", "required": ["仓库链接", "README", "AI日志"]},
    "C6":  {"title": "Web Application", "required": ["线上URL", "仓库链接", "AI日志", "拿来说明", "演示截图"]},
}

# ============ 2. 扫描李亚轩真实提交 ============
def scan_real_liyaxuan():
    records = []
    # C2A
    c2a_dir = os.path.join(DESKTOP_SUBMIT, "C2A_MetaCal-Shift")
    c2a_files = {
        "方案设计": os.path.exists(os.path.join(c2a_dir, "LiYaxuan_C2A_proposal.md")),
        "AI日志": os.path.exists(os.path.join(c2a_dir, "LiYaxuan_C2A_AI日志.md")),
        "AAR复盘": os.path.exists(os.path.join(c2a_dir, "LiYaxuan_C2A_AAR七维复盘.md")),
        "拿来说明": os.path.exists(os.path.join(c2a_dir, "LiYaxuan_C2A_拿来说明.md")),
        "核心产物": os.path.exists(os.path.join(c2a_dir, "benchmark", "data", "results.json")),
    }
    records.append(make_record("李亚轩", "LiYaxuan", "C2A", "2026-10-03T13:00:00+08:00", c2a_files, real=True,
                               note="真实提交：桌面 C2A_MetaCal-Shift 文件夹扫描"))

    # C2G
    c2g_dir = os.path.join(DESKTOP_SUBMIT, "C2G_ParameterGolf")
    c2g_files = {
        "方案设计": os.path.exists(os.path.join(c2g_dir, "docs", "LiYaxuan_C2G_方案设计.md")),
        "AI日志": os.path.exists(os.path.join(c2g_dir, "docs", "LiYaxuan_C2G_AI日志.md")),
        "AAR复盘": os.path.exists(os.path.join(c2g_dir, "docs", "LiYaxuan_C2G_AAR七维复盘.md")),
        "拿来说明": os.path.exists(os.path.join(c2g_dir, "docs", "LiYaxuan_C2G_拿来说明.md")),
        "技术报告": os.path.exists(os.path.join(c2g_dir, "docs", "LiYaxuan_C2G_tech_report.pdf")),
        "提交包": os.path.exists(os.path.join(c2g_dir, "LiYaxuan_C2G_提交文件", "LiYaxuan_C2G_submission.tar.gz")),
    }
    records.append(make_record("李亚轩", "LiYaxuan", "C2G", "2026-10-03T14:00:00+08:00", c2g_files, real=True,
                               note="真实提交：桌面 C2G_ParameterGolf 文件夹扫描"))

    # C4 系列（C4A/C4B/C4C/C4D）
    c4_base = os.path.join(DESKTOP_SUBMIT, "C4_技能分享与传播")
    c4_map = {
        "C4A": ("01_C4A_技能评审", "LiYaxuan_C4A_skill-evaluator.skill"),
        "C4B": ("02_C4B_公众号发布", "LiYaxuan_C4B_wechat-publisher.skill"),
        "C4C": ("03_C4C_作业求解", "LiYaxuan_C4C_homework-solver.skill"),
        "C4D": ("04_C4D_本地Agent", "LiYaxuan_C4D_Agent技能.skill"),
    }
    for cid, (sub, skillfile) in c4_map.items():
        d = os.path.join(c4_base, sub)
        files = {
            "技能包": os.path.exists(os.path.join(d, skillfile)),
            "方案设计": os.path.exists(os.path.join(d, f"LiYaxuan_{cid}_方案设计.md")),
            "AI日志": os.path.exists(os.path.join(d, f"LiYaxuan_{cid}_AI日志.md")),
            "教学说明": os.path.exists(os.path.join(d, f"LiYaxuan_{cid}_教学说明.md")),
            "拿来说明": os.path.exists(os.path.join(d, f"LiYaxuan_{cid}_拿来说明.md")),
        }
        if cid == "C4B":
            files["输出文章"] = os.path.exists(os.path.join(d, "LiYaxuan_C4B_output.html"))
        if cid == "C4D":
            files["验证报告"] = os.path.exists(os.path.join(d, "LiYaxuan_C4D_验证报告.md"))
        records.append(make_record("李亚轩", "LiYaxuan", cid, "2026-10-04T10:00:00+08:00", files, real=True,
                                   note=f"真实提交：桌面 C4_技能分享与传播/{sub} 扫描"))
    return records

# ============ 3. 演示数据集（虚构同学，明确标注） ============
DEMO_CLASSMATES = [
    # (姓名, 拼音, {挑战: {必填项: 是否有}})
    ("王小明", "WangXiaoming", {
        "C2A": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"核心产物":True},
        "C2G": {"方案设计":True,"AI日志":True,"AAR复盘":False,"拿来说明":True,"技术报告":True,"提交包":True},
        "C4A": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C4B": {"技能包":True,"方案设计":True,"AI日志":False,"教学说明":True,"拿来说明":True,"输出文章":True},
        "C5":  {"仓库链接":True,"README":True,"AI日志":True},
    }),
    ("李思颖", "LiSiying", {
        "C2A": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"核心产物":False},
        "C4B": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":False,"拿来说明":True,"输出文章":True},
        "C4C": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C5":  {"仓库链接":True,"README":True,"AI日志":False},
    }),
    ("张子涵", "ZhangZihan", {
        "C2G": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"技术报告":False,"提交包":True},
        "C4A": {"技能包":True,"方案设计":False,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C4D": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True,"验证报告":False},
        "C5":  {"仓库链接":True,"README":True,"AI日志":True},
    }),
    ("陈雨桐", "ChenYutong", {
        "C2A": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"核心产物":True},
        "C2G": {"方案设计":True,"AI日志":False,"AAR复盘":False,"拿来说明":False,"技术报告":False,"提交包":False},
        "C4B": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True,"输出文章":True},
        "C6":  {"线上URL":True,"仓库链接":True,"AI日志":True,"拿来说明":True,"演示截图":True},
    }),
    ("刘浩然", "LiuHaoran", {
        "C4C": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C4D": {"技能包":True,"方案设计":True,"AI日志":False,"教学说明":True,"拿来说明":True,"验证报告":True},
        "C5":  {"仓库链接":True,"README":False,"AI日志":True},
    }),
    ("赵欣怡", "ZhaoXinyi", {
        "C2A": {"方案设计":True,"AI日志":True,"AAR复盘":False,"拿来说明":True,"核心产物":True},
        "C4A": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":False},
        "C4B": {"技能包":False,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True,"输出文章":True},
    }),
    ("孙嘉怡", "SunJiayi", {
        "C2G": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"技术报告":True,"提交包":True},
        "C4C": {"技能包":True,"方案设计":False,"AI日志":True,"教学说明":False,"拿来说明":True},
        "C5":  {"仓库链接":True,"README":True,"AI日志":True},
        "C6":  {"线上URL":True,"仓库链接":True,"AI日志":False,"拿来说明":True,"演示截图":True},
    }),
    ("周宇航", "ZhouYuhang", {
        "C4A": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C4D": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True,"验证报告":True},
    }),
    ("吴梦琪", "WuMengqi", {
        "C2A": {"方案设计":True,"AI日志":False,"AAR复盘":False,"拿来说明":True,"核心产物":True},
        "C4B": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True,"输出文章":False},
        "C5":  {"仓库链接":False,"README":False,"AI日志":False},
    }),
    ("郑凯文", "ZhengKaiwen", {
        "C2G": {"方案设计":True,"AI日志":True,"AAR复盘":True,"拿来说明":True,"技术报告":True,"提交包":True},
        "C4C": {"技能包":True,"方案设计":True,"AI日志":True,"教学说明":True,"拿来说明":True},
        "C6":  {"线上URL":True,"仓库链接":True,"AI日志":True,"拿来说明":True,"演示截图":True},
    }),
]

def make_record(name, pinyin, cid, submitted_at, files, real, note=""):
    req = CHALLENGES[cid]["required"]
    file_list = []
    missing = []
    for item in req:
        present = files.get(item, False)
        file_list.append({"item": item, "required": True, "present": present})
        if not present:
            missing.append(item)
    done = sum(1 for f in file_list if f["present"])
    completeness = round(done / len(req), 2)
    if completeness == 1.0:
        status = "complete"
    elif completeness >= 0.5:
        status = "partial"
    else:
        status = "missing"
    return {
        "student": {"name": name, "name_pinyin": pinyin, "is_real_liyaxuan": real},
        "challenge": cid,
        "challenge_title": CHALLENGES[cid]["title"],
        "submitted_at": submitted_at,
        "files": file_list,
        "status": status,
        "completeness": completeness,
        "missing": missing,
        "is_demo_data": not real,
        "note": note,
    }

def build_demo_records():
    records = []
    base_date = datetime.date(2026, 9, 20)
    for i, (name, pinyin, subs) in enumerate(DEMO_CLASSMATES):
        for cid, files in subs.items():
            # spread submission dates over Sept-Oct
            d = base_date + datetime.timedelta(days=(i * 3 + len(cid)))
            ts = f"{d.isoformat()}T{10+i%8:02d}:00:00+08:00"
            records.append(make_record(name, pinyin, cid, ts, files, real=False,
                                       note="演示样例数据：虚构同学，仅用于仪表盘功能演示"))
    return records

# ============ 4. 主流程 ============
def main():
    real = scan_real_liyaxuan()
    demo = build_demo_records()
    all_records = real + demo

    data = {
        "meta": {
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "course": "Elite20 提交数据仪表盘",
            "data_source_note": (
                "本数据集包含两类记录：\n"
                "1) is_real_liyaxuan=true：李亚轩本人真实提交，扫描自桌面 "
                f"{DESKTOP_SUBMIT} 下的 C2A/C2G/C4 文件夹；\n"
                "2) is_demo_data=true：同班同学演示样例数据，人物姓名与提交情况均为虚构，"
                "仅用于演示仪表盘的筛选、高亮、统计功能，不代表任何真实同学的提交状态。"
            ),
            "challenges": CHALLENGES,
        },
        "records": all_records,
    }

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    json_path = os.path.join(ROOT, "data", "submissions.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON written: {json_path} ({len(all_records)} records, real={len(real)}, demo={len(demo)})")

    # 数据说明
    readme = """# 数据说明

本目录下 `submissions.json` 是 C6A 仪表盘的数据源。

## 数据来源（务必阅读）

数据集由两部分组成，**严禁混淆**：

### A. 李亚轩本人真实提交（is_real_liyaxuan = true）
- 来源：扫描本机桌面 `C:\\Users\\lenovo\\Desktop\\提交挑战\\` 下：
  - `C2A_MetaCal-Shift`
  - `C2G_ParameterGolf`
  - `C4_技能分享与传播`（含 C4A/C4B/C4C/C4D 四个子项）
- 真实性：文件路径、文件名、文件存在性均由 `build_dashboard.py` 脚本实际遍历磁盘得出。

### B. 同班同学演示样例数据（is_demo_data = true）
- **完全虚构**：姓名（王小明、李思颖、张子涵 等）与提交情况均为构造，
  不代表 Elite20 任何真实同学的提交状态。
- 用途：仅用于演示仪表盘的"按学生筛选 / 按挑战筛选 / 缺失高亮 / 统计图表"等交互功能。
- 每一条 demo 记录的 `note` 字段都标注了"演示样例数据：虚构同学"。

## Schema

每条 record 结构见 CHALLENGE.md 中"提交记录 Schema"：
student / challenge / submitted_at / files[] / status / completeness / missing / is_demo_data。
"""
    with open(os.path.join(ROOT, "data", "数据说明.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    print("数据说明.md written")

if __name__ == "__main__":
    main()
