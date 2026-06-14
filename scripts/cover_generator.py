#!/usr/bin/env python3
"""
AI 封面图生成器
用法: python3 cover_generator.py --title "文章标题" --output /path/to/cover.jpg [--subtitle "副标题"]

基于 PIL 生成 900x500 专业封面图，含渐变背景 + 标题文字 + 品牌标示
"""

import argparse
import os
import sys
import hashlib
import colorsys
from PIL import Image, ImageDraw, ImageFont


CANVAS_W = 900
CANVAS_H = 500
PADDING = 50


def get_font(size, bold=False):
    """逐级降级查找可用中文字体"""
    candidates = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def title_to_color(title):
    """基于标题哈希生成一致的配色"""
    h = hashlib.md5(title.encode()).digest()
    hue = (h[0] * 256 + h[1]) / 65536.0
    sat = 0.5 + (h[2] / 512.0)
    light = 0.35 + (h[3] / 1024.0)
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return (int(r * 255), int(g * 255), int(b * 255))


def generate_gradient(size, color_top, color_bottom):
    """生成从上到下的渐变图"""
    w, h = size
    img = Image.new("RGB", size)
    for y in range(h):
        ratio = y / h
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img


def wrap_text(draw, text, font, max_width):
    """中文自动换行"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def generate_cover(title, output_path, subtitle=""):
    base_color = title_to_color(title)
    dark_color = tuple(max(0, c - 80) for c in base_color)
    very_dark = tuple(max(0, c - 140) for c in base_color)
    light_color = tuple(min(255, c + 60) for c in base_color)

    bg = generate_gradient((CANVAS_W, CANVAS_H), dark_color, very_dark)
    draw = ImageDraw.Draw(bg)

    accent_w = 8
    draw.rectangle([PADDING, PADDING, PADDING + accent_w, CANVAS_H - PADDING], fill=light_color)

    title_font = get_font(38, bold=True)
    sub_font = get_font(20)
    brand_font = get_font(14)
    source_font = get_font(13)

    max_title_w = CANVAS_W - PADDING * 2 - accent_w - 20
    title_lines = wrap_text(draw, title, title_font, max_title_w)

    if len(title_lines) > 2:
        title_lines = title_lines[:2]
        title_lines[-1] = title_lines[-1][:15] + "…"

    title_block_h = len(title_lines) * 52
    title_y_start = (CANVAS_H - title_block_h) // 2 - 20

    for i, line in enumerate(title_lines):
        y = title_y_start + i * 52
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw = bbox[2] - bbox[0]
        x = PADDING + accent_w + 15
        draw.text((x + 1, y + 1), line, font=title_font, fill=(0, 0, 0, 80))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((x + dx, y + dy), line, font=title_font, fill=(0, 0, 0, 30))
        draw.text((x, y), line, font=title_font, fill=(255, 255, 255))

    if subtitle:
        sub_y = title_y_start + len(title_lines) * 52 + 10
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        sub_x = PADDING + accent_w + 15
        draw.text((sub_x, sub_y), subtitle, font=sub_font, fill=light_color)

    brand_text = "人人易AI之光"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    bw = bbox[2] - bbox[0]
    draw.text((CANVAS_W - PADDING - bw, CANVAS_H - PADDING - 20), brand_text, font=brand_font, fill=(180, 180, 180))

    divider_y = CANVAS_H - PADDING - 8
    draw.line([(PADDING + accent_w + 15, divider_y), (CANVAS_W - PADDING, divider_y)], fill=(80, 80, 80), width=1)

    source_text = "微信公众号 · 深度解读"
    draw.text((PADDING + accent_w + 15, divider_y + 6), source_text, font=source_font, fill=(140, 140, 140))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    bg.save(output_path, "JPEG", quality=92)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="AI 封面图生成器")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--output", required=True, help="输出图片路径")
    parser.add_argument("--subtitle", default="", help="副标题（可选）")
    args = parser.parse_args()

    path = generate_cover(args.title, args.output, args.subtitle)
    print(f"✅ 封面生成: {path}")
    print(f"output={path}")


if __name__ == "__main__":
    main()
