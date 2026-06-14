# OpenClaw Daily Sync

全链路 AI Agent 生态情报同步 Skill — 从全网搜索到公众号草稿箱，一站完成。

## 能力链

```
全网搜索 9 大关键词 → 自动导入知识库 → 深度改写公众号文章 → AI 生成封面 → 推送微信草稿箱
```

## 覆盖关键词

OpenClaw · Hermes Agent · Codex · Claude Code · Antigravity · WorkBuddy · QClaw · Marvis · Accio Work

## 触发方式

在 ima.copilot 对话中说：

> 「同步 openclaw 情报」

## 目标

- **知识库**：OpenClaw 小龙虾 WorkBuddy
- **公众号**：人人易AI之光

## 目录结构

```
├── SKILL.md                 # 技能定义与工作流
├── scripts/
│   ├── wechat_draft.py      # 微信公众号草稿箱推送
│   └── cover_generator.py   # AI 封面图生成（PIL）
└── README.md
```

## 依赖

- Python 3.x + Pillow
- 微信公众号 AppID / AppSecret（已在脚本中配置）
- IMA OpenAPI 凭证（环境变量）

## 许可

MIT
