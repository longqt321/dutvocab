import streamlit as st

from core.db import init_db

init_db()

st.title("DUTVocab")

pages = {
    "Dashboard": [
        st.Page("./pages/dashboard.py",title="Dashboard",default=True)
    ],
    "Main functions": [
        st.Page("./pages/library.py",title="Vocab list"),
        st.Page("./pages/add_word.py",title="Add new word"),            
    ],
    "Review": [
        st.Page("./pages/review.py",title="Review"),
    ]
}

st.set_page_config(page_title="DUTVocab",layout="wide")
pg = st.navigation(pages)
pg.run()

