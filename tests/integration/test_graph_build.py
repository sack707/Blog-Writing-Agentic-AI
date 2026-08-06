"""
FILE: test_graph_build.py

KYA KARTA HAI:
Ye file LangGraph StateGraph topology compilation aur node wiring test karti hai without invoking LLM/Tavily API calls.

RESPONSIBILITY:
- build_graph() successfully compile hone verify karna
- Node names (`router`, `research`, `orchestrator`, `worker`, `reducer`) presence check karna

KON USE KARTA HAI:
- pytest runner / manual validation

DEPENDENCIES:
- blog_agent.graph.builder -> build_graph

REVISION:
test_graph_build.py = LangGraph integration & topology compilation test.
"""

import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from blog_agent.graph.builder import build_graph


def test_graph_compilation():
    graph_app = build_graph()
    assert graph_app is not None
    # Verify graph node names
    nodes = list(graph_app.nodes.keys())
    assert "router" in nodes
    assert "research" in nodes
    assert "orchestrator" in nodes
    assert "worker" in nodes
    assert "reducer" in nodes
    print("Graph compilation test passed successfully!")


if __name__ == "__main__":
    test_graph_compilation()
