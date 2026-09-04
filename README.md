# supervisor-skills

把一项大工程交给一个「总管会话」统筹的三个配套 skill：它只出任务书、判据、裁决与合入，**不亲自写实现代码**。

同一份文件在 **Claude Code** 和 **Codex CLI** 两边都能用——两边的 skill 格式相同（一个目录 + 一个带 YAML 头的 `SKILL.md`）。正文里不出现任何一端专有的工具名，具体命令收在 `skills/supervisor-session/references/runtime-map.md`。

## 三个 skill

| Skill | 干什么 | 什么时候触发 |
|---|---|---|
| `supervisor-session` | 总管的完整工作准则：冻结基线、单一总账、拆卡派发、只读巡检、合入、测试分层、汇报、开收工自查 | 用户指定某个会话当总管／监察／管理者，要它统筹而不是亲自干活 |
| `decision-briefing` | 需要用户拍板或同步进展时的固定五段格式，让对方不必追问就能决策 | 汇报进展、提「要不要做 X」「A 还是 B」、用户问「这是什么／到哪一步了／为什么卡着」 |
| `progress-review-and-dispatch` | 批量盘点在推进的事项，按目标分组、按动作路由定档，报完立刻把动作做掉 | 巡检产出跨线汇总、「该派的都派了吗」「哪些能立刻部署」 |

`supervisor-session` 正文会引用另外两个，三个一起装最完整。

## 装法

Claude Code：

```bash
cp -R skills/* ~/.claude/skills/
```

Codex CLI：

```bash
cp -R skills/* ~/.codex/skills/
```

只给某个项目用，就放进该仓库的 `.claude/skills/`（Claude Code）。装完重开会话，问一句「你是这次移植的总管，先说说你打算怎么派活」就能验证是否加载。

## 落地前要填的空

下面这些位置写的是占位符，用之前替换成你们自己的值：

- `<集成分支>`——各模块分支往上合的那条分支
- `<文档目录>`——总账与任务书放哪
- 团队统一的测试入口（容器／预发／浏览器／API）、拿存量数据回放复验的工具
- 远端登录命令、外部依赖子仓的安装命令、端到端测试会改写的生成物文件名

正文里保留的具体数字（例如重跑上限）只是示例量级，按自己情况调。

## 这套东西的三条核心主张

1. **总管的产出是任务书、判据、裁决与合入，不是实现。** 发现自己在写实现代码就停下，改成派卡。
2. **一切状态只读获取，非必要不打扰任何会话。** 能从 git、读数文件、会话记录里读到的，一律不发消息问——发消息会重启空闲会话、污染读数。
3. **测试分层。** 实现会话只跑轻量验证，重测试（集成、端到端、浏览器、真模型验收）统一由总管串行做，否则多条线同时起栈会压垮机器。

---

# supervisor-skills (English)

Three companion skills for running a large engineering effort through a **supervisor session**: it produces task briefs, acceptance criteria, rulings, and merges — it does **not** write the implementation itself.

The same files work in both **Claude Code** and **Codex CLI**: both look for a directory containing a `SKILL.md` with YAML frontmatter. The skill bodies avoid host-specific tool names; concrete per-host commands live in `skills/supervisor-session/references/runtime-map.md`.

> **Note:** the skill bodies are written in Chinese. This README is bilingual, the instructions themselves are not (yet).

## The three skills

| Skill | What it does | When it fires |
|---|---|---|
| `supervisor-session` | The full supervisor playbook: freeze the baseline, keep one ledger, split and dispatch work, patrol read-only, merge, tier the testing, report, and run open/close checklists | The user puts a session in charge of a big effort and tells it to coordinate rather than implement |
| `decision-briefing` | A fixed five-part shape for anything the user has to decide, so they can rule on it without a round of follow-up questions | Reporting progress, "should we do X", "A or B", "what is this / where does it stand / why is it stuck" |
| `progress-review-and-dispatch` | Sweep everything in flight, bucket each item by the action it needs, then actually take those actions | Cross-workstream status sweeps, "did everything that should be dispatched get dispatched", "what can ship now" |

## Install

Claude Code:

```bash
cp -R skills/* ~/.claude/skills/
```

Codex CLI:

```bash
cp -R skills/* ~/.codex/skills/
```

Restart the session, then ask something like "you're the supervisor for this migration — how would you start?" to confirm the skill loads.

## Fill in the blanks

The following are placeholders — substitute your own values before use:

- `<集成分支>` — the integration branch module branches merge into
- `<文档目录>` — where the ledger and task briefs live
- your team's standard test entry points (container / staging / browser / API), and whatever you use to replay historical data
- remote login command, dependency-install command for external sub-repos, generated files your end-to-end tests rewrite

Concrete numbers left in the text (retry ceilings and the like) are illustrative orders of magnitude — recalibrate them for your own setup.

## Three claims at the core

1. **A supervisor's output is task briefs, criteria, rulings, and merges — not code.** Catch yourself writing implementation code and stop; turn it into a dispatched task instead.
2. **Get state read-only; don't interrupt sessions unless you must.** Anything readable from git, report files, or session records is never worth a message — messaging wakes idle sessions and pollutes the readings.
3. **Tier the testing.** Implementation sessions run only lightweight checks; heavy testing (integration, end-to-end, browser, real-model acceptance) is run serially by the supervisor, or parallel stacks will crush the machine.
