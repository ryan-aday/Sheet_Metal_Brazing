import pandas as pd
import streamlit as st

from app_data import BRAZING_QUALIFICATION, BRAZING_REQUIREMENTS

st.title("Brazing Requirements")

st.markdown(
    """
    Consolidated brazing criteria reflecting the MIL brazing guidance. Tailor the notes to your
    exact joint design, fixture strategy, and alloy family.
    """
)

st.subheader("Material and brazing alloy requirements")
st.table(pd.DataFrame(BRAZING_REQUIREMENTS))

st.subheader("Brazing alloys, test specimens, and loads")
st.dataframe(pd.DataFrame(BRAZING_QUALIFICATION), use_container_width=True)
