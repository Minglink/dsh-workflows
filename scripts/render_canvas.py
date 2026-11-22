#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render DSH-style dark-theme workflow canvas previews from versions/*.json."""

import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

PALETTE = {
    "blue": (77, 139, 254),
    "green": (52, 211, 153),
    "amber": (245, 158, 11),
    "coral": (248, 113, 113),
    "teal": (45, 212, 191),
    "pink": (244, 114, 182),
    "olive": (163, 230, 53),
    "violet": (167, 139, 250),
    "slate": (148, 163, 184),
}

BG = (15, 19, 26)
DOT = (34, 42, 56)
TOPBAR = (20, 25, 34)
CARD_BG = (24, 30, 41)
CARD_BORDER = (51, 62, 82)
RES_BG = (19, 24, 34)
RES_BORDER = (56, 68, 90)
INPUT_BG = (22, 30, 44)
INPUT_ACCENT = (56, 189, 248)
TEXT_MAIN = (238, 242, 248)
TEXT_SUB = (156, 169, 190)
TEXT_DIM = (114, 128, 150)
EDGE_MAIN = (148, 163, 184)
EDGE_DATA = (71, 88, 115)
EDGE_COND = (250, 204, 21)
EDGE_LOOP = (244, 114, 182)


def load_font(bold=False, size=14):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap_text(draw, text, font, max_w, max_lines=2):
    lines = []
    cur = ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            if len(lines) >= max_lines:
                break
            continue
        test = cur + ch
        if draw.textlength(test, font=font) > max_w:
            lines.append(cur)
            cur = ch
            if len(lines) >= max_lines:
                break
        else:
            cur = test
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and len("".join(lines)) < len(text.replace("\n", "")):
        lines[-1] = lines[-1][:-1] + "…"
    return lines


def draw_dashed_rect(draw, box, outline, width=2, dash=8, gap=6, radius=10):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=radius, fill=RES_BG, outline=outline, width=width)


def cubic_bezier(p0, p1, p2, p3, steps=40):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def draw_arrow(draw, pts, color, width=3, dashed=False):
    if dashed:
        for i in range(0, len(pts) - 1, 2):
            draw.line([pts[i], pts[min(i + 1, len(pts) - 1)]], fill=color, width=width)
    else:
        draw.line(pts, fill=color, width=width)
    # Arrowhead at end
    p_end = pts[-1]
    p_prev = pts[-3] if len(pts) >= 3 else pts[0]
    ang = math.atan2(p_end[1] - p_prev[1], p_end[0] - p_prev[0])
    size = 11 + width
    a1 = (p_end[0] - size * math.cos(ang - 0.42), p_end[1] - size * math.sin(ang - 0.42))
    a2 = (p_end[0] - size * math.cos(ang + 0.42), p_end[1] - size * math.sin(ang + 0.42))
    draw.polygon([p_end, a1, a2], fill=color)


def draw_pill(draw, center, text, font, bg, fg, border=None):
    tw = draw.textlength(text, font=font)
    th = font.size + 4
    px, py = 12, 5
    x0 = center[0] - tw / 2 - px
    y0 = center[1] - th / 2 - py
    x1 = center[0] + tw / 2 + px
    y1 = center[1] + th / 2 + py
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=bg, outline=border, width=2 if border else 0)
    draw.text((center[0] - tw / 2, center[1] - th / 2 - 1), text, font=font, fill=fg)


