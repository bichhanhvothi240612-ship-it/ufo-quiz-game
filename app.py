st.markdown(f"<h3 style='text-align: center;'>Tổng điểm: {st.session_state.score}/{len(questions)}</h3>", unsafe_allow_html=True)
    
    if st.session_state.score == 3:
        st.balloons()
        st.success("🎉 Tuyệt vời! Bạn là nhà thám hiểm vũ trụ xuất sắc!")
    elif st.session_state.score == 2:
        st.info("👏 Khá tốt! Cố gắng hơn nhé!")
    else:
        st.warning("💪 Đừng nản lòng, thử lại lần nữa nhé!")
    
    if st.button("Chơi lại 🔄"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
