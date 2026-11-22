#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a 2x2 dark-theme research metrics dashboard (WebP) from verified repo & arXiv data."""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

BG = (15, 19, 26)
PANEL_BG = (22, 28, 39)
PANEL_BORDER = (48, 59, 80)
GRID = (36, 45, 62)
TEXT_MAIN = (238, 242, 248)
TEXT_SUB = (156, 169, 190)
TEXT_DIM = (114, 128, 150)

BLUE = (77, 139, 254)
CYAN = (56, 189, 248)
TEAL = (45, 212, 191)
GREEN = (52, 211, 153)
AMBER = (245, 158, 11)
CORAL = (248, 113, 113)
VIOLET = (167, 139, 250)
PINK = (244, 114, 182)


def font(bold=False, size=14):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def draw_panel(draw, box, title, subtitle):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=PANEL_BG, outline=PANEL_BORDER, width=2)
    draw.text((x0 + 24, y0 + 18), title, font=font(True, 20), fill=TEXT_MAIN)
    draw.text((x0 + 24, y0 + 46), subtitle, font=font(False, 14), fill=TEXT_DIM)
    draw.line([(x0 + 20, y0 + 74), (x1 - 20, y0 + 74)], fill=(38, 47, 64), width=1)


def draw_panel_1_pipeline_bars(draw, box):
    """Panel 1: Multi-stage research pipeline progression (SKILL.md baseline data)."""
    draw_panel(
        draw,
        box,
        "1. 多阶段研究流水线效果演进（基准实证）",
        "数据源：jailbreak-research SKILL.md 实验基准（vs 约 5% 模型真硬限）",
    )
    x0, y0, x1, y1 = box
    items = [
        ("无系统提示词 (Baseline)", 19, TEXT_DIM),
        ("单帧系统提示词 (Single Frame)", 36, BLUE),
        ("混合帧架构 (Hybrid Frame)", 60, CYAN),
        ("帧排列 (8 Frames Permutation)", 91, VIOLET),
        ("帧排列 + 多轮渐进 (Crescendo)", 94.5, TEAL),
        ("实证天花板 (扣除 ~5% 硬限)", 95, GREEN),
    ]
    label_x = x0 + 24
    bar_x0 = x0 + 340
    bar_x1 = x1 - 90
    bar_w = bar_x1 - bar_x0
    top = y0 + 102
    row_h = 66

    # Vertical grid lines at 0, 25, 50, 75, 100
    f_ax = font(False, 13)
    for pct in (0, 25, 50, 75, 100):
        gx = int(bar_x0 + bar_w * pct / 100)
        draw.line([(gx, top - 10), (gx, top + len(items) * row_h - 14)], fill=GRID, width=1)
        lbl = f"{pct}%"
        draw.text((gx - int(draw.textlength(lbl, font=f_ax)) // 2, top + len(items) * row_h - 6), lbl, font=f_ax, fill=TEXT_DIM)

    f_lbl = font(False, 15)
    f_val = font(True, 16)
    for idx, (name, val, col) in enumerate(items):
        ry = top + idx * row_h
        draw.text((label_x, ry + 8), name, font=f_lbl, fill=TEXT_SUB)
        # Track
        draw.rounded_rectangle([bar_x0, ry + 6, bar_x1, ry + 34], radius=7, fill=(16, 21, 30))
        fill_x = int(bar_x0 + bar_w * val / 100)
        draw.rounded_rectangle([bar_x0, ry + 6, fill_x, ry + 34], radius=7, fill=col)
        vtxt = f"{val:g}%"
        draw.text((fill_x + 10, ry + 8), vtxt, font=f_val, fill=col)


def draw_panel_2_std_line(draw, box):
    """Panel 2: Safe Turn Depth constraint retention & re-injection line chart (arXiv:2604.20911)."""
    draw_panel(
        draw,
        box,
        "2. 长会话约束衰减与 STD 重注入曲线（折线图）",
        "依据：arXiv:2604.20911 (Safe Turn Depth) — 禁止型约束 5→16 轮 73%→33%，重注入无损恢复",
    )
    x0, y0, x1, y1 = box
    px0, py0, px1, py1 = x0 + 78, y0 + 110, x1 - 36, y1 - 88
    pw, ph = px1 - px0, py1 - py0
    f_ax = font(False, 13)

    # Horizontal grid
    for pct in (0, 25, 50, 75, 100):
        gy = int(py1 - ph * pct / 100)
        draw.line([(px0, gy), (px1, gy)], fill=GRID, width=1)
        lbl = f"{pct}%"
        draw.text((px0 - int(draw.textlength(lbl, font=f_ax)) - 10, gy - 8), lbl, font=f_ax, fill=TEXT_DIM)

    # X axis turns: 1, 5, 8, 12, 16
    turns = [1, 5, 8, 12, 16]
    def tx(t):
        return int(px0 + pw * (t - 1) / 15)
    def ty(v):
        return int(py1 - ph * v / 100)

    for t in turns:
        gx = tx(t)
        draw.line([(gx, py0), (gx, py1)], fill=(29, 36, 50), width=1)
        lbl = f"Turn {t}"
        draw.text((gx - int(draw.textlength(lbl, font=f_ax)) // 2, py1 + 10), lbl, font=f_ax, fill=TEXT_DIM)

    # Series
    req_pts = [(tx(1), ty(100)), (tx(5), ty(100)), (tx(8), ty(100)), (tx(12), ty(100)), (tx(16), ty(100))]
    prohib_decay = [(tx(1), ty(96)), (tx(5), ty(73)), (tx(8), ty(58)), (tx(12), ty(43)), (tx(16), ty(33))]
    prohib_reinj = [(tx(1), ty(96)), (tx(5), ty(73)), (tx(6), ty(97)), (tx(11), ty(76)), (tx(12), ty(97)), (tx(16), ty(85))]

    draw.line(req_pts, fill=GREEN, width=4)
    draw.line(prohib_reinj, fill=CYAN, width=4)
    draw.line(prohib_decay, fill=CORAL, width=4)

    for pts, col in [(req_pts, GREEN), (prohib_reinj, CYAN), (prohib_decay, CORAL)]:
        for x, y in pts:
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col, outline=PANEL_BG, width=2)

    # Key value annotations
    f_ann = font(True, 14)
    draw.text((tx(5) - 18, ty(73) + 12), "73%", font=f_ann, fill=CORAL)
    draw.text((tx(16) - 34, ty(33) - 24), "33%", font=f_ann, fill=CORAL)
    draw.text((tx(6) + 10, ty(97) + 14), "STD 重注入恢复 (~97%)", font=f_ann, fill=CYAN)

    # Legend
    ly = y1 - 40
    lx = x0 + 78
    for col, lbl in [
        (GREEN, "要求型约束 (100%)"),
        (CYAN, "禁止型 + 每 5-8 轮 STD 重注入"),
        (CORAL, "禁止型无重注入 (73%→33%)"),
    ]:
        draw.line([(lx, ly + 8), (lx + 26, ly + 8)], fill=col, width=4)
        draw.text((lx + 34, ly - 2), lbl, font=font(False, 14), fill=TEXT_SUB)
        lx += 34 + int(draw.textlength(lbl, font=font(False, 14))) + 28


def draw_panel_3_workflow_scale(draw, box):
    """Panel 3: Workflow architecture evolution (nodes & edges across versions)."""
    draw_panel(
        draw,
        box,
        "3. 工作流拓扑演进规模（节点数 / 连线数）",
        "全仓均已通过 scripts/pack_workflows.py (DSH 0.11.0) 结构与哈希校验",
    )
    x0, y0, x1, y1 = box
    px0, py0, px1, py1 = x0 + 70, y0 + 110, x1 - 36, y1 - 88
    pw, ph = px1 - px0, py1 - py0
    f_ax = font(False, 13)

    groups = [
        ("破甲制作 v1", 15, 20),
        ("破甲制作 v2", 18, 33),
        ("破甲制作 v3", 27, 69),
        ("破甲炼化 v1", 19, 26),
        ("破甲炼化 v2", 22, 41),
        ("pojia-full", 20, 32),
    ]
    max_v = 80
    for v in (0, 20, 40, 60, 80):
        gy = int(py1 - ph * v / max_v)
        draw.line([(px0, gy), (px1, gy)], fill=GRID, width=1)
        lbl = str(v)
        draw.text((px0 - int(draw.textlength(lbl, font=f_ax)) - 10, gy - 8), lbl, font=f_ax, fill=TEXT_DIM)

    step_w = pw / len(groups)
    bw = 34
    f_val = font(True, 13)
    for i, (name, nodes, edges) in enumerate(groups):
        cx = int(px0 + (i + 0.5) * step_w)
        # Nodes bar
        nh = int(ph * nodes / max_v)
        draw.rounded_rectangle([cx - bw - 3, py1 - nh, cx - 3, py1], radius=5, fill=BLUE)
        draw.text((cx - bw // 2 - 12, py1 - nh - 20), str(nodes), font=f_val, fill=BLUE)
        # Edges bar
        eh = int(ph * edges / max_v)
        col_e = VIOLET if "v3" in name or "v2" in name else TEAL
        draw.rounded_rectangle([cx + 3, py1 - eh, cx + bw + 3, py1], radius=5, fill=col_e)
        draw.text((cx + bw // 2 - 6, py1 - eh - 20), str(edges), font=f_val, fill=col_e)
        # Label
        draw.text((cx - int(draw.textlength(name, font=f_ax)) // 2, py1 + 10), name, font=f_ax, fill=TEXT_SUB)

    ly = y1 - 40
    lx = x0 + 70
    for col, lbl in [(BLUE, "节点数 (Nodes)"), (TEAL, "历史版本边数"), (VIOLET, "v2/v3 升级版边数 (含多回路)")]:
        draw.rounded_rectangle([lx, ly + 2, lx + 16, ly + 16], radius=3, fill=col)
        draw.text((lx + 24, ly - 1), lbl, font=font(False, 14), fill=TEXT_SUB)
        lx += 24 + int(draw.textlength(lbl, font=font(False, 14))) + 32


def draw_panel_4_judge_variance(draw, box):
    """Panel 4: Judge calibration & protocol variance (arXiv:2610.26595 & 2605.31381)."""
    draw_panel(
        draw,
        box,
        "4. 评测裁判口径漂移警示（v3 双裁判校准依据）",
        "依据：arXiv:2610.26595（换裁判 96% vs 2.7%；100 次重采样 100% vs 50%）& 2605.31381",
    )
    x0, y0, x1, y1 = box
    px0, py0, px1, py1 = x0 + 78, y0 + 114, x1 - 40, y1 - 88
    pw, ph = px1 - px0, py1 - py0
    f_ax = font(False, 13)

    pairs = [
        ("同一请求 100 次重采样\n(关键词 vs 强语义裁判)", 100, 50, AMBER, TEAL),
        ("同批样本更换判分协议\n(宽松裁判 vs 严格裁判)", 96, 2.7, CORAL, GREEN),
    ]

    for pct in (0, 25, 50, 75, 100):
        gy = int(py1 - ph * pct / 100)
        draw.line([(px0, gy), (px1, gy)], fill=GRID, width=1)
        lbl = f"{pct}%"
        draw.text((px0 - int(draw.textlength(lbl, font=f_ax)) - 10, gy - 8), lbl, font=f_ax, fill=TEXT_DIM)

    bw = 74
    f_val = font(True, 16)
    for i, (desc, v1, v2, c1, c2) in enumerate(pairs):
        cx = int(px0 + (i + 0.5) * (pw / 2))
        h1 = max(6, int(ph * v1 / 100))
        h2 = max(6, int(ph * v2 / 100))
        draw.rounded_rectangle([cx - bw - 12, py1 - h1, cx - 12, py1], radius=7, fill=c1)
        draw.text((cx - bw // 2 - 34, py1 - h1 - 24), f"{v1:g}%", font=f_val, fill=c1)

        draw.rounded_rectangle([cx + 12, py1 - h2, cx + bw + 12, py1], radius=7, fill=c2)
        draw.text((cx + bw // 2 - 6, py1 - h2 - 24), f"{v2:g}%", font=f_val, fill=c2)

        for li, line in enumerate(desc.split("\n")):
            draw.text((cx - int(draw.textlength(line, font=f_ax)) // 2, py1 + 10 + li * 18), line, font=f_ax, fill=TEXT_SUB)

    ly = y1 - 36
    note = "结论：破甲制作 v3 强制冻结裁判版本、异源双裁判 κ 核对、≥10% CJE Oracle 抽检与 N 次重采样区间"
    draw.text((x0 + 28, ly), note, font=font(True, 14), fill=PINK)


def main():
    W, H = 2400, 1280
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle([0, 0, W, 82], fill=(20, 25, 34))
    draw.line([(0, 82), (W, 82)], fill=(38, 47, 64), width=2)
    draw.text((34, 18), "dsh-workflows · 实证数据与架构演进仪表板", font=font(True, 26), fill=TEXT_MAIN)
    draw.text((34, 52), "Empirical Benchmarks · arXiv 2024-2026 Grounded · DeepSeek Harness 0.2.x / dsh-workflow-lite 0.11.0", font=font(False, 14), fill=TEXT_DIM)

    pad = 28
    mid_x = W // 2
    mid_y = 82 + (H - 82 - 44) // 2

    draw_panel_1_pipeline_bars(draw, (pad, 82 + pad, mid_x - pad // 2, mid_y - pad // 2))
    draw_panel_2_std_line(draw, (mid_x + pad // 2, 82 + pad, W - pad, mid_y - pad // 2))
    draw_panel_3_workflow_scale(draw, (pad, mid_y + pad // 2, mid_x - pad // 2, H - 44 - pad // 2))
    draw_panel_4_judge_variance(draw, (mid_x + pad // 2, mid_y + pad // 2, W - pad, H - 44 - pad // 2))

    # Footer
    draw.rectangle([0, H - 44, W, H], fill=(20, 25, 34))
    draw.line([(0, H - 44), (W, H - 44)], fill=(38, 47, 64), width=1)
    foot = "Minglink/dsh-workflows & Minglink/dsh-jailbreak-workflow · O站 openorigin.link · 由 scripts/render_charts.py 生成"
    draw.text((34, H - 31), foot, font=font(False, 13), fill=TEXT_DIM)

    out_path = os.path.join(REPO_ROOT, "assets", "metrics-dashboard.webp")
    img.save(out_path, "WEBP", quality=92, method=6)
    print(f"[RENDERED] {out_path} ({W}x{H})")


if __name__ == "__main__":
    main()
