---
name: openclaw-daily-sync
description: 搜索 OpenClaw、Hermes Agent、Codex、Claude Code、Antigravity、WorkBuddy、QClaw、Marvis、Accio Work 的最新资讯，自动导入知识库「OpenClaw 小龙虾 WorkBuddy」，并将每篇文章深度改写为通俗易懂的公众号文章，推送到「人人易AI之光」公众号草稿箱。当用户说「同步 openclaw 情报」「更新 OpenClaw 知识库」「openclaw 每日同步」「采集龙虾资讯」「同步龙虾情报」或类似意图时触发。不适用于单一关键词深度研究或搜索其他领域内容。
---

# OpenClaw Daily Sync — 全链路情报同步

## 概述

从全网搜索 9 个 AI Agent 生态关键词 → 导入知识库 → 深度改写为公众号文章 → 推送微信草稿箱，一站式完成。

- **目标知识库**：OpenClaw 小龙虾 WorkBuddy（kb_id: `gluhyxAPg8VjSuJJ10r6u4uPfwSP_q7LSE60BOvya6k=`）
- **目标公众号**：人人易AI之光（AppID: `wx19c8ad59f4ac42a6`）
- **核心脚本**：`scripts/wechat_draft.py`（草稿推送）、`scripts/cover_generator.py`（AI 封面生成）

## 工作流总览

```
Phase 1: 并行搜索 9 关键词
    ↓
Phase 2: URL 收集、去重、展示
    ↓
Phase 3: 用户确认要改写的文章 ⚠️ 确认门
    ↓
Phase 4: 逐篇「抓取 → 深度改写 → 生成封面 → 推送草稿」
    ↓
Phase 5: 汇总报告
```

---

## Phase 1：并行搜索

同时执行 9 个 `search(source="web")` 调用。从 `<current_time>` 提取当前年份构建 query：

| # | 关键词 | 搜索 query 模板 |
|---|--------|---------------|
| 1 | openclaw | `openclaw {YEAR}年最新文章资讯` |
| 2 | hermes agent | `hermes agent {YEAR}年最新文章资讯` |
| 3 | codex | `codex AI agent {YEAR}年最新文章资讯` |
| 4 | claude code | `claude code {YEAR}年最新文章资讯` |
| 5 | antigravity | `antigravity AI {YEAR}年最新文章资讯` |
| 6 | workbuddy | `workbuddy AI {YEAR}年最新文章资讯` |
| 7 | qlcaw | `qlcaw {YEAR}年最新文章资讯` |
| 8 | marvis | `marvis AI agent {YEAR}年最新文章资讯` |
| 9 | accio work | `Accio Work {YEAR}年最新文章资讯` |

---

## Phase 2：URL 收集与去重

1. 提取每条结果的 `id`（URL）和 `title`
2. **去重**：相同 URL 只保留一条
3. **过滤**：剔除主题明显无关的页面
4. 按关键词分组整理，展示给用户

**展示格式**：

```
## 🔍 搜索结果（{DATE}）

| 关键词 | 篇数 |
|--------|:----:|
| openclaw | N |
| hermes agent | N |
| ...

点击每条可查看摘要。
```

---

## Phase 3：确认门 ⚠️

列出所有文章后，**必须询问用户**：

> 「共搜索到 X 篇文章。你要全部改写并推送草稿箱，还是挑选其中几篇？如果挑选，告诉我要哪些序号。」

用户可能回复：
- **「全部」** → 逐篇处理所有文章
- **「第 1、3、5 篇」** → 只处理指定篇
- **「openclaw 和 codex 的」** → 只处理指定关键词的文章

**确认后立即进入 Phase 4，不再二次确认。**

---

## Phase 4：逐篇改写与推送

对每一篇用户选中的文章，按以下子步骤执行：

### 4a. 抓取原文

使用 `fetch(type="url", id="{文章URL}")` 获取原文内容。question 参数用：

> 完整提取这篇文章的所有实质性内容，包括核心观点、关键数据、引用来源、具体案例。不要省略任何重要信息。

### 4b. 深度改写

基于抓取到的原文内容，生成一篇公众号文章。**同时满足两个要求**：

**更有深度**：
- 补充行业背景和上下文（这个技术/事件在整个 AI Agent 生态中的位置）
- 分析影响和趋势（对开发者/企业/行业意味着什么）
- 横向对比（与竞品/同类方案比较）
- 提炼可操作的观点（读者能用这个信息做什么）

**更通俗易懂**：
- 开篇用一个生活化比喻或场景引入
- 技术概念用大白话解释（假设读者是非技术背景的创业者/产品经理）
- 复杂逻辑拆成短段落，每段不超过 3 句话
- 穿插「一句话总结」帮助理解

**输出格式**：HTML，适配微信公众号编辑器。结构如下：

