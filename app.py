
import random
import string
import streamlit as st
import streamlit.components.v1 as components

from supabase import create_client

st.set_page_config(
    page_title="UFO TRÍ NÃO",
    page_icon="🛸",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #c9f2ff, #fce0f2, #e4ffd9);
}
h1 {
    color: #7550c8;
    text-align: center;
    font-weight: 900;
}
.block-container {
    max-width: 1000px;
}
.stButton button {
    background: #8967e8;
    color: white;
    border-radius: 14px;
    font-weight: bold;
    border: 2px solid white;
    min-height: 44px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛸 UFO TRÍ NÃO")
st.markdown(
    "<h3 style='text-align:center'>👽 Ai là cao thủ kiến thức?</h3>",
    unsafe_allow_html=True
)

# Nhạc nền tổng hợp
components.html("""
<button id="music" style="padding:10px 18px;border:0;
border-radius:12px;background:#8065d7;color:white;font-weight:bold">
🎵 Bật / tắt nhạc nền
</button>
<script>
let audio = null, timer = null, on = false, i = 0;
let notes = [523,659,784,659,587,698,880,698];
document.getElementById("music").onclick = async function() {
    if (!audio) audio = new AudioContext();
    await audio.resume();
    on = !on;
    if (on) {
        timer = setInterval(() => {
            let osc = audio.createOscillator();
            let gain = audio.createGain();
            osc.frequency.value = notes[i++ % notes.length];
            gain.gain.value = 0.025;
            osc.connect(gain);
            gain.connect(audio.destination);
            osc.start();
            osc.stop(audio.currentTime + 0.15);
        }, 250);
        this.innerText = "🔇 Tắt nhạc nền";
    } else {
        clearInterval(timer);
        this.innerText = "🎵 Bật nhạc nền";
    }
};
</script>
""", height=60)

QUESTIONS = [
    {
        "q": "Giải phương trình x² - 5x + 6 = 0.",
        "a": ["x = 2 hoặc x = 3", "x = 1", "x = 6", "Vô nghiệm"],
        "correct": 0,
        "explain": "(x - 2)(x - 3) = 0 nên x = 2 hoặc x = 3."
    },
    {
        "q": "Theo Vi-ét, tổng hai nghiệm của x² - 7x + 10 = 0 là?",
        "a": ["10", "-7", "7", "-10"],
        "correct": 2,
        "explain": "Tổng hai nghiệm bằng -b/a = 7."
    },
    {
        "q": "Tam giác vuông có hai cạnh góc vuông 6 và 8. Cạnh huyền là?",
        "a": ["9", "10", "12", "14"],
        "correct": 1,
        "explain": "Cạnh huyền = √(6² + 8²) = 10."
    },
    {
        "q": "She has lived here ___ 2020.",
        "a": ["for", "since", "during", "at"],
        "correct": 1,
        "explain": "Since đi với mốc thời gian."
    },
    {
        "q": "Đơn vị đo cường độ dòng điện là gì?",
        "a": ["Vôn", "Oát", "Ampe", "Jun"],
        "correct": 2,
        "explain": "Cường độ dòng điện đo bằng ampe (A)."
    },
    {
        "q": "Nếu 20% của một số bằng 18, số đó là?",
        "a": ["36", "72", "90", "100"],
        "correct": 2,
        "explain": "18 ÷ 0,2 = 90."
    },
    {
        "q": "Thủ đô Nhật Bản là thành phố nào?",
        "a": ["Kyoto", "Osaka", "Tokyo", "Nagoya"],
        "correct": 2,
        "explain": "Thủ đô Nhật Bản là Tokyo."
    },
    {
        "q": "Một giờ có bao nhiêu phút?",
        "a": ["30", "45", "60", "100"],
        "correct": 2,
        "explain": "Một giờ có 60 phút."
    },
    {
        "q": "Nếu x - y = 4 và x + y = 10 thì x bằng?",
        "a": ["3", "5", "7", "14"],
        "correct": 2,
        "explain": "Cộng hai phương trình: 2x = 14, x = 7."
    },
    {
        "q": "Từ trái nghĩa với generous là gì?",
        "a": ["Kind", "Helpful", "Selfish", "Friendly"],
        "correct": 2,
        "explain": "Generous là hào phóng; selfish là ích kỷ."
    }
]

# Kết nối cơ sở dữ liệu
try:
    db = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_ANON_KEY"]
    )
except Exception:
    st.error(
        "Bạn cần cài Supabase và thêm SUPABASE_URL, "
        "SUPABASE_ANON_KEY trong Streamlit Secrets."
    )
    st.stop()

if "player_id" not in st.session_state:
    st.session_state.player_id = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=12)
    )

if "room" not in st.session_state:
    st.session_state.room = ""

def get_room(code):
    data = db.table("rooms").select("*").eq(
        "room_code", code
    ).execute().data
    return data[0] if data else None

