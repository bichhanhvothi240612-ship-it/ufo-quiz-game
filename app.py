import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import uuid
import random
import string
import html

st.set_page_config(
    page_title="UFO TRI NÃO",
    page_icon="🛸",
    layout="centered"
)

# ---------- GIAO DIỆN ----------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at top, #243b72 0%, transparent 55%),
        linear-gradient(145deg, #080d25, #171044, #071b35);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    width: 100%;
    min-height: 46px;
    border-radius: 14px;
    font-weight: bold;
}
div[data-testid="stForm"] {
    border: 1px solid #5966a8;
    border-radius: 16px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center'>🛸 UFO TRI NÃO</h1>"
    "<p style='text-align:center'>🌌 Chinh phục vũ trụ tri thức!</p>",
    unsafe_allow_html=True
)

# ---------- KẾT NỐI SUPABASE ----------
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    db = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    st.error(
        "Chưa kết nối Supabase. Hãy thiết lập "
        "SUPABASE_URL và SUPABASE_KEY trong Streamlit Secrets."
    )
    st.stop()

# ---------- NHẠC NỀN ----------
music_url = st.secrets.get("MUSIC_URL", "")

if music_url:
    st.caption("🎵 Nhạc nền vũ trụ — nhấn Play để nghe.")
    st.audio(music_url, format="audio/mp3", loop=True)
else:
    st.caption("🎵 Có thể thêm đường dẫn nhạc MP3 trong Streamlit Secrets.")

# ---------- CÂU HỎI ----------
QUESTIONS = [
    {
        "q": "Hành tinh nào gần Mặt Trời nhất?",
        "options": ["Sao Kim", "Sao Thủy", "Trái Đất", "Sao Hỏa"],
        "answer": "Sao Thủy"
    },
    {
        "q": "Hành tinh nào được gọi là hành tinh đỏ?",
        "options": ["Sao Hỏa", "Sao Mộc", "Sao Thổ", "Sao Kim"],
        "answer": "Sao Hỏa"
    },
    {
        "q": "Mặt Trăng là gì?",
        "options": [
            "Một ngôi sao",
            "Một thiên hà",
            "Vệ tinh tự nhiên của Trái Đất",
            "Một hành tinh"
        ],
        "answer": "Vệ tinh tự nhiên của Trái Đất"
    },
    {
        "q": "Hành tinh lớn nhất Hệ Mặt Trời là gì?",
        "options": ["Trái Đất", "Sao Mộc", "Sao Hải Vương", "Sao Thủy"],
        "answer": "Sao Mộc"
    },
    {
        "q": "Mặt Trời thuộc loại thiên thể nào?",
        "options": ["Hành tinh", "Vệ tinh", "Ngôi sao", "Thiên thạch"],
        "answer": "Ngôi sao"
    },
    {
        "q": "Con người sống trên hành tinh nào?",
        "options": ["Sao Kim", "Sao Hỏa", "Trái Đất", "Sao Mộc"],
        "answer": "Trái Đất"
    },
    {
      "q": "Ai là người đầu tiên đặt chân lên Mặt Trăng?",
        "options": [
            "Neil Armstrong",
            "Albert Einstein",
            "Yuri Gagarin",
            "Galileo Galilei"
        ],
        "answer": "Neil Armstrong"
    },
    {
        "q": "Hành tinh nào nổi tiếng với hệ vành đai?",
        "options": ["Sao Thổ", "Sao Thủy", "Trái Đất", "Sao Hỏa"],
        "answer": "Sao Thổ"
    },
    {
        "q": "Ánh sáng Mặt Trời đến Trái Đất mất khoảng bao lâu?",
        "options": ["8 phút 20 giây", "1 giây", "1 giờ", "24 giờ"],
        "answer": "8 phút 20 giây"
    },
    {
        "q": "Thiên hà chứa Hệ Mặt Trời có tên là gì?",
        "options": ["Tiên Nữ", "Dải Ngân Hà", "Tam Giác", "Mây Magellan"],
        "answer": "Dải Ngân Hà"
    }
]

if "player_id" not in st.session_state:
    st.session_state.player_id = str(uuid.uuid4())

if "room_code" not in st.session_state:
    st.session_state.room_code = ""

if "is_host" not in st.session_state:
    st.session_state.is_host = False

player_id = st.session_state.player_id


