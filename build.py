#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课件相册生成器 —— 超简单版
把图片放进 slides/ 目录，按数字编号命名（01.jpg, 02.jpg...）
运行本脚本 → 生成 index.html → 所有人打开链接就能看
"""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.join(BASE, "slides")
OUTPUT = os.path.join(BASE, "index.html")

IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".heic", ".avif", ".svg"}

def get_slides():
    if not os.path.isdir(SLIDES_DIR):
        return []
    files = [f for f in os.listdir(SLIDES_DIR)
             if os.path.splitext(f)[1].lower() in IMG_EXT]
    def key(name):
        nums = re.findall(r"\d+", name)
        return int(nums[0]) if nums else 999
    files.sort(key=key)
    return files

slides = get_slides()

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>课件</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1a1d23;color:#e8eaed;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.h{padding:12px 16px;border-bottom:1px solid #282c34;display:flex;justify-content:space-between;align-items:center}
.h span{font-size:15px;font-weight:600}
.h small{color:#6b7280;font-size:12px}
.empty{padding:60px 20px;text-align:center;color:#6b7280;line-height:2;font-size:14px}
.view{padding:12px;text-align:center}
.view img{max-width:95vw;max-height:82vh;border-radius:4px}
.bar{padding:10px;display:flex;justify-content:center;align-items:center;gap:10px}
.bar button{padding:7px 16px;border:none;border-radius:6px;font-size:13px;cursor:pointer}
.b1{background:#282c34;color:#e8eaed}.b2{background:#3b82f6;color:#fff}
.b1:hover{background:#3a3f4a}.b2:hover{background:#2563eb}
.ct{color:#6b7280;font-size:12px;min-width:60px}
.grid{padding:12px;display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}
.g-item{position:relative;border-radius:6px;overflow:hidden;cursor:pointer;aspect-ratio:4/3;background:#232730}
.g-item img{width:100%;height:100%;object-fit:cover}
.g-item .n{position:absolute;top:4px;left:4px;background:rgba(0,0,0,.5);color:#fff;font-size:10px;padding:1px 5px;border-radius:8px}
</style>
</head>
<body>
<div class="h"><span>📖 课件</span><small id="info"></small></div>
'''

if not slides:
    html += '''<div class="empty">还没有课件图片 📭<br>把图片放进 slides/ 目录，按数字编号命名<br>01.jpg → 第1页 · 02.jpg → 第2页 · ...<br>然后运行 build.py 重新生成</div>'''
else:
    html += f'''<div class="grid" id="grid">{"".join([f'<div class="g-item" onclick="v({i})"><span class="n">{i+1}</span><img src="slides/{s}" loading="lazy"></div>' for i,s in enumerate(slides)])}</div>'''
    html += '''<div class="view" id="big" style="display:none"><img id="im"></div>'''
    html += '''<div class="bar" id="bar" style="display:none"><button class="b1" onclick="g(-1)">← 上页</button><span class="ct" id="ct"></span><button class="b2" onclick="g(1)">下页 →</button><button class="b1" onclick="grid()">目录</button></div>'''
    html += f'''<script>var L={json.dumps(slides)},c=0;document.getElementById("info").textContent=L.length+"页";function v(i){{c=i;sh();document.getElementById("grid").style.display="none";document.getElementById("big").style.display="";document.getElementById("bar").style.display=""}}function g(d){{c=(c+d+L.length)%L.length;sh()}}function sh(){{document.getElementById("im").src="slides/"+L[c];document.getElementById("ct").textContent=(c+1)+"/"+L.length}}function grid(){{document.getElementById("grid").style.display="";document.getElementById("big").style.display="none";document.getElementById("bar").style.display="none"}}document.onkeydown=function(e){{if(document.getElementById("big").style.display==="none")return;if(e.key==="Escape")grid();if(e.key==="ArrowLeft")g(-1);if(e.key==="ArrowRight")g(1)}};</script>'''

html += '''</body></html>'''

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 生成完成！共 {len(slides)} 张课件")
if slides:
    for i, s in enumerate(slides):
        print(f"   {i+1}. {s}")
