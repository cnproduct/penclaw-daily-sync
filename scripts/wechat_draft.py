#!/usr/bin/env python3
"""
微信公众号草稿箱推送工具
用法: python3 wechat_draft.py --title "标题" --content-file /path/to/content.html --author "人人易AI之光" --cover /path/to/cover.jpg [--digest "摘要"] [--source-url "https://..."]
"""

import argparse
import json
import sys
import os
import requests

APPID = "wx19c8ad59f4ac42a6"
APPSECRET = "18e9a87793f16d9005f6e0f6b6690765"
TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"


def get_access_token():
    resp = requests.get(
        TOKEN_URL,
        params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
        timeout=30
    ).json()
    if "access_token" not in resp:
        raise Exception(f"获取 access_token 失败: {resp}")
    print(f"✅ access_token 获取成功")
    return resp["access_token"]


def upload_cover(access_token, file_path):
    """上传封面图为永久素材，返回 media_id"""
    url = f"{UPLOAD_URL}?access_token={access_token}&type=image"
    with open(file_path, "rb") as f:
        resp = requests.post(url, files={"media": (os.path.basename(file_path), f, "image/jpeg")}, timeout=60).json()
    if "media_id" not in resp:
        raise Exception(f"上传封面失败: {resp}")
    print(f"✅ 封面上传成功 media_id={resp['media_id']}")
    return resp["media_id"]


def create_draft(access_token, title, content, thumb_media_id, author="人人易AI之光", digest="", source_url=""):
    """创建草稿，返回 draft_media_id"""
    payload = {
        "articles": [{
            "title": title[:32],
            "thumb_media_id": thumb_media_id,
            "author": author[:16],
            "digest": (digest or content[:54].replace("<", "").replace(">", "").strip())[:120],
            "content": content,
            "content_source_url": source_url,
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
            "show_cover_pic": 1
        }]
    }
    resp = requests.post(
        f"{DRAFT_URL}?access_token={access_token}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        timeout=30
    ).json()
    if "media_id" not in resp:
        raise Exception(f"创建草稿失败: {resp}")
    print(f"✅ 草稿创建成功 media_id={resp['media_id']}")
    return resp["media_id"]


def main():
    parser = argparse.ArgumentParser(description="推送文章到微信公众号草稿箱")
    parser.add_argument("--title", required=True, help="文章标题（≤32字）")
    parser.add_argument("--content-file", required=True, help="文章正文 HTML 文件路径")
    parser.add_argument("--author", default="人人易AI之光", help="作者名（≤16字）")
    parser.add_argument("--cover", required=True, help="封面图片路径（JPG/PNG, 900x500）")
    parser.add_argument("--digest", default="", help="摘要（≤120字）")
    parser.add_argument("--source-url", default="", help="原文链接")
    args = parser.parse_args()

    if not os.path.exists(args.content_file):
        print(f"❌ 正文文件不存在: {args.content_file}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.cover):
        print(f"❌ 封面文件不存在: {args.cover}", file=sys.stderr)
        sys.exit(1)

    with open(args.content_file, "r", encoding="utf-8") as f:
        content = f.read()

    token = get_access_token()
    thumb_id = upload_cover(token, args.cover)
    draft_id = create_draft(
        token,
        title=args.title,
        content=content,
        thumb_media_id=thumb_id,
        author=args.author,
        digest=args.digest,
        source_url=args.source_url
    )
    print(f"\n🎉 推送完成！草稿 media_id: {draft_id}")
    print(f"请到 mp.weixin.qq.com → 草稿箱 查看")


if __name__ == "__main__":
    main()
