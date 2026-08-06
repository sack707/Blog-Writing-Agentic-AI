# Developer Guide: Extending BlogAgent

This guide explains how to extend, modify, or add new capabilities to the BlogAgent platform.

---

## 1. How to Add a New Agent Node

Suppose you want to add an **SEO Optimization Agent** that runs after the reducer:

1. **Define Schema (if needed)** in `src/blog_agent/domain/schemas.py`:
   ```python
   class SEOReport(BaseModel):
       meta_description: str
       keywords: List[str]
   ```
2. **Add State Field (if needed)** in `src/blog_agent/domain/state.py`:
   ```python
   class BlogState(TypedDict):
       ...
       seo_report: Optional[dict]
   ```
3. **Create Prompt** in `src/blog_agent/prompts/seo.py`:
   ```python
   SEO_SYSTEM = "You are an SEO expert..."
   ```
4. **Create Agent Module** in `src/blog_agent/agents/seo_agent.py`:
   ```python
   def seo_node(state: BlogState) -> dict:
       llm = get_text_llm()
       ...
       return {"seo_report": report.model_dump()}
   ```
5. **Register Node & Edges** in `src/blog_agent/graph/builder.py`:
   ```python
   g.add_node("seo", seo_node)
   g.add_edge("reducer", "seo")
   g.add_edge("seo", END)
   ```
6. **Add UI Tab (if needed)** under `src/blog_agent/ui/components/seo.py` and connect it in `workspace.py`.

---

## 2. How to Add a New Search / Retrieval Tool

1. Create a provider function in `src/blog_agent/providers/search.py`:
   ```python
   def wikipedia_search(query: str) -> List[dict]:
       ...
   ```
2. Call `wikipedia_search()` inside `src/blog_agent/agents/researcher.py`.

---

## 3. How to Replace or Swap the LLM Provider

1. Open `src/blog_agent/providers/llm.py`.
2. Replace `ChatGoogleGenerativeAI` with `ChatOpenAI` or `ChatAnthropic`:
   ```python
   def get_text_llm():
       return ChatOpenAI(model="gpt-4o-mini")
   ```
3. Because all agents call `get_text_llm()`, zero code changes are required in `agents/`, `graph/`, or `ui/`.

---

## 4. How to Add a New UI Tab

1. Create a component in `src/blog_agent/ui/components/my_tab.py`:
   ```python
   def render_my_tab(out):
       st.markdown(...)
   ```
2. Import and render in `src/blog_agent/ui/components/workspace.py`:
   ```python
   tab1, tab2, ..., my_tab = st.tabs([...])
   with my_tab:
       render_my_tab(out)
   ```
