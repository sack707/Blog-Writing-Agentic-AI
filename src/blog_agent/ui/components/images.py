"""
FILE: images.py

KYA KARTA HAI:
Ye file Images Tab (Generated diagram gallery, specifications JSON expander, ZIP download button) render karti hai.

RESPONSIBILITY:
`images/` directory ke local image files gallery grid me render karna.

KON USE KARTA HAI:
- ui/components/workspace.py

DEPENDENCIES:
- streamlit
- pathlib -> Path
- utils/markdown -> images_zip
- config/settings -> IMAGES_DIR

REVISION:
images.py = Generated images gallery component.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st

from ...utils.markdown import images_zip
from ...config.settings import IMAGES_DIR


def render_images_tab(out: Optional[Dict[str, Any]]):
    """
    Renders Images gallery tab and specifications expander.
    """
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Generated Images & Visual Artifacts")
    if not out:
        st.info("No images generated for this article.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    specs = out.get("image_specs") or []
    images_dir = IMAGES_DIR

    if not specs and not images_dir.exists():
        st.info("No images generated for this article.")
    else:
        if specs:
            with st.expander("View Image Specifications"):
                st.json(specs)

        if images_dir.exists():
            files = [p for p in images_dir.iterdir() if p.is_file()]
            if files:
                cols_img = st.columns(2)
                for idx, p in enumerate(sorted(files)):
                    with cols_img[idx % 2]:
                        st.image(str(p), caption=p.name, use_container_width=True)

            z = images_zip(images_dir)
            if z:
                st.download_button(
                    "⬇️ Download Images (ZIP)",
                    data=z,
                    file_name="images.zip",
                    mime="application/zip",
                )
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Generated images gallery tab view render karna.
# Isko call karta hai: ui/components/workspace.py
# Data flow: IMAGES_DIR -> render_images_tab() -> Images gallery grid
# Shortcut: render_images_tab() = Diagram gallery tab.
# ============================================================
