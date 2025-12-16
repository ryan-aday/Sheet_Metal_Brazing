import pandas as pd
import streamlit as st

from app_data import (
    BASE_FILLER_MATERIALS,
    DOC_LINKS,
    GD_T_CALL_OUTS,
    download_references,
    load_milstd248_tables,
    resolved_docs,
)

st.title("Materials, Fillers, and Drawings")

st.markdown(
    """
    Browse common base and filler materials paired with welding or brazing processes.
    Values are formatted as quick-reference prompts based on the MIL guidance; confirm details in
    the source specifications using the provided links.
    """
)

st.subheader("Base and filler materials")
st.dataframe(pd.DataFrame(BASE_FILLER_MATERIALS), use_container_width=True)

st.subheader("MIL-SD-248D extracted tables and footnotes")
extracted = load_milstd248_tables()
if extracted["tables"]:
    for idx, table in enumerate(extracted["tables"], start=1):
        st.markdown(f"**Table {idx}**")
        st.code("\n".join(table))
else:
    st.info(
        "No tables were loaded. Add a local copy of `MIL-SD-248D.pdf` inside the `files/` "
        "folder to automatically extract tables and footnotes for the material listings."
    )

if extracted["footnotes"]:
    st.markdown("**Table Notes / Footnotes**")
    for note in extracted["footnotes"]:
        st.write(note)

st.subheader("Drawing callouts to watch")
st.table(pd.DataFrame(GD_T_CALL_OUTS))

st.subheader("Document library")

for name, links in DOC_LINKS.items():
    st.markdown(
        f"- **{name}** — [external link]({links['external']}) · expected local copy: `{links['local']}`"
    )

st.markdown("**Local file check**")
st.dataframe(pd.DataFrame(resolved_docs()), use_container_width=True)

if st.button("Attempt to download missing PDFs"):
    with st.spinner("Downloading..."):
        results = download_references()
    for title, ok, message in results:
        icon = "✅" if ok else "⚠️"
        st.write(f"{icon} {title}: {message}")
    st.dataframe(pd.DataFrame(resolved_docs()), use_container_width=True)
