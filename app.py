
import streamlit as st
import random
import os
import base64

st.set_page_config(
    page_title="UFO Khảo Bài",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CÂU HỎI ----------
QUESTION_BANK = [
    {
        "subject": "Toán",
        "q": "Nghiệm của phương trình 2x + 4 = 10 là gì?",
        "options": ["x = 2", "x = 3", "x = 4", "x = 7"],
        "answer": 1,
        "explain": "2x = 10 - 4 = 6 nên x = 3."
    },
    {
        "subject": "Toán",
        "q": "Căn bậc hai số học của 81 là bao nhiêu?",
        "options": ["7", "8", "9", "10"],
        "answer": 2,
        "explain": "Vì 9² = 81 nên căn bậc hai số học của 81 là 9."
    },
    {
        "subject": "Toán",
        "q": "Nếu x + y = 10 và x = 4 thì y bằng bao nhiêu?",
        "options": ["4", "5", "6", "14"],
        "answer": 2,
        "explain": "Thay x = 4 vào x + y = 10, ta được y = 6."
    },
    {
        "subject": "Tiếng Anh",
        "q": "Quá khứ của động từ 'go' là gì?",
        "options": ["Goed", "Gone", "Went", "Going"],
        "answer": 2,
        "explain": "'Go' là động từ bất quy tắc, dạng quá khứ là 'went'."
    },
    {
        "subject": "Tiếng Anh",
        "q": "Từ nào có nghĩa là 'xinh đẹp'?",
        "options": ["Beautiful", "Difficult", "Dangerous", "Careful"],
        "answer": 0,
        "explain": "'Beautiful' có nghĩa là xinh đẹp."
    },
    {
        "subject": "Khoa học",
        "q": "Hành tinh nào chúng ta đang sinh sống?",
        "options": ["Sao Hỏa", "Trái Đất", "Sao Kim", "Sao Mộc"],
        "answer": 1,
        "explain": "Trái Đất là hành tinh nơi con người đang sinh sống."
    },
    {
        "subject": "Khoa học",
        "q": "Nước đóng băng ở khoảng bao nhiêu độ C?",
        "options": ["0°C", "10°C", "50°C", "100°C"],
        "answer": 0,
        "explain": "Ở áp suất khí quyển tiêu chuẩn, nước tinh khiết đóng băng ở 0°C."
    },
    {
        "subject": "Địa lý",
        "q": "Việt Nam thuộc châu lục nào?",
        "options": ["Châu Âu", "Châu Mỹ", "Châu Á", "Châu Phi"],
        "answer": 2,
        "explain": "Việt Nam nằm ở khu vực Đông Nam Á, thuộc châu Á."
    },
    {
        "subject": "Lịch sử",
        "q": "Ngày Quốc khánh Việt Nam là ngày nào?",
        "options": ["30/4", "2/9", "19/5", "20/11"],
        "answer": 1,
        "explain": "Ngày Quốc khánh Việt Nam là ngày 2 tháng 9."
    },
    {
        "subject": "Khoa học",
        "q": "Cơ quan nào bơm máu đi khắp cơ thể?",
        "options": ["Phổi", "Dạ dày", "Tim", "Gan"],
        "answer": 2,
        "explain": "Tim co bóp để bơm máu đi khắp cơ thể."
    },
]

# ---------- TRẠNG THÁI GAME ----------
if "game_questions" not in st.session_state:
    st.session_state.game_questions = random.sample(
        QUESTION_BANK, len(QUESTION_BANK)
    )
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = None
    st.session_state.finished = False
    st.session_state.started = False

def restart_game():
    st.session_state.game_questions = random.sample(
        QUESTION_BANK, len(QUESTION_BANK)
    )
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = None
    st.session_state.finished = False
    st.session_state.started = True

def choose_answer(index):
    if st.session_state.answered is None:
        st.session_state.answered = index
        question = st.session_state.game_questions[
            st.session_state.current
        ]
        if index == question["answer"]:
            st.session_state.score += 1

def next_question():
    st.session_state.current += 1
    st.session_state.answered = None
    if st.session_state.current >= len(st.session_state.game_questions):
        st.session_state.finished = True

# ---------- HÌNH NỀN ----------
background_css = """
.stApp {
    background:
        radial-gradient(circle at 12% 18%, #ffffffb0 0 2px, transparent 3px),
        radial-gradient(circle at 80% 24%, #fff8 0 2px, transparent 4px),
        linear-gradient(180deg, #55c9ff 0%, #b9eaff 44%, #ffe4ba 100%);
    background-size: 190px 150px, 230px 180px, cover;
    color: #24365b;
}
"""

# Nếu có ảnh background.png trong repository, dùng ảnh đó làm nền.
if os.path.exists("background.png"):
    with open("background.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    background_css = f"""
    .stApp {{
        background-image:
            linear-gradient(180deg, #10264a22, #10264a33),
            url("data:image/png;base64,{image_data}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

st.markdown(
    f"""
    <style>
    {background_css}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 1050px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }}

    .hero {{
        text-align: center;
        padding: 24px 16px;
        border: 2px solid #ffffffcc;
        border-radius: 28px;
        background: linear-gradient(135deg, #ffffffd9, #e8f8ffd9);
        box-shadow: 0 12px 35px #245b8b30;
        animation: floaty 3s ease-in-out infinite;
        margin-bottom: 20px;
    }}

    .hero h1 {{
        color: #3949ab;
        font-size: clamp(30px, 5vw, 48px);
        margin: 0;
        font-weight: 900;
    }}

    .hero p {{
        color: #49658b;
        font-size: 17px;
        margin: 8px 0 0;
    }}

    .ufo {{
        font-size: 54px;
        display: inline-block;
        animation: fly 3s ease-in-out infinite;
    }}

    .game-card {{
        background: #ffffffed;
        border: 2px solid #ffffff;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 12px 30px #214b6b25;
        color: #24365b;
        margin: 10px 0 16px;
    }}

    .tag {{
        display: inline-block;
        padding: 6px 13px;
        background: #e4e9ff;
        color: #4549a6;
        border-radius: 30px;
        font-weight: 800;
        font-size: 13px;
    }}

    .question {{
        font-size: clamp(20px, 3vw, 28px);
        font-weight: 800;
        line-height: 1.5;
        color: #263b67;
        margin-top: 14px;
    }}

    div.stButton > button {{
        width: 100%;
        min-height: 52px;
        border-radius: 16px;
        border: 2px solid #d9e6ff;
        background: #ffffff;
        color: #30456d;
        font-size: 16px;
        font-weight: 700;
        transition: all .18s ease;
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px);
        border-color: #858bff;
        background: #f0f3ff;
        color: #343c9a;
        box-shadow: 0 6px 15px #5668a622;
    }}

    .feedback {{
        border-radius: 16px;
        padding: 15px 18px;
        background: #effaf3;
        border: 2px solid #bde8cb;
        color: #245b3a;
        margin: 12px 0;
    }}

    @keyframes floaty {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}

    @keyframes fly {{
        0%, 100% {{ transform: translateY(0) rotate(-3deg); }}
        50% {{ transform: translateY(-10px) rotate(3deg); }}
    }}

    @media (max-width: 600px) {{
        .block-container {{ padding: 1rem .7rem; }}
        .hero {{ padding: 20px 10px; }}
        .game-card {{ padding: 15px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- TIÊU ĐỀ ----------
st.markdown(
    """
    <div class="hero">
        <div class="ufo">🛸</div>
        <h1>UFO KHẢO BÀI</h1>
        <p>👽 Người ngoài hành tinh đến thử thách kiến thức của bạn!</p>
        <p>🏫 Thành phố học đường • 🚀 Học vui • ⭐ Tích điểm</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- MÀN HÌNH BẮT ĐẦU ----------
if not st.session_state.started:
    st.markdown(
        """
        <div class="game-card">
            <h2>🌈 Sẵn sàng lên phi thuyền chưa?</h2>
            <p>Trả lời 10 câu hỏi để trở thành nhà thám hiểm vũ trụ!</p>
            <p>⭐ Mỗi câu đúng được 1 điểm.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.button(
        "🚀 BẮT ĐẦU KHẢO BÀI",
        type="primary",
        on_click=restart_game,
        use_container_width=True
    )

# ---------- ĐANG CHƠI ----------
elif not st.session_state.finished:
    i = st.session_state.current
    question = st.session_state.game_questions[i]
    total = len(st.session_state.game_questions)

    st.progress(i / total, text=f"🚀 Tiến độ: câu {i + 1}/{total}")

    a, b = st.columns(2)
    a.metric("⭐ Điểm của bạn", st.session_state.score)
    b.metric("🛸 Câu hỏi", f"{i + 1}/{total}")

    st.markdown(
        f"""
        <div class="game-card">
            <span class="tag">📚 {question["subject"]}</span>
            <div class="question">
                Câu {i + 1}: {question["q"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### 👇 Chọn đáp án của bạn")

    for start in range(0, len(question["options"]), 2):
        cols = st.columns(2)
        for offset in range(2):
            idx = start + offset
            if idx < len(question["options"]):
                label = question["options"][idx]
                cols[offset].button(
                    f"{chr(65 + idx)}. {label}",
                    key=f"q{i}_option{idx}",
                    on_click=choose_answer,
                    args=(idx,),
                    disabled=st.session_state.answered is not None
                )

    if st.session_state.answered is not None:
        if st.session_state.answered == question["answer"]:
            st.success("🎉 Chính xác! Bạn nhận được 1 điểm.")
            st.balloons()
        else:
            correct = question["options"][question["answer"]]
            st.error(f"👽 Chưa đúng rồi! Đáp án đúng là: {correct}")

        st.info(f"💡 Giải thích: {question['explain']}")

        if i + 1 < total:
            st.button(
                "➡️ Câu tiếp theo",
                type="primary",
                on_click=next_question,
                use_container_width=True
            )
        else:
            st.button(
                "🏁 Xem kết quả",
                type="primary",
                on_click=next_question,
                use_container_width=True
            )

# ---------- KẾT QUẢ ----------
else:
    score = st.session_state.score
    total = len(st.session_state.game_questions)
    percent = score / total * 100

    st.balloons()
    st.markdown(
        f"""
        <div class="hero">
            <div class="ufo">🏆</div>
            <h1>HOÀN THÀNH NHIỆM VỤ!</h1>
            <p>Bạn đã trở về Trái Đất an toàn!</p>
            <h2 style="color:#3949ab">{score}/{total} điểm</h2>
            <p>Độ chính xác: {percent:.0f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if score == total:
        st.success("🌟 Tuyệt vời! Bạn là siêu sao tri thức vũ trụ!")
    elif score >= 7:
        st.success("🚀 Rất tốt! Bạn là nhà thám hiểm xuất sắc!")
    elif score >= 5:
        st.info("👏 Khá lắm! Ôn tập thêm để chinh phục vũ trụ nhé!")
    else:
        st.warning("💪 Đừng nản lòng! Chơi lại để luyện tập thêm nhé!")

    st.button(
        "🔄 CHƠI LẠI",
        type="primary",
        on_click=restart_game,
        use_container_width=True
    )

st.markdown(
    """
    <p style="text-align:center;color:#344d70;font-weight:700;margin-top:25px">
        🛸 UFO Khảo Bài • Học tập vui vẻ mỗi ngày 🌈
    </p>
    """,
    unsafe_allow_html=True
)


