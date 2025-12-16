import pandas as pd
import streamlit as st

from app_data import (
    ASSEMBLY_TESTS,
    FILLER_COMBINATIONS,
    PERFORMANCE_EVAL,
    QUALIFICATION_LIMITS,
)

st.title("Procedure & Performance Qualification")

st.markdown(
    "Use these tables to plan qualification coupons and acceptance reviews. Align selections with the governing MIL standards and drawing notes."
)

st.subheader("Filler metal and process combinations")
st.dataframe(pd.DataFrame(FILLER_COMBINATIONS), use_container_width=True)

st.subheader("Qualification test limitations")
st.table(pd.DataFrame(QUALIFICATION_LIMITS))

st.subheader("Performance qualification evaluation")
st.table(pd.DataFrame(PERFORMANCE_EVAL))

st.subheader("Welding procedure assembly test requirements")
st.table(pd.DataFrame(ASSEMBLY_TESTS))
