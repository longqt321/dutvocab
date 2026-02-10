import streamlit as st
from sqlmodel import select

from core.db import get_session
from core.models import Card

st.header("⚡ Nạp Từ Mới")

with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        word = st.text_input("Từ vựng").strip()
        meaning = st.text_input("Nghĩa").strip()
    with col2:
        level = st.text_input("Cấp độ (VD: N3, C1)")
        note = st.text_area("Ghi chú")
        
    submitted = st.form_submit_button("Lưu ngay", use_container_width=True)
    
    if submitted and word and meaning:
        with get_session() as session:
            # Kiểm tra trùng lặp bằng ORM
            statement = select(Card).where(Card.word == word)
            existing = session.exec(statement).first()
            
            if existing:
                st.error(f"Từ '{word}' đã tồn tại!")
            else:
                # Tạo object mới
                new_card = Card(word=word, meaning=meaning, note=note, level=level)
                session.add(new_card)
                session.commit()
                st.success(f"Đã thêm: **{word}**")
