import streamlit as st

from app_data import DOC_LINKS, resolved_docs

st.set_page_config(
    page_title="Sheet Metal Brazing Guide",
    page_icon="🧰",
    layout="wide",
)

st.title("Sheet Metal Brazing & Welding Companion")

st.markdown(
    """
    This Streamlit app organizes practical guidance inspired by MIL-SD-248D and MIL-S-23284A.
    Use the sidebar to navigate topic-specific pages including materials, inspection checklists,
    qualification tests, brazing requirements, and engineering equations. Local copies of the
    reference PDFs are expected under `/files` (see References page for status). Because this
    environment cannot fetch external files, download the specifications manually if needed.
    """
)

st.info(
    """
    **Tip:** Place downloaded PDF copies into the `files/` folder using the exact filenames shown
    below so the app can confirm their presence and link to them locally.
    """
)

st.subheader("Reference documents")

for name, links in DOC_LINKS.items():
    st.markdown(
        f"- **{name}** — external link: [{links['external']}]({links['external']}) | expected local copy: `{links['local']}`"
    )

st.subheader("Local availability summary")
st.dataframe(resolved_docs(), use_container_width=True)

st.caption(
    "Image cropping from the PDFs is not available in this environment; use the saved files on disk to extract diagrams if needed."
)
