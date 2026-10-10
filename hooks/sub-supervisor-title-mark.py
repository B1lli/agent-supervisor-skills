#!/usr/bin/env python3
# PreToolUse 提醒：派出分管会话时，标题要以中文感叹号「！」开头，方便用户在会话列表里找到分管。
# 「这次派发是不是分管」由总管自己判断：它按 supervisor-session skill 写分管任务书时，首句固定是
# 「你是 <类> 的分管，按 supervisor-session skill 工作」。本钩子只认这句总管自己写下的身份声明，不猜语义。
# 派发工具的入参里没有 title 字段时不检查（标题改不了，拦了也没用）。
# 有这句、标题却没有「！」时拦下，把原因还给总管，由它自己改标题重派；其余情况一律放行，出错也放行。
import json
import re
import sys

MARK = "！"
TITLE_MAX = 60
DECLARATION = re.compile(r"你是[^。\n]{0,40}?的分管\s*[，,]\s*按\s*supervisor-session")


def main() -> None:
    try:
        check()
    except Exception:
        return


def check() -> None:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    if not isinstance(tool_input, dict) or "title" not in tool_input:
        return
    prompt = tool_input.get("prompt") or ""
    title = tool_input.get("title") or ""
    if not isinstance(prompt, str) or not isinstance(title, str):
        return
    if not DECLARATION.search(prompt) or title.startswith(MARK):
        return
    suggested = (MARK + title.lstrip("!！ "))[:TITLE_MAX]
    reason = (
        "这份任务书声明它是分管（「你是…的分管，按 supervisor-session skill 工作」），"
        f"按 supervisor-session skill 的约定，分管会话的标题要以中文感叹号「{MARK}」开头，方便在会话列表里找到分管。"
        f"请把 title 改成「{suggested}」（或你认为更合适、同样以「{MARK}」开头的标题，不超过 {TITLE_MAX} 字）后重新派发。"
        "如果这其实不是分管，就去掉任务书里那句分管声明再派。"
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )

if __name__ == "__main__":
    main()
