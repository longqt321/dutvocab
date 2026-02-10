import polars as pl
import streamlit as st
from sqlmodel import select

from core.db import engine, get_all_cards, get_session
from core.models import Card

st.header("📚 Kho Từ Vựng")

cards = get_all_cards()

if cards:
    data = [card.model_dump() for card in cards]     
    df = pl.DataFrame(data)
    
    # Cấu hình hiển thị bảng
    column_config = {
        "id": None,
        "word": st.column_config.TextColumn("Từ vựng", width="medium"),
        "meaning": st.column_config.TextColumn("Nghĩa", width="large"),
        "level": None,
        "repetitions": st.column_config.ProgressColumn("Độ thấm", min_value=0, max_value=20, format="%d"),
        # "interval": st.column_config.NumberColumn("Cách ngày", format="%.1f ngày"),
        "interval": None,
        "note" : None,
        "last_review" : None,
        "next_review": None,
        "easiness_factor": None, 
    }

    # Hiển thị bảng
    event = st.dataframe(df, width="stretch",
                         column_config=column_config,
                         hide_index=False,
                         on_select="rerun",
                         selection_mode="multi-row"
    )
    selected_rows = event.selection.rows

    if selected_rows:
        count = len(selected_rows)
        st.warning(f"Bạn đang chọn {count} từ để xóa.")
        
        if st.button(f"🗑️ Xóa {count} từ", type="primary", width="stretch"):
            
            # --- CÚ PHÁP POLARS ---
            # Lấy cột "id" tại các dòng được chọn (selected_rows)
            # Cú pháp: df[row_indices, col_name]
            ids_to_delete = df[selected_rows, "id"].to_list()
            
            with get_session() as session:
                for card_id in ids_to_delete:
                    card = session.get(Card, card_id)
                    if card:
                        session.delete(card)
                session.commit()
            
            st.toast(f"Đã xóa vĩnh viễn {count} từ!", icon="✨")
            st.rerun()
else:
    st.warning("Kho từ vựng đang trống. Hãy thêm từ mới!")
