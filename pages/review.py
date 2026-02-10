import streamlit as st

from core.db import get_due_cards, get_session
from core.models import Card
from core.srs import update_card

st.header("🧠 Phòng Luyện Tập (SRS)")

# Lấy danh sách cần học (Lưu vào session_state để không bị mất khi reload trang)
if 'review_queue' not in st.session_state:
    st.session_state.review_queue = get_due_cards()

queue = st.session_state.review_queue

if not queue:
    st.success("🎉 Tuyệt vời! Bạn đã hoàn thành bài tập hôm nay.")
else:
    # Lấy từ đầu tiên trong hàng đợi
    current_card = queue[0]
    
    # Giao diện thẻ Flashcard
    with st.container(border=True):
        st.subheader(current_card.word)
        st.caption(f"Tag: {current_card.level or 'General'}")
        
        # Trạng thái lật thẻ
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
            
        if st.session_state.show_answer:
            st.divider()
            st.markdown(f"**Nghĩa:** {current_card.meaning}")
            if current_card.note:
                st.info(f"📝 {current_card.note}")
            
            st.write("---")
            st.write("Bạn nhớ từ này thế nào?")
            
            # Các nút đánh giá
            c1, c2, c3 = st.columns(3)
            
            def process_review(stupidity):
                with get_session() as session:
                    # Cần query lại object từ session hiện tại để update
                    card_to_update = session.get(Card, current_card.id)
                    update_card(card_to_update, stupidity=stupidity)
                    session.add(card_to_update)
                    session.commit()
                
                # Xóa khỏi hàng đợi và ẩn đáp án
                st.session_state.review_queue.pop(0)
                st.session_state.show_answer = False
                st.rerun()

            with c1: st.button("😭 Quên hẳn (0đ)", on_click=process_review, args=(5,), use_container_width=True)
            with c2: st.button("🤔 Hơi nhớ (3đ)", on_click=process_review, args=(3,), use_container_width=True)
            with c3: st.button("😎 Quá dễ (5đ)", on_click=process_review, args=(0,), use_container_width=True)
            
        else:
            st.button("Xem đáp án", on_click=lambda: st.session_state.update(show_answer=True), use_container_width=True)
