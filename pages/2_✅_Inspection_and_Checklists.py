import pandas as pd
import streamlit as st

from app_data import INSPECTION_CHECKLIST, MATERIAL_THICKNESS_LIMITS, WELDING_LIMITATIONS

st.title("Inspection & Procedure Limits")

st.subheader("Inspection checklist")
st.dataframe(pd.DataFrame(INSPECTION_CHECKLIST), use_container_width=True)

st.subheader("Welding procedure limitations")
st.dataframe(pd.DataFrame(WELDING_LIMITATIONS), use_container_width=True)

st.subheader("Material thickness limits by process")
st.table(pd.DataFrame(MATERIAL_THICKNESS_LIMITS))
