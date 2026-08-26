"""
AI Work Agent DAU 动态排名竞赛动画
30秒 MP4, 1280×720, 25fps
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# ─── CONFIG ────────────────────────────────────────────────────────────────────
VIDEO_DIR  = "/Users/ianonymous/.openclaw/workspace/agent_dau_video"
DATA_FILE  = os.path.join(VIDEO_DIR, "dau_data.csv")
OUT_FILE   = os.path.join(VIDEO_DIR, "agent_dau_race.mp4")

W, H        = 1280, 720
FPS         = 25
DPI         = 120
N_AGENTS    = 12
FPS_TOTAL   = 30 * FPS
INTRO_END   = 3 * FPS
OUTRO_START = FPS_TOTAL - 5 * FPS

BG_COLOR    = "#0A0E27"

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
df      = pd.read_csv(DATA_FILE)
dates   = sorted(df["date"].unique())
agents  = list(df["agent"].unique())

CATEGORY_COLORS = {
    "通用助手":  "#74B9FF",
    "编程助手":  "#0984E3",
    "搜索/研究": "#FDCB6E",
    "效率工具":  "#A29BFE",
    "多模态":    "#FD79A8",
}

BAR_COLORS = {
    "ChatGPT":          "#10A37F",
    "Claude":           "#CC785C",
    "Copilot":          "#0078D4",
    "Gemini":           "#4285F4",
    "Cursor":           "#7B61FF",
    "Perplexity":       "#D4AF37",
    "文心一言":         "#E74C3C",
    "通义千问":         "#FF6B35",
    "Kimi":             "#00C4B4",
    "Notion AI":        "#AAAAAA",
    "Midjourney":       "#9B59B6",
    "Stable Diffusion":  "#8E44AD",
}

MILESTONES = {
    "2024-04": ("ChatGPT 破亿",   "#FDCB6E"),
    "2024-07": ("Kimi 爆发增长",  "#00C4B4"),
    "2024-10": ("Claude 强势追击", "#CC785C"),
    "2024-01": ("2024 新起点",   "#74B9FF"),
}

# Pre-build lookup: date → {agent: dau}
lookup = {}
for d in dates:
    sub = df[df["date"] == d].set_index("agent")
    lookup[d] = sub["dau"].to_dict()

def format_dau(v):
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000:     return f"{v/1_000:.0f}K"
    return str(int(v))

def frame_to_month_float(f):
    if f < INTRO_END:
        return 0.0
    anim_t   = f - INTRO_END
    max_anim = FPS_TOTAL - INTRO_END
    return min(anim_t / max_anim * (len(dates) - 1), len(dates) - 1)

# ─── FIGURE ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
fig.patch.set_facecolor(BG_COLOR)

ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_facecolor(BG_COLOR)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")

# Pre-load font with Chinese support
import matplotlib.font_manager as fm
font_prop = fm.FontProperties(family="PingFang TC")

def draw_frame(f):
    ax.clear()
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    t = f / FPS

    # ── INTRO (0–3s) ────────────────────────────────────────────────────────
    if f < INTRO_END:
        alpha = f / max(1, INTRO_END)
        ax.text(0.5, 0.65, "AI Work Agent",
                ha="center", va="center", fontsize=38,
                color="white", fontweight="bold", alpha=alpha,
                fontproperties=font_prop)
        ax.text(0.5, 0.51, "DAU 实时排名竞赛",
                ha="center", va="center", fontsize=24,
                color="#74B9FF", fontweight="bold", alpha=alpha,
                fontproperties=font_prop)
        ax.text(0.5, 0.38, "2023 – 2024 · 全球战场",
                ha="center", va="center", fontsize=13,
                color="#888", alpha=alpha, fontproperties=font_prop)
        bar_w = alpha * 0.4
        ax.add_patch(plt.Rectangle((0.3 - bar_w/2, 0.21), 0.4, 0.015,
                                    color="#1a1f4e", alpha=alpha))
        ax.add_patch(plt.Rectangle((0.3 - bar_w/2, 0.21), bar_w, 0.015,
                                    color="#74B9FF", alpha=alpha))
        ax.text(0.5, 0.14, "Loading ...",
                ha="center", va="center", fontsize=10,
                color="#444", alpha=alpha)
        return

    # ── OUTRO (last 5s) ────────────────────────────────────────────────────
    if f >= OUTRO_START:
        alpha = (f - OUTRO_START) / (FPS_TOTAL - OUTRO_START)
        ax.add_patch(plt.Rectangle((0,0), 1, 1, color=BG_COLOR, alpha=0.82 * alpha))
        cur = sorted(lookup[dates[-1]].items(), key=lambda x: x[1], reverse=True)[:N_AGENTS]
        top1, v1 = cur[0]
        top2, v2 = cur[1]
        ax.text(0.5, 0.76, "FINAL RANKING",
                ha="center", va="center", fontsize=26,
                color="white", fontweight="bold", alpha=alpha)
        ax.text(0.5, 0.61, f"#1  {top1}",
                ha="center", va="center", fontsize=18,
                color="#FDCB6E", fontweight="bold", alpha=alpha,
                fontproperties=font_prop)
        ax.text(0.5, 0.52, format_dau(v1),
                ha="center", va="center", fontsize=13,
                color="#888", alpha=alpha)
        ax.text(0.5, 0.42, f"#2  {top2}  {format_dau(v2)}",
                ha="center", va="center", fontsize=13,
                color="#aaa", alpha=alpha, fontproperties=font_prop)
        total = sum(v for _, v in lookup[dates[-1]].items())
        ax.text(0.5, 0.32, f"24 Months · Total DAU {format_dau(total)}+",
                ha="center", va="center", fontsize=11,
                color="#74B9FF", alpha=alpha)
        ax.text(0.5, 0.18, "Powered by Data · Witnessed by AI",
                ha="center", va="center", fontsize=9,
                color="#333", alpha=alpha)
        return

    # ── MAIN RACE ─────────────────────────────────────────────────────────────
    month_f  = frame_to_month_float(f)
    mi       = int(month_f)
    frac     = month_f - mi
    mi       = min(mi, len(dates) - 1)
    ni       = min(mi + 1, len(dates) - 1)

    d0 = dates[mi]
    d1 = dates[ni]
    date_lbl = d0

    # Interpolate between two months as plain dicts
    cur_dict = lookup[d0]
    nxt_dict = lookup[d1]
    interp = {}
    for agent in cur_dict:
        cur_v = cur_dict[agent]
        nxt_v = nxt_dict.get(agent, cur_v)
        interp[agent] = cur_v * (1 - frac) + nxt_v * frac

    sorted_agents = sorted(interp.items(), key=lambda x: x[1], reverse=True)[:N_AGENTS]
    MAX_DAU       = sorted_agents[0][1]

    # ── Layout constants ────────────────────────────────────────────────────
    BAR_AREA_X0  = 0.13
    BAR_AREA_W   = 0.78
    BAR_H        = 0.050
    BAR_GAP      = 0.006
    TOP_Y        = 0.91

    # Top header band
    ax.add_patch(plt.Rectangle((0, 0.93), 1, 0.07, color="#0d1028", alpha=0.95))
    ax.text(0.14, 0.967, "AI Work Agent  DAU Live Ranking",
            ha="left", va="center", fontsize=9.5, color="#555")
    ax.text(0.90, 0.967, date_lbl,
            ha="right", va="center", fontsize=13, color="#74B9FF", fontweight="bold",
            fontproperties=font_prop)

    # Category legend (top-right, compact)
    cats = list(CATEGORY_COLORS.items())
    for ci, (cat, cc) in enumerate(cats[:4]):  # show max 4 to save space
        ax.text(0.91 + ci * 0.0, 0.945 - ci * 0.016,
                "●", ha="right", va="center", fontsize=7, color=cc, alpha=0.8)
        ax.text(0.915, 0.945 - ci * 0.016,
                cat, ha="left", va="center", fontsize=6, color="#666", alpha=0.8,
                fontproperties=font_prop)

    ax.plot([0.12, 0.92], [0.925, 0.925], color="#1c2150", lw=0.5)

    # ── Bars ─────────────────────────────────────────────────────────────────
    for rank, (agent, dau) in enumerate(sorted_agents):
        y      = TOP_Y - rank * (BAR_H + BAR_GAP)
        bar_w  = (dau / MAX_DAU) * BAR_AREA_W
        color  = BAR_COLORS.get(agent, "#74B9FF")

        # Glow (3 layers)
        for gw, ga in [(0.022, 0.12), (0.012, 0.25), (0.005, 0.65)]:
            ax.add_patch(plt.Rectangle(
                (BAR_AREA_X0, y - BAR_H/2 - gw/2),
                bar_w, BAR_H + gw,
                color=color, alpha=ga, zorder=1))

        # Main bar
        ax.add_patch(plt.Rectangle(
            (BAR_AREA_X0, y - BAR_H/2),
            bar_w, BAR_H,
            color=color, alpha=0.97, zorder=2))

        # Rank
        ax.text(BAR_AREA_X0 - 0.004, y, f"#{rank+1}",
                ha="right", va="center", fontsize=8.5, color="#333",
                fontfamily="monospace")

        # Name
        ax.text(BAR_AREA_X0 + 0.005, y, agent,
                ha="left", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=3,
                fontproperties=font_prop)

        # DAU value
        ax.text(BAR_AREA_X0 + bar_w + 0.005, y,
                format_dau(dau),
                ha="left", va="center", fontsize=9.5,
                color=color, fontweight="bold", zorder=3,
                fontproperties=font_prop)

    # ── Milestone callout ───────────────────────────────────────────────────
    if date_lbl in MILESTONES:
        label, lcolor = MILESTONES[date_lbl]
        y_row  = TOP_Y - 3 * (BAR_H + BAR_GAP)
        bx     = BAR_AREA_X0 + 0.02
        ax.annotate(
            label,
            xy=(bx, y_row - BAR_H/2),
            xytext=(bx, y_row - BAR_H/2 + 0.065),
            fontsize=9, color=lcolor, fontweight="bold",
            ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=lcolor, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#0d1028",
                      edgecolor=lcolor, alpha=0.85, lw=0.7),
            fontproperties=font_prop)

    # Bottom footer
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.058, color="#0d1028", alpha=0.95))
    ax.text(0.5, 0.022,
            "Data: Simulated 2023-01~2024-11 · 24-month rolling simulation",
            ha="center", va="center", fontsize=7.5, color="#2a2a4a")
    total_dau = sum(interp.values())
    ax.text(0.90, 0.022,
            f"Total DAU {format_dau(total_dau)}/day",
            ha="right", va="center", fontsize=8, color="#74B9FF")

# ─── RENDER ────────────────────────────────────────────────────────────────────
from matplotlib.animation import FuncAnimation, FFMpegWriter

print(f"开始渲染 {FPS_TOTAL} 帧 ({FPS_TOTAL/FPS:.0f}s) ...")
anim  = FuncAnimation(fig, draw_frame, frames=FPS_TOTAL,
                       interval=1000/FPS, blit=False)
writer = FFMpegWriter(fps=FPS, bitrate=4000)
anim.save(OUT_FILE, writer=writer, dpi=DPI)
plt.close()

size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
print(f"\n✅ 视频已生成: {OUT_FILE}")
print(f"   大小: {size_mb:.1f} MB | 时长: {FPS_TOTAL/FPS:.0f}s | 分辨率: {W}×{H}")
