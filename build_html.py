# -*- coding: utf-8 -*-
"""读取 submissions.json，生成 dashboard/index.html（数据内嵌，ECharts CDN）。"""
import os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "data", "submissions.json"), encoding="utf-8") as f:
    data = json.load(f)
data_js = json.dumps(data, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Elite20 提交数据仪表盘</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<style>
:root{--teal:#0f6e6e;--teal2:#14a0a0;--bg:#f4fafb;--card:#fff;--line:#d8eaea;--ink:#123;--muted:#5b7a7a;--bad:#b3261e;--warn:#b4550e;--good:#0f7b4d}
*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink)}
header{background:linear-gradient(135deg,#0f3d3e,var(--teal));color:#fff;padding:18px 20px}
.wrap{max-width:1200px;margin:0 auto;padding:0 16px}
h1{margin:0;font-size:22px}h2{font-size:15px;color:var(--teal);margin:0 0 10px}
.banner{background:#fff8e1;border-left:4px solid var(--warn);padding:10px 14px;border-radius:6px;font-size:13px;margin:14px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
@media(max-width:800px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;box-shadow:0 2px 10px rgba(15,110,110,.06)}
.chart{height:320px}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:12px 0}
select,button{padding:8px 12px;border-radius:8px;border:1.5px solid var(--line);font-size:13px;background:#fff}
button{background:var(--teal);color:#fff;border:0;cursor:pointer}button:hover{background:#0d5a5a}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:center}th{background:var(--teal);color:#fff;position:sticky;top:0}
tr:hover td{background:#eefafa}
.st-complete{color:var(--good);font-weight:600}.st-partial{color:var(--warn);font-weight:600}.st-missing{color:var(--bad);font-weight:600}
.badge{display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;margin-left:4px}
.badge-real{background:#dcf5e8;color:var(--good)}.badge-demo{background:#fff1e0;color:var(--warn)}
.miss-cell{background:#fde2e0!important;color:var(--bad);font-weight:600}
.stats{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}
.stat{flex:1;min-width:130px;background:var(--teal);color:#fff;border-radius:10px;padding:12px;text-align:center}
.stat .n{font-size:24px;font-weight:700}.stat .t{font-size:12px;opacity:.9}
</style>
</head>
<body>
<header><div class="wrap"><h1>Elite20 提交数据仪表盘</h1>
<p style="margin:6px 0 0;opacity:.9;font-size:13px">双击此文件即可在浏览器打开 · 数据已内嵌 · 李亚轩本人真实提交 + 同班同学演示样例（已明确标注）</p></div></header>
<main class="wrap">
<div class="banner"><b>数据来源声明：</b>
<span id="dataNote"></span></div>

<div class="stats">
  <div class="stat"><div class="n" id="stStudents">0</div><div class="t">学生数</div></div>
  <div class="stat"><div class="n" id="stRecords">0</div><div class="t">提交记录数</div></div>
  <div class="stat"><div class="n" id="stReal">0</div><div class="t">本人真实记录</div></div>
  <div class="stat"><div class="n" id="stDemo">0</div><div class="t">演示样例记录</div></div>
  <div class="stat"><div class="n" id="stRate">0%</div><div class="t">完整提交率</div></div>
</div>

<div class="grid">
  <div class="card"><h2>① 全班完成率总览（按挑战）</h2><div id="chart1" class="chart"></div></div>
  <div class="card"><h2>② 提交状态分布</h2><div id="chart2" class="chart"></div></div>
</div>

<div class="card">
  <h2>③ 明细筛选</h2>
  <div class="filters">
    <label>学生 <select id="fStudent"><option value="">全部</option></select></label>
    <label>挑战 <select id="fChallenge"><option value="">全部</option></select></label>
    <label>状态 <select id="fStatus"><option value="">全部</option><option value="complete">完整</option><option value="partial">部分</option><option value="missing">缺失</option></select></label>
    <button onclick="exportCSV()">导出 CSV</button>
    <button onclick="resetFilter()" style="background:#fff;color:var(--teal);border:1.5px solid var(--teal)">重置</button>
  </div>
  <div style="overflow-x:auto;max-height:420px;overflow-y:auto">
  <table id="tbl"><thead><tr>
    <th>学生</th><th>类型</th><th>挑战</th><th>提交日期</th><th>状态</th><th>完成度</th><th>缺失项</th>
  </tr></thead><tbody></tbody></table>
  </div>
</div>
</main>
<script>
const DATA = __DATA__;
document.getElementById('dataNote').textContent = DATA.meta.data_source_note;

const records = DATA.records;
const challenges = Object.keys(DATA.meta.challenges);
const students = [...new Set(records.map(r=>r.student.name))].sort((a,b)=> a==='李亚轩'?-1: b==='李亚轩'?1: a.localeCompare(b,'zh'));

// stats
document.getElementById('stStudents').textContent = students.length;
document.getElementById('stRecords').textContent = records.length;
document.getElementById('stReal').textContent = records.filter(r=>r.student.is_real_liyaxuan).length;
document.getElementById('stDemo').textContent = records.filter(r=>r.is_demo_data).length;
document.getElementById('stRate').textContent = Math.round(records.filter(r=>r.status==='complete').length/records.length*100)+'%';

// filters
const fs=document.getElementById('fStudent'), fc=document.getElementById('fChallenge'), fst=document.getElementById('fStatus');
students.forEach(s=>{const o=document.createElement('option');o.value=s;o.textContent=s;fs.appendChild(o)});
challenges.forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;fc.appendChild(o)});
[fs,fc,fst].forEach(e=>e.onchange=render);

// charts
const c1=echarts.init(document.getElementById('chart1'));
const c2=echarts.init(document.getElementById('chart2'));
function renderCharts(){
  const compByCh = challenges.map(cid=>{
    const sub=records.filter(r=>r.challenge===cid);
    return Math.round(sub.filter(r=>r.status==='complete').length/Math.max(1,students.length)*100);
  });
  c1.setOption({tooltip:{trigger:'axis'},xAxis:{type:'category',data:challenges,axisLabel:{fontSize:11}},
    yAxis:{type:'value',max:100,axisLabel:{formatter:'{value}%'}},
    series:[{type:'bar',data:compByCh,itemStyle:{color:'#14a0a0'},label:{show:true,formatter:'{c}%'}}]});
  const cnt={complete:0,partial:0,missing:0};
  records.forEach(r=>cnt[r.status]++);
  c2.setOption({tooltip:{trigger:'item'},legend:{bottom:0},
    series:[{type:'pie',radius:['40%','70%'],data:[
      {value:cnt.complete,name:'完整',itemStyle:{color:'#0f7b4d'}},
      {value:cnt.partial,name:'部分',itemStyle:{color:'#b4550e'}},
      {value:cnt.missing,name:'缺失',itemStyle:{color:'#b3261e'}}
    ]}]});
}

function render(){
  const sv=fs.value, cv=fc.value, stv=fst.value;
  const rows=records.filter(r=>(!sv||r.student.name===sv)&&(!cv||r.challenge===cv)&&(!stv||r.status===stv));
  const tb=document.querySelector('#tbl tbody'); tb.innerHTML='';
  rows.forEach(r=>{
    const tr=document.createElement('tr');
    const badge=r.student.is_real_liyaxuan?'<span class="badge badge-real">本人真实</span>':'<span class="badge badge-demo">演示样例</span>';
    const miss=r.missing.length? r.missing.join('、'):'—';
    tr.innerHTML=`<td>${r.student.name} ${badge}</td><td>${r.student.is_real_liyaxuan?'真实':'演示'}</td>
      <td>${r.challenge}</td><td>${r.submitted_at.slice(0,10)}</td>
      <td class="st-${r.status}">${r.status==='complete'?'完整':r.status==='partial'?'部分':'缺失'}</td>
      <td>${Math.round(r.completeness*100)}%</td>
      <td class="${r.missing.length?'miss-cell':''}">${miss}</td>`;
    tb.appendChild(tr);
  });
}
function resetFilter(){fs.value='';fc.value='';fst.value='';render();}
function exportCSV(){
  const rows=[['学生','类型','挑战','提交日期','状态','完成度','缺失项']];
  records.forEach(r=>rows.push([r.student.name,r.student.is_real_liyaxuan?'真实':'演示',r.challenge,r.submitted_at.slice(0,10),r.status,r.completeness,r.missing.join('、')]));
  const csv='\\uFEFF'+rows.map(r=>r.join(',')).join('\\n');
  const blob=new Blob([csv],{type:'text/csv'}); const a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download='dashboard_export.csv'; a.click();
}
renderCharts(); render();
window.addEventListener('resize',()=>{c1.resize();c2.resize();});
</script>
</body>
</html>
"""
html = html.replace("__DATA__", data_js)
os.makedirs(os.path.join(ROOT, "dashboard"), exist_ok=True)
out = os.path.join(ROOT, "dashboard", "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("Dashboard HTML:", out, "size=", len(html))
