import polars as pl
import streamlit as st
from sqlmodel import select

from core.db import add_card, get_session, import_from_csv
from core.models import Card

st.header("⚡ Nạp Từ Mới")

tab1,tab2 = st.tabs(["Manual import","Import from CSV"])

with tab1:
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            word = st.text_input("Từ vựng").strip()
            meaning = st.text_input("Nghĩa").strip()
        with col2:
            level = st.text_input("Cấp độ (VD: N3, C1)")
            note = st.text_area("Ghi chú")
            
        submitted = st.form_submit_button("Lưu ngay", width="stretch")
        
        if submitted:
            if not word or not meaning:
                st.warning("Word or Meaning is missing")
            else:
                success,message = add_card(word,meaning,level,note)
                if success:
                    st.success(message)
                else:
                    st.error(message)
with tab2:
    st.info("File csv need `word`,`meaning` columns. `level` and `note` are optional")
    uploaded_file = st.file_uploader("Choose csv file",type=["csv"])

    if uploaded_file is not None:
        try:
            df = pl.read_csv(uploaded_file)
            required_cols = {'word','meaning'}
            if not required_cols.issubset(set(df.columns)):
                st.error(f"Missing columns: {required_cols - set(df.columns)}")
            else:
                if st.button("Import",type="primary"):
                    with st.spinner("Uploading..."):
                        result = import_from_csv(df)

                    st.success(f"Imported: {result["success_count"]}")
                    if result["skip_count"] > 0:
                        st.warning(f"Skipped: {result["skip_count"]}")
                    if result["errors"]:
                        with st.expander("Error details"):
                            st.write(result["errors"])
        except Exception as e:
            st.error(f"Error when reading file: {e}")
