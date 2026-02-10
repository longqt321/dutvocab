import streamlit as st

from core.db import get_all_cards, get_due_cards

st.header("📊 Tổng quan tiến độ")

total_cards = len(get_all_cards())
due_cards = len(get_due_cards())

col1, col2, col3 = st.columns(3)
col1.metric("Tổng vốn từ", f"{total_cards} từ")
col2.metric("Cần ôn hôm nay", f"{due_cards} từ", delta_color="inverse")
col3.metric("Trạng thái", "Sẵn sàng" if due_cards > 0 else "Thư giãn")

st.info("👈 Chọn chức năng bên trái để bắt đầu.")
