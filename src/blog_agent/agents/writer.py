"""
FILE: writer.py

KYA KARTA HAI:
Ye file Parallel Worker (Section Writer) Agent Node implement karti hai.

RESPONSIBILITY:
Send fan-out ke throw har individual Task payload process karna, Gemini se standard Markdown section generate karna, aur `_message_text` helper use karke plain text extract karke tuple `(task_id, section_md)` append state me return karna.

KON USE KARTA HAI:
- graph/builder.py (Worker Node ke tarah register karne ke liye)
- graph/routing.py (fanout conditional edge ke through payloads receive karta hai)

DEPENDENCIES:
- domain/schemas.py -> Task, Plan, EvidenceItem
- providers/llm.py -> get_text_llm
- prompts/writer.py -> WORKER_SYSTEM
- utils/messages.py -> _message_text

REVISION:
writer.py = Parallel section writer worker.
"""

from langchain_core.messages import SystemMessage, HumanMessage

from ..domain.schemas import Task, Plan, EvidenceItem
from ..providers.llm import get_text_llm
from ..prompts.writer import WORKER_SYSTEM
from ..utils.messages import _message_text


def worker_node(payload: dict) -> dict:
    """
    Parallel Worker Node:
    - Input: Send payload dict containing single task, plan dict, topic, mode, evidence
    - Action: Gemini se markdown section content write karwana
    - Output: Dictionary with sections list tuple `[(task.id, section_md)]` (accumulated via operator.add reducer)
    """
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]

    bullets_text = "\n- " + "\n- ".join(task.bullets)
    evidence_text = "\n".join(
        f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}"
        for e in evidence[:20]
    )

    llm = get_text_llm()
    resp = llm.invoke(
        [
            SystemMessage(content=WORKER_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog title: {plan.blog_title}\n"
                    f"Audience: {plan.audience}\n"
                    f"Tone: {plan.tone}\n"
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Constraints: {plan.constraints}\n"
                    f"Topic: {payload['topic']}\n"
                    f"Mode: {payload.get('mode')}\n"
                    f"As-of: {payload.get('as_of')} (recency_days={payload.get('recency_days')})\n\n"
                    f"Section title: {task.title}\n"
                    f"Goal: {task.goal}\n"
                    f"Target words: {task.target_words}\n"
                    f"Tags: {task.tags}\n"
                    f"requires_research: {task.requires_research}\n"
                    f"requires_citations: {task.requires_citations}\n"
                    f"requires_code: {task.requires_code}\n"
                    f"Bullets:{bullets_text}\n\n"
                    f"Evidence (ONLY cite these URLs):\n{evidence_text}\n"
                )
            ),
        ]
    )
    section_md = _message_text(resp).strip()

    return {"sections": [(task.id, section_md)]}


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Parallel me ek single section Markdown write karna.
# Isko call karta hai: graph/routing.py (via Send fanout) -> LangGraph engine
# Ye call karta hai: providers/llm.py (Gemini), utils/messages.py (_message_text)
# Data flow: Task Payload -> worker_node() -> (task_id, section_md) -> Reducer state
# Shortcut: worker_node = Parallel section writer.
# ============================================================