def get_room(code):
    result = (
        db.table("game_rooms")
        .select("*")
        .eq("code", code)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None


def get_players(code):
    result = (
        db.table("game_players")
        .select("*")
        .eq("room_code", code)
        .order("score", desc=True)
        .execute()
    )
    return result.data


def create_room():
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    selected = random.sample(QUESTIONS, len(QUESTIONS))

    db.table("game_rooms").insert({
        "code": code,
        "host_id": player_id,
        "status": "lobby",
        "current_q": 0,
        "questions": selected
    }).execute()

    db.table("game_players").insert({
        "id": player_id,
        "room_code": code,
        "name": "Chủ phòng",
        "score": 0,
        "answers": {}
    }).execute()

    st.session_state.room_code = code
    st.session_state.is_host = True


# ---------- TẠO PHÒNG / THAM GIA ----------
if not st.session_state.room_code:
    st.subheader("🚀 Bắt đầu cuộc phiêu lưu")

    with st.form("create_form"):
        st.write("Tạo phòng mới để làm chủ trò chơi.")
        create_clicked = st.form_submit_button("🌟 TẠO PHÒNG")
        if create_clicked:
            create_room()
            st.rerun()

    st.divider()

    with st.form("join_form"):
        name = st.text_input("Tên người chơi", max_chars=20)
        code_input = st.text_input(
            "Mã phòng gồm 6 ký tự",
            max_chars=6
        ).strip().upper()

        join_clicked = st.form_submit_button("🛸 THAM GIA PHÒNG")

        if join_clicked:
            if not name.strip() or not code_input:
                st.warning("Nhập tên và mã phòng trước nha!")
            else:
                room = get_room(code_input)

                if not room:
                    st.error("Không tìm thấy phòng này.")
                elif room["status"] == "finished":
                    st.error("Phòng đã kết thúc.")
                else:
                    players = get_players(code_input)

                    if len(players) >= 100:
                        st.error("Phòng đã đủ 100 người!")
                    else:
                        db.table("game_players").insert({
                            "id": player_id,
                            "room_code": code_input,
                            "name": name.strip(),
                            "score": 0,
                            "answers": {}
                        }).execute()

                        st.session_state.room_code = code_input
                        st.session_state.is_host = False
                        st.rerun()

# ---------- PHÒNG CHƠI ----------
else:
    code = st.session_state.room_code
    room = get_room(code)

    if not room:
        st.error("Phòng không còn tồn tại.")
        if st.button("Quay lại"):
            st.session_state.room_code = ""
            st.rerun()
        st.stop()

    players = get_players(code)

    st.markdown(f"### 🔑 Mã phòng: `{code}`")
    st.write(f"👥 Người chơi: **{len(players)}/100**")
    st.caption("Gửi mã phòng cho bạn bè để cùng tham gia.")

    if room["status"] == "lobby":
        st.subheader("🌌 Phòng chờ")

        for p in players:
            st.write("👨‍🚀 " + html.escape(p["name"]))

        if st.session_state.is_host:
            if st.button("🚀 BẮT ĐẦU TRÒ CHƠI"):
                db.table("game_rooms").update({
                    "status": "playing",
                    "current_q": 0
                }).eq("code", code).execute()
                st.rerun()
        else:
            st.info("Đợi chủ phòng bắt đầu nha!")

    elif room["status"] == "playing":
        questions = room["questions"]
        q_index = room["current_q"]

        if q_index >= len(questions):
            st.info("Đang cập nhật kết quả...")
            st.stop()

        question = questions[q_index]
        answers = next(
            (p.get("answers") or {} for p in players if p["id"] == player_id),
            {}
        )

        st.progress((q_index + 1) / len(questions))
        st.subheader(f"🪐 Câu {q_index + 1}/{len(questions)}")
        st.markdown(f"### {question['q']}")

        answer_key = str(q_index)

        if answer_key in answers:
            st.success("✅ M đã trả lời câu này rồi!")
        else:
            with st.form(f"answer_form_{q_index}"):
                choice = st.radio(
                    "Chọn đáp án:",
                    question["options"]
                )
                submitted = st.form_submit_button("✨ GỬI ĐÁP ÁN")

                if submitted:
                    me = next(
                        (p for p in players if p["id"] == player_id),
                        None
                    )

                    if me and answer_key not in (me.get("answers") or {}):
                        new_answers = dict(me.get("answers") or {})
                        new_answers[answer_key] = choice

                        new_score = me["score"]
                        if choice == question["answer"]:
                            new_score += 1

                        db.table("game_players").update({
                            "answers": new_answers,
                            "score": new_score
                        }).eq("id", player_id).execute()

                    st.rerun()

        answered_count = sum(
            1 for p in players
            if answer_key in (p.get("answers") or {})
        )

        st.write(f"📊 Đã trả lời: {answered_count}/{len(players)} người")

        if st.session_state.is_host:
            st.divider()
            if st.button("➡️ CÂU TIẾP THEO"):
                if q_index + 1 < len(questions):
                    db.table("game_rooms").update({
                        "current_q": q_index + 1
                    }).eq("code", code).execute()
                else:
                    db.table("game_rooms").update({
                        "status": "finished"
                    }).eq("code", code).execute()
                st.rerun()

        if st.button("🔄 Cập nhật màn hình"):
        