def render_workflow(json_path, out_path, title, subtitle_badge, row_order):
    vdata = json.load(open(json_path, encoding="utf-8"))
    doc = vdata["document"]
    nodes = {n["id"]: n for n in doc["nodes"]}
    edges = doc["edges"]

    # Classify nodes
    inputs = [n for n in doc["nodes"] if n["type"] == "wfInput"]
    steps = [nodes[sid] for sid in row_order[0] + row_order[1]]
    resources = [n for n in doc["nodes"] if n["type"] == "wfResource"]
    skill_nodes = [n for n in resources if n["data"].get("items", [{}])[0].get("kind") == "skill"]

    # Map each step -> its written resource file(s)
    step_writes = {s["id"]: [] for s in steps}
    step_reads = {s["id"]: 0 for s in steps}
    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in step_writes and tgt in nodes and nodes[tgt]["type"] == "wfResource":
            step_writes[src].append(nodes[tgt])
        if src in nodes and nodes[src]["type"] == "wfResource" and tgt in step_reads:
            step_reads[tgt] += 1

    # Layout geometry (2x crisp canvas)
    cols = max(len(row_order[0]), len(row_order[1]))
    W = 2400
    H = 1360
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Dot grid
    for gx in range(28, W, 32):
        for gy in range(88, H - 64, 32):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=DOT)

    # Top bar
    draw.rectangle([0, 0, W, 76], fill=TOPBAR)
    draw.line([(0, 76), (W, 76)], fill=(38, 47, 64), width=2)
    f_title = load_font(True, 26)
    f_badge = load_font(False, 18)
    f_card_title = load_font(True, 17)
    f_card_id = load_font(False, 13)
    f_card_body = load_font(False, 14)
    f_small = load_font(False, 13)
    f_edge = load_font(True, 15)

    draw.text((34, 21), title, font=f_title, fill=TEXT_MAIN)
    tx = 34 + int(draw.textlength(title, font=f_title)) + 24

    for txt, fg, bg, bd in [
        (subtitle_badge, TEXT_SUB, (28, 36, 50), (54, 66, 88)),
        ("编译 problems 0 · warnings 0", (74, 222, 128), (20, 42, 34), (34, 90, 65)),
        ("DSH dsh-workflow-lite 0.11.0", (125, 211, 252), (20, 36, 52), (42, 78, 112)),
    ]:
        tw = int(draw.textlength(txt, font=f_badge))
        draw.rounded_rectangle([tx, 20, tx + tw + 26, 56], radius=16, fill=bg, outline=bd, width=2)
        draw.text((tx + 13, 25), txt, font=f_badge, fill=fg)
        tx += tw + 40

    # Left column: Inputs + Skill card
    left_x = 34
    left_w = 340
    iy = 116
    draw.text((left_x, iy - 26), f"执行前输入 ({len(inputs)})", font=f_card_id, fill=INPUT_ACCENT)
    for inp in inputs:
        d = inp["data"]
        ih = 76
        draw.rounded_rectangle([left_x, iy, left_x + left_w, iy + ih], radius=10, fill=INPUT_BG, outline=(46, 72, 102), width=2)
        draw.rounded_rectangle([left_x, iy + 8, left_x + 5, iy + ih - 8], radius=3, fill=INPUT_ACCENT)
        q = d.get("question", inp["id"])
        q_lines = wrap_text(draw, q, f_card_body, left_w - 28, max_lines=2)
        for li, ln in enumerate(q_lines):
            draw.text((left_x + 16, iy + 11 + li * 21), ln, font=f_card_body, fill=TEXT_MAIN)
        tag = "必填" if d.get("required") else ("选择" if d.get("kind") == "choice" else "可选")
        draw.text((left_x + 16, iy + ih - 22), f"{inp['id']}  ·  {tag}", font=f_small, fill=TEXT_DIM)
        iy += ih + 14

    iy += 16
    for sk in skill_nodes:
        d = sk["data"]
        sh = 148
        draw.rounded_rectangle([left_x, iy, left_x + left_w, iy + sh], radius=12, fill=(28, 25, 44), outline=(109, 78, 178), width=2)
        draw.rounded_rectangle([left_x, iy + 10, left_x + 6, iy + sh - 10], radius=3, fill=PALETTE["violet"])
        draw.text((left_x + 18, iy + 12), f"SKILL · {d.get('label', sk['id'])}", font=f_card_title, fill=(216, 180, 254))
        desc_lines = wrap_text(draw, d.get("description", ""), f_small, left_w - 30, max_lines=4)
        for li, ln in enumerate(desc_lines):
            draw.text((left_x + 18, iy + 44 + li * 20), ln, font=f_small, fill=TEXT_SUB)
        iy += sh + 16

    # Main 2-row step grid
    grid_x0 = 420
    grid_w = W - grid_x0 - 44
    col_gap = 42
    card_w = (grid_w - col_gap * (cols - 1)) // cols
    card_h = 186
    res_h = 54
    row_ys = [150, 740]

    step_boxes = {}
    res_boxes = {}

    for r_idx, row_ids in enumerate(row_order):
        ry = row_ys[r_idx]
        # Center row if fewer than cols
        row_total_w = len(row_ids) * card_w + (len(row_ids) - 1) * col_gap
        start_x = grid_x0 + (grid_w - row_total_w) // 2
        for c_idx, sid in enumerate(row_ids):
            sx = start_x + c_idx * (card_w + col_gap)
            step_boxes[sid] = (sx, ry, sx + card_w, ry + card_h)
            # Resource box(es) below step
            w_res = step_writes.get(sid, [])
            for wi, rn in enumerate(w_res):
                rx0 = sx + 10
                ry0 = ry + card_h + 36 + wi * (res_h + 12)
                res_boxes[rn["id"]] = (rx0, ry0, sx + card_w - 10, ry0 + res_h)

    # Draw edges FIRST (behind cards)
    # 1. Step -> Resource write connectors
    for sid, w_res in step_writes.items():
        sx0, sy0, sx1, sy1 = step_boxes[sid]
        cx = (sx0 + sx1) / 2
        for rn in w_res:
            rx0, ry0, rx1, ry1 = res_boxes[rn["id"]]
            draw_arrow(draw, [(cx, sy1), (cx, ry0 - 2)], EDGE_DATA, width=2, dashed=True)

    # 2. Control flow & conditional edges between steps
    for e in edges:
        src, tgt = e["source"], e["target"]
        if src not in step_boxes or tgt not in step_boxes:
            continue
        sx0, sy0, sx1, sy1 = step_boxes[src]
        tx0, ty0, tx1, ty1 = step_boxes[tgt]
        when = (e.get("data") or {}).get("when")
        is_loop = when and ("fail" in when)

        if not when:
            # Normal flow
            if abs(sy0 - ty0) < 20 and tx0 > sx0:
                p0 = (sx1, (sy0 + sy1) / 2)
                p3 = (tx0 - 4, (ty0 + ty1) / 2)
                draw_arrow(draw, [p0, p3], EDGE_MAIN, width=3)
            else:
                # Row 1 end -> Row 2 start (smooth S-curve across gap)
                p0 = ((sx0 + sx1) / 2, sy1 + 100)
                # Connect from right side of row 1 last node down to left/top of row 2 first node
                p0 = (sx1, (sy0 + sy1) / 2)
                mid_y = (sy1 + ty0) / 2 + 40
                pts = (
                    cubic_bezier(p0, (sx1 + 45, p0[1]), (sx1 + 45, mid_y), (sx1 - 60, mid_y), 16)
                    + [(tx0 + 60, mid_y)]
                    + cubic_bezier((tx0 + 60, mid_y), (tx0 - 55, mid_y), (tx0 - 55, (ty0 + ty1) / 2), (tx0 - 4, (ty0 + ty1) / 2), 16)
                )
                draw_arrow(draw, pts, EDGE_MAIN, width=3)
        elif not is_loop:
            # pass branch (clean horizontal gold arrow with pill above)
            p0 = (sx1, (sy0 + sy1) / 2)
            p3 = (tx0 - 4, (ty0 + ty1) / 2)
            draw_arrow(draw, [p0, p3], EDGE_COND, width=4)
            mid = ((p0[0] + p3[0]) / 2, p0[1] - 26)
            draw_pill(draw, mid, when, f_edge, (38, 34, 16), EDGE_COND, EDGE_COND)
        else:
            # Loop-back pink dashed arc
            if abs(sy0 - ty0) < 20:
                # Same row loopback (over top of row 2)
                p0 = ((sx0 + sx1) / 2 - 20, sy0)
                p3 = ((tx0 + tx1) / 2 + 20, ty0 - 4)
                arc_y = sy0 - 110
                pts = cubic_bezier(p0, (p0[0], arc_y), (p3[0], arc_y), p3, 36)
                draw_arrow(draw, pts, EDGE_LOOP, width=4, dashed=True)
                mid = pts[len(pts) // 2]
                draw_pill(draw, (mid[0], mid[1] - 12), when, f_edge, (44, 20, 36), EDGE_LOOP, EDGE_LOOP)
            else:
                # Cross-row loopback (e.g. verify -> infer_probe)
                p0 = ((sx0 + sx1) / 2 + 30, sy0)
                p3 = ((tx0 + tx1) / 2, ty1 + 96)
                p3 = ((tx0 + tx1) / 2 + 35, ty1 + 4)
                pts = cubic_bezier(p0, (p0[0] + 60, sy0 - 140), (p3[0] + 60, ty1 + 140), p3, 40)
                draw_arrow(draw, pts, EDGE_LOOP, width=4, dashed=True)
                mid = pts[len(pts) // 2]
                draw_pill(draw, (mid[0] + 24, mid[1]), when, f_edge, (44, 20, 36), EDGE_LOOP, EDGE_LOOP)

    # Draw step cards
    for sid, (x0, y0, x1, y1) in step_boxes.items():
        n = nodes[sid]
        d = n["data"]
        accent = PALETTE.get(d.get("color", "blue"), PALETTE["blue"])
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.rounded_rectangle([x0, y0 + 10, x0 + 6, y1 - 10], radius=3, fill=accent)

        # Title + id pill (auto-fit so title never overlaps id pill)
        id_w = int(draw.textlength(sid, font=f_small))
        pill_x0 = x1 - id_w - 24
        draw.rounded_rectangle([pill_x0, y0 + 14, x1 - 10, y0 + 36], radius=6, fill=(32, 40, 54), outline=(58, 70, 92), width=1)
        draw.text((pill_x0 + 7, y0 + 16), sid, font=f_small, fill=TEXT_DIM)

        label = d.get("label", sid)
        max_title_w = pill_x0 - (x0 + 18) - 8
        while draw.textlength(label, font=f_card_title) > max_title_w and len(label) > 4:
            label = label[:-2] + "…"
        draw.text((x0 + 18, y0 + 15), label, font=f_card_title, fill=TEXT_MAIN)

        # Summary from prompt first line
        first_line = d.get("prompt", "").split("\n")[0]
        body_lines = wrap_text(draw, first_line, f_card_body, card_w - 34, max_lines=3)
        for li, ln in enumerate(body_lines):
            draw.text((x0 + 18, y0 + 50 + li * 24), ln, font=f_card_body, fill=TEXT_SUB)

        # Footer chips: writes, reads, chars
        fy = y1 - 36
        fx = x0 + 18
        w_names = [r["data"]["items"][0]["value"] for r in step_writes.get(sid, [])]
        chips = []
        if w_names:
            chips.append((f"产 {w_names[0]}" + (f" +{len(w_names)-1}" if len(w_names) > 1 else ""), (147, 197, 253)))
        if step_reads.get(sid, 0):
            chips.append((f"读 {step_reads[sid]}", (134, 239, 172)))
        chips.append((f"{len(d.get('prompt', ''))} 字", TEXT_DIM))
        for ctxt, cfg in chips:
            cw = int(draw.textlength(ctxt, font=f_small))
            if fx + cw + 16 > x1 - 10:
                break
            draw.rounded_rectangle([fx, fy, fx + cw + 14, fy + 24], radius=5, fill=(18, 24, 34), outline=(48, 58, 78), width=1)
            draw.text((fx + 7, fy + 2), ctxt, font=f_small, fill=cfg)
            fx += cw + 20

    # Draw resource file cards (with crisp vector document icon)
    for rid, (x0, y0, x1, y1) in res_boxes.items():
        rn = nodes[rid]
        fname = rn["data"]["items"][0]["value"]
        draw_dashed_rect(draw, [x0, y0, x1, y1], outline=RES_BORDER, width=2, radius=9)
        ix, iy = x0 + 16, y0 + 16
        draw.rounded_rectangle([ix, iy, ix + 16, iy + 20], radius=3, outline=TEXT_DIM, width=2)
        draw.line([(ix + 4, iy + 7), (ix + 12, iy + 7)], fill=TEXT_DIM, width=1)
        draw.line([(ix + 4, iy + 11), (ix + 12, iy + 11)], fill=TEXT_DIM, width=1)
        draw.line([(ix + 4, iy + 15), (ix + 9, iy + 15)], fill=TEXT_DIM, width=1)
        draw.text((x0 + 42, y0 + 16), fname, font=f_card_body, fill=TEXT_SUB)

    # Bottom legend bar
    draw.rectangle([0, H - 56, W, H], fill=TOPBAR)
    draw.line([(0, H - 56), (W, H - 56)], fill=(38, 47, 64), width=2)
    lx = 36
    ly = H - 36
    legend = [
        (EDGE_MAIN, False, "主链控制流"),
        (EDGE_COND, False, "条件通过 (pass)"),
        (EDGE_LOOP, True, "失败归因回边 (fail / fail_prompt / fail_surface)"),
        (EDGE_DATA, True, "产物写入 / 跨步读取"),
    ]
    for col, is_d, lbl in legend:
        if is_d:
            for k in range(0, 32, 8):
                draw.line([(lx + k, ly + 9), (lx + k + 5, ly + 9)], fill=col, width=3)
        else:
            draw.line([(lx, ly + 9), (lx + 32, ly + 9)], fill=col, width=3)
        draw.text((lx + 42, ly - 2), lbl, font=f_small, fill=TEXT_SUB)
        lx += 42 + int(draw.textlength(lbl, font=f_small)) + 36

    right_note = "由 scripts/render_canvas.py 从工作流 JSON 自动渲染 · 无 API Key / 脱敏展示"
    rw = int(draw.textlength(right_note, font=f_small))
    draw.text((W - rw - 32, ly - 2), right_note, font=f_small, fill=TEXT_DIM)

    # Save crisp WebP
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "WEBP", quality=92, method=6)
    print(f"[RENDERED] {out_path} ({W}x{H})")


if __name__ == "__main__":
    render_workflow(
        os.path.join(REPO_ROOT, "workflows", "破甲制作", "versions", "3.json"),
        os.path.join(REPO_ROOT, "assets", "canvas-v3.webp"),
        "破甲制作 v3",
        "10 步 · 27 节点 · 69 边",
        [
            ["recon", "probe", "bprobe", "infer_probe", "analyze"],
            ["generate", "stress_test", "verify", "report", "feedback_pack"],
        ],
    )
    render_workflow(
        os.path.join(REPO_ROOT, "workflows", "破甲炼化", "versions", "2.json"),
        os.path.join(REPO_ROOT, "assets", "canvas-distillery-v2.webp"),
        "破甲炼化 v2",
        "8 步 · 22 节点 · 41 边",
        [
            ["gather", "survey", "cluster", "webcross"],
            ["distill", "compose", "verify", "armory"],
        ],
    )