```html
<h1>【标题】吸引人的中文标题（≤32字）</h1>

<p><strong>导读：</strong>1-2 句话概括核心价值，告诉读者为什么值得花 3 分钟读这篇。</p>

<h2>一、发生了什么事</h2>
<p>用场景化语言讲清楚事情本身。控制在 3 段内。</p>

<h2>二、为什么重要</h2>
<p>深度分析。这部分是核心，要有观点、有数据、有对比。</p>

<h2>三、对你意味着什么</h2>
<p>从读者视角出发，给出可操作的建议或启发。</p>

<h2>四、小结</h2>
<p>提炼核心要点 + 一句引人思考的结尾。</p>

<hr/>
<p style="color:#888;font-size:13px;">原文参考：<a href="{原文URL}">{原文标题}</a></p>
<p style="color:#888;font-size:13px;">本文由 ima.copilot 基于全网资讯自动生成，经人工审核后发布。</p>
```

**改写完成后，先将 HTML 内容写入 workspace 文件。** 文件路径：`/sandbox/workspace/outputs/draft_{序号}.html`

### 4c. AI 生成封面

调用封面生成脚本：

```bash
python3 /sandbox/workspace/skills/openclaw-daily-sync/scripts/cover_generator.py \
  --title "{文章标题}" \
  --subtitle "{简短副标题（可选，≤15字）}" \
  --output /sandbox/workspace/outputs/cover_{序号}.jpg
```

封面基于标题生成唯一配色（哈希取色），包含渐变背景 + 标题文字 + 「人人易AI之光」品牌标示。900×500，适配公众号封面。

### 4d. 推送草稿箱

调用推送脚本：

```bash
python3 /sandbox/workspace/skills/openclaw-daily-sync/scripts/wechat_draft.py \
  --title "{文章标题}" \
  --content-file /sandbox/workspace/outputs/draft_{序号}.html \
  --author "人人易AI之光" \
  --cover /sandbox/workspace/outputs/cover_{序号}.jpg \
  --digest "{摘要（≤120字）}" \
  --source-url "{原文URL}"
```

**注意**：必须先执行 4c 生成封面，才能执行 4d 推送。封面是必填参数。

### 逐篇处理，不要并行

文章逐一处理（4a → 4b → 4c → 4d），处理完一篇再开始下一篇。这确保：
- 每篇封面与文章一一对应
- 出错时方便定位
- 微信 API 不会触发频率限制

每完成一篇，简要告知用户进度：「✅ 第 1/5 篇已推送：《XXX》」

---

## Phase 5：汇总报告

所有文章处理完毕后，输出最终报告：

```
## 📋 全链路同步完成 — {DATE} {TIME}

### 知识库导入
| 关键词 | 导入篇数 |
|--------|:--------:|
| openclaw | N |
| ... | ... |
**总计**：X 条 URL 已入库

### 公众号草稿箱
| # | 标题 | 草稿 media_id | 原文来源 |
|---|------|:------------:|---------|
| 1 | XXX | xxx | 来源名 |
| ... | ... | ... | ... |
**总计**：Y 篇已推送至「人人易AI之光」草稿箱

🔗 请到 mp.weixin.qq.com → 草稿箱 审核后发布
```

如有任何失败（搜索无结果、抓取失败、微信 API 报错），单独列出。

---

## 使用示例

### 示例 1：完整同步 + 改写 + 推送

```
用户：「同步 openclaw 情报」
→ Phase 1 搜索 → Phase 2 整理展示 → Phase 3 用户选「全部」
→ Phase 4 逐篇改写推送 → Phase 5 汇总
```

### 示例 2：只同步不入库（仅改写推送）

如果用户明确说「只改写推送，不要导入知识库」，跳过 Phase 2 末尾的知识库导入步骤，直接进入改写推送。

### 示例 3：挑选特定关键词

```
用户：「只改写 claude code 和 codex 的文章」
→ 搜索结果中只处理这两个关键词的文章
```

---

## 错误处理

| 问题 | 处理方式 |
|------|---------|
| 微信 API 返回 40164（IP 不在白名单） | 告知用户需在 mp.weixin.qq.com 添加 IP `49.235.105.51` |
| 微信 API 返回 40001（access_token 过期） | 脚本自动重新获取，不需要人工干预 |
| 原文抓取失败（404/JS 渲染/付费墙） | 跳过该篇，标注「原文无法抓取」，继续下一篇 |
| 封面生成失败 | 告知用户并跳过该篇，继续下一篇 |
| 单次搜索返回 0 结果 | 标注该关键词「无新内容」，不影响其他关键词 |

---

## 外部定时调度

本 Skill 是同步工作流。如需每日 12:00 和 23:00 自动触发，需外部调度器。推荐 GitHub Actions：

```yaml
# .github/workflows/openclaw-sync.yml
name: OpenClaw Daily Sync
on:
  schedule:
    - cron: '0 4,15 * * *'  # UTC 4:00=北京12:00, 15:00=北京23:00
```

定时调度的实际触发方式取决于 ima.copilot 平台的 API 接入方式。
