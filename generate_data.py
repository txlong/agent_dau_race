"""
生成 AI Work Agent DAU 示例数据
12 个 agent × 24 个月 (2023-01 ~ 2024-12)
"""

import csv
from datetime import datetime, timedelta

AGENTS = [
    {"name": "ChatGPT",    "color": "#10A37F", "category": "通用助手",  "base": 1_000_000, "growth": 0.12, "volatility": 0.05},
    {"name": "Claude",     "color": "#CC785C", "category": "通用助手",  "base": 200_000,   "growth": 0.18, "volatility": 0.06},
    {"name": "Copilot",    "color": "#0078D4", "category": "编程助手",  "base": 500_000,   "growth": 0.10, "volatility": 0.04},
    {"name": "Gemini",     "color": "#4285F4", "category": "通用助手",  "base": 100_000,   "growth": 0.25, "volatility": 0.10},
    {"name": "Cursor",     "color": "#7B61FF", "category": "编程助手",  "base": 30_000,    "growth": 0.35, "volatility": 0.15},
    {"name": "Perplexity", "color": "#D4AF37", "category": "搜索/研究", "base": 80_000,    "growth": 0.30, "volatility": 0.12},
    {"name": "文心一言",   "color": "#E74C3C", "category": "通用助手",  "base": 300_000,   "growth": 0.08, "volatility": 0.05},
    {"name": "通义千问",   "color": "#FF6B35", "category": "通用助手",  "base": 150_000,   "growth": 0.15, "volatility": 0.07},
    {"name": "Kimi",       "color": "#00C4B4", "category": "通用助手",  "base": 20_000,    "growth": 0.45, "volatility": 0.20},
    {"name": "Notion AI",  "color": "#1A1A1A", "category": "效率工具", "base": 400_000,   "growth": 0.07, "volatility": 0.03},
    {"name": "Midjourney", "color": "#9B59B6", "category": "多模态",   "base": 600_000,   "growth": 0.05, "volatility": 0.08},
    {"name": "Stable Diffusion","color": "#8E44AD","category":"多模态", "base": 350_000,  "growth": 0.06, "volatility": 0.06},
]

# 关键事件:在特定月份给特定 agent 施加增长冲击
EVENTS = {
    # (agent_name, month_offset): multiplier
    ("Kimi", 8):   3.5,   # Kimi 爆发
    ("Cursor", 10): 4.0,   # Cursor 逆袭
    ("Claude", 14): 2.0,   # Claude 2 发布
    ("Gemini", 16): 2.5,   # Gemini Pro
    ("Perplexity", 12): 3.0,
    ("ChatGPT", 20): 1.8,  # GPT-4o
}

import random
random.seed(42)

rows = []
start = datetime(2023, 1, 1)
cumulative_mult = {}  # 记录每个 agent 的累积增长冲击

for m in range(24):
    date = start + timedelta(days=30 * m)
    for agent in AGENTS:
        name = agent["name"]
        if name not in cumulative_mult:
            cumulative_mult[name] = 1.0

        # 基础增长
        mult = cumulative_mult[name]
        base = agent["base"] * (1 + agent["growth"]) ** m

        # 事件冲击
        if (name, m) in EVENTS:
            mult *= EVENTS[(name, m)]
            cumulative_mult[name] = mult

        # 波动
        noise = 1 + random.uniform(-agent["volatility"], agent["volatility"])
        dau = int(base * mult * noise)
        dau = max(dau, 5000)  # 保底

        rows.append({
            "date": date.strftime("%Y-%m"),
            "agent": name,
            "dau": dau,
            "category": agent["category"],
            "color": agent["color"],
        })

with open("/Users/ianonymous/.openclaw/workspace/agent_dau_video/dau_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date","agent","dau","category","color"])
    writer.writeheader()
    writer.writerows(rows)

print("✅ 数据已生成: dau_data.csv")
print(f"   共 {len(rows)} 行, {len(AGENTS)} 个 agent, 24 个月")

# 打印每月总量预览
import collections
monthly_totals = collections.defaultdict(int)
for r in rows:
    monthly_totals[r["date"]] += r["dau"]

for k, v in sorted(monthly_totals.items()):
    print(f"  {k}: 全行业 DAU ≈ {v/1e6:.2f}M")