def get_players(code):
    data = db.table("players").select("*").eq(
        "room_code", code
    ).execute().data
    return sorted(data, key=lambda p: -p["score"])

def create_room():
    code = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    db.table("rooms").insert({
        "room_code": code,
        "status": "waiting",
        "q_index": 0
    }).execute()
    st.session_state.room = code
    st.session_state.role = "host"
    st.rerun()

def join_room(code, name):
    code = code.strip().upper()
    if not name.strip():
        st.error("Hãy nhập tên của bạn.")
        return

    room = get_room(code)
    if not room:
        st.error("Mã phòng không tồn tại.")
        return

    players = get_players(code)
    old = [
        p for p in players
        if p["player_id"] == st.session_state.player_id
    ]

    if not old and len(players) >= 100:
        st.error("Phòng đã đủ 100 người chơi.")
        return

    db.table("players").upsert({
        "room_code": code,
        "player_id": st.session_state.player_id,
        "name": name.strip()[:24],
        "score": 0,
        "answered_q": -1
    }).execute()

    st.session_state.room = code
    st.session_state.role = "player"
    st.rerun()

if not st.session_state.room:
    tab1, tab2 = st.tabs(["🧑‍🏫 Tạo phòng", "🧑‍🎓 Vào phòng"])

    with tab1:
        st.write("Tạo phòng và chia sẻ mã cho bạn bè.")
        if st.button("🚀 TẠO PHÒNG MỚI"):
            create_room()

    with tab2:
        code = st.text_input("Mã phòng").upper()
        name = st.text_input("Tên người chơi")
        if st.button("🛸 VÀO PHÒNG"):
            join_room(code, name)

else:
    code = st.session_state.room
    st_autorefresh(interval=4000, key="refresh")

    room = get_room(code)
    if not room:
        st.error("Không tìm thấy phòng.")
        st.stop()

    players = get_players(code)
    me = next(
        (p for p in players
         if p["player_id"] == st.session_state.player_id),
        None
    )

    st.subheader(f"🏙️ Mã phòng: {code}")
    col1, col2 = st.columns(2)
    col1.metric("👥 Người chơi", f"{len(players)}/100")
    col2.metric("⭐ Điểm của bạn", me["score"] if me else 0)

    if room["status"] == "waiting":
        st.info("Đang chờ quản trò bắt đầu.")

        if st.session_state.role == "host":
            if st.button("▶️ BẮT ĐẦU"):
                db.table("rooms").update({
                    "status": "playing",
                    "q_index": 0
                }).eq("room_code", code).execute()
                st.rerun()

    elif room["status"] == "playing":
        qi = room["q_index"]

        if qi >= len(QUESTIONS):
            if st.session_state.role == "host":
                db.table("rooms").update({
                    "status": "finished"
                }).eq("room_code", code).execute()
                st.rerun()
        else:
            q = QUESTIONS[qi]
            st.markdown(f"## 👽 Câu {qi + 1}")
            st.write(q["q"])

            if st.session_state.role == "host":
                answered = sum(
                    p["answered_q"] == qi for p in players
                )
                st.write(f"Đã trả lời: {answered}/{len(players)}")

                if st.button("➡️ CÂU TIẾP THEO"):
                    db.table("rooms").update({
                        "q_index": qi + 1
                    }).eq("room_code", code).execute()
                    st.rerun()

            elif me and me["answered_q"] == qi:
                st.success("Bạn đã trả lời. Chờ câu tiếp theo nhé!")

            else:
                answer = st.radio("Chọn đáp án:", q["a"])

                if st.button("📨 GỬI ĐÁP ÁN"):
                    fresh = db.table("players").select("*").eq(
                        "room_code", code
                    ).eq(
                        "player_id", st.session_state.player_id
                    ).execute().data

                    if fresh and fresh[0]["answered_q"] != qi:
                        correct = q["a"].index(answer) == q["correct"]
                        score = fresh[0]["score"] + (
                            10 if correct else 0
                        )

                        db.table("players").update({
                            "score": score,
                            "answered_q": qi
                        }).eq(
                            "room_code", code
                        ).eq(
                            "player_id", st.session_state.player_id
                        ).execute()

                        if correct:
                            st.success("🎉 Chính xác! +10 điểm.")
                        else:
                            st.error("Chưa đúng: " + q["explain"])

                        st.rerun()

    elif room["status"] == "finished":
        st.balloons()
        st.success("🏆 Trò chơi kết thúc!")

    st.divider()
    st.subheader("🏆 BẢNG XẾP HẠNG")

    for i, p in enumerate(players[:100], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "👽"
        st.write(f"{medal} {i}. **{p['name']}** — {p['score']} điểm")

    if st.button("🚪 RỜI PHÒNG"):
        st.session_state.room = ""
        st.rerun()
