import streamlit as st

st.set_page_config(
    page_title="UFO Quiz",
    page_icon="🛸",
    layout="centered"
)

questions = [
    {
        "question": "🪐 Hành tinh nào gần Mặt Trời nhất?",
        "options": ["Trái Đất", "Sao Thủy", "Sao Hỏa", "Sao Mộc"],
        "answer": "Sao Thủy"
    },
    {
        "question": "🌍 Hành tinh nào được gọi là hành tinh xanh?",
        "options": ["Sao Kim", "Sao Thổ", "Trái Đất", "Sao Hỏa"],
        "answer": "Trái Đất"
    },
    {
        "question": "🚀 Ai là người đầu tiên đặt chân lên Mặt Trăng?",
        "options": [
            "Yuri Gagarin",
            "Neil Armstrong",
            "Albert Einstein",
            "Elon Musk"
        ],
        "answer": "Neil Armstrong"
    }
]

if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.finished = False

st.title("🛸 UFO QUIZ")
st.subheader("🌌 Thử thách kiến thức vũ trụ")
st.write("Trả lời 3 câu hỏi để trở thành nhà thám hiểm vũ trụ!")

if not st.session_state.finished:
    q_index = st.session_state.current_q
    question = questions[q_index]

    st.progress(q_index / len(questions))
    st.write(f"### Câu {q_index + 1}/{len(questions)}")
    st.write(f"**{question['question']}**")

    choice = st.radio(
        "Chọn đáp án của m:",
        question["options"],
        key=f"choice_{q_index}",
        disabled=st.session_state.answered
    )

    if not st.session_state.answered:
        if st.button("🚀 Xác nhận đáp án", use_container_width=True):
            st.session_state.answered = True

            if choice == question["answer"]:
                st.session_state.score += 1
                st.success("🎉 Chính xác! Giỏi quá!")
            else:
                st.error(
                    f"Chưa đúng rồi! Đáp án là: {question['answer']}"
                )

            st.rerun()

    else:
        st.write(
            f"Điểm hiện tại: {st.session_state.score}/{len(questions)}"
        )

        if st.button("➡️ Câu tiếp theo", use_container_width=True):
            if q_index + 1 < len(questions):
                st.session_state.current_q += 1
                st.session_state.answered = False
            else:
                st.session_state.finished = True

            st.rerun()

else:
    st.balloons()
    st.markdown(
        f"<h2 style='text-align:center'>"
        f"🏆 Kết quả: {st.session_state.score}/{len(questions)}"
        f"</h2>",
        unsafe_allow_html=True
    )

    if st.session_state.score == 3:
        st.success("🌟 Tuyệt vời! M là nhà thám hiểm vũ trụ xuất sắc!")
    elif st.session_state.score == 2:
        st.info("👏 Khá tốt! M cố gắng thêm chút nữa nha!")
    else:
        st.warning("💪 Đừng nản lòng, thử lại lần nữa nhé!")

    if st.button("🔄 Chơi lại", use_container_width=True):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.finished = False
        st.rerun()
