

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="UFO Khảo Bài",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #d9f4ff, #fce4ff, #fff2d6);
    }
    .block-container {
        padding: 1rem 0.5rem 0 !important;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: "Trebuchet MS", Arial, sans-serif;
    background: #dff6ff;
    color: #27354b;
}
button { font-family: inherit; cursor: pointer; }
.game { max-width: 1100px; margin: auto; padding: 10px; }
.topbar {
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 8px; margin-bottom: 10px;
}
.logo {
    font-size: clamp(19px, 4vw, 28px); font-weight: 900;
    color: #7652c9; text-shadow: 2px 2px #fff;
}
.stat {
    background: white; border: 2px solid #e7ddff;
    border-radius: 14px; padding: 8px 13px; font-weight: bold;
    box-shadow: 0 4px 0 #d7c8f5;
}
.scene {
    height: 440px; position: relative; overflow: hidden;
    border: 4px solid white; border-radius: 22px;
    background: linear-gradient(#b9eaff 0%, #e5f8ff 54%, #a5d9b6 55%, #80c5a2 100%);
    box-shadow: 0 8px 0 #c9b9ee, 0 12px 25px #8b79b344;
}
.sun {
    position:absolute; width:65px;height:65px;border-radius:50%;
    background:#ffe88b; right:8%;top:20px;
    box-shadow:0 0 35px #fff3a8;
}
.cloud {
    position:absolute;top:45px;left:15%;font-size:42px;
    opacity:.85; animation: cloudmove 18s linear infinite;
}
.cloud.two {top:90px;left:62%;animation-delay:-8s;font-size:32px;}
@keyframes cloudmove {0%{transform:translateX(-40px)}50%{transform:translateX(35px)}100%{transform:translateX(-40px)}}
.buildings {
    position:absolute;left:0;right:0;bottom:155px;height:140px;
    display:flex;align-items:flex-end;justify-content:space-around;gap:5px;
}
.shop {
    height:100%;width:19%;position:relative;border:3px solid #fff;
    border-radius:8px 8px 0 0;box-shadow:inset 0 -8px #0000000b;
    text-align:center;font-size:clamp(10px,2vw,15px);font-weight:900;
    padding-top:12px;color:#5b4264;
}
.shop:before {
    content:"";position:absolute;left:-4px;right:-4px;top:35px;height:15px;
    background:repeating-linear-gradient(90deg,#ffcf7b 0 22px,#fff1cb 22px 44px);
    border:2px solid white;
}
.shop:after {
    content:"";position:absolute;left:20%;right:20%;bottom:0;height:48px;
    background:linear-gradient(90deg,#6da9d4 0 45%,#fff 45% 53%,#6da9d4 53%);
    border:3px solid #fff;border-bottom:0;border-radius:5px 5px 0 0;
}
.shop span {position:relative;z-index:1;background:#fff8;padding:3px;border-radius:5px;}
.s1{background:#ffd9a6}.s2{background:#ffb9cb}.s3{background:#c5edc8}.s4{background:#ffe4a6}.s5{background:#cbbdff}
.tree {
    position:absolute;bottom:145px;font-size:43px;z-index:2;
}
.tree.t1{left:3%}.tree.t2{right:3%}
.sidewalk {
    position:absolute;bottom:112px;width:100%;height:48px;
    background:repeating-linear-gradient(90deg,#f5d6b9 0 65px,#eac4a5 65px 69px);
    border-top:4px solid #fff5e7;border-bottom:4px solid #d3a98b;
}
.road {
    position:absolute;bottom:0;width:100%;height:115px;
    background:linear-gradient(#69788c,#4b5b73);
    border-top:5px solid #f7f0d5;
}
.road:after {
    content:"";position:absolute;top:51px;left:0;right:0;height:5px;
    background:repeating-linear-gradient(90deg,#fff5cc 0 45px,transparent 45px 82px);
}
.lamp {
    position:absolute;bottom:115px;font-size:38px;z-index:3;
}
.l1{left:12%}.l2{right:12%}
.ufo {
    position:absolute;z-index:8;top:13px;left:50%;
    transform:translateX(-50%);font-size:66px;
    filter:drop-shadow(0 5px 4px #7565a566);
    transition:left 1s ease, top .8s ease;
    animation: hover 2s ease-in-out infinite;
}
@keyframes hover {0%,100%{margin-top:0}50%{margin-top:9px}}
.ufo-counter {
    position:absolute;top:83px;left:50%;transform:translateX(-50%);
    z-index:9;background:#263a48;color:#baffd4;border:3px solid #fff;
    border-radius:7px;padding:2px 14px;font-weight:900;font-size:13px;
}
.beam {
    display:none;position:absolute;z-index:6;top:88px;left:50%;
    transform:translateX(-50%);
    width:0;height:240px;
    background:linear-gradient(180deg,#a6fff7aa,#b7f4ff22);
    clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);
    filter:drop-shadow(0 0 15px #b3fff9);
}
.beam.active {display:block;animation: beamflash .5s infinite alternate;}
@keyframes beamflash {from{opacity:.45}to{opacity:1}}
.student {
    position:absolute;z-index:7;bottom:78px;left:var(--x);
    transform:translateX(-50%);text-align:center;
    transition:left 1.1s ease, bottom 1s ease, transform .5s;
    animation: walk 1s ease-in-out infinite alternate;
}
@keyframes walk {from{margin-bottom:0}to{margin-bottom:4px}}
.student .name {
    display:block;white-space:nowrap;font-size:11px;font-weight:900;
    background:white;border:1px solid #cfc5e9;border-radius:7px;
    padding:3px 5px;margin-bottom:1px;box-shadow:0 2px 0 #c9c1df;
}
.student .person {font-size:36px;line-height:38px;display:block;}
.student .ride {font-size:23px;line-height:20px;display:block;margin-top:-7px;}
.student.captured {bottom:300px;transform:translateX(-50%) scale(.65);opacity:.2;}
.student.selected .name {background:#fff29d;border-color:#ff9c49;}
.hint {
    text-align:center;font-size:14px;font-weight:bold;color:#67568b;
    margin:10px 0;
}
.controls {display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:12px 0;}
.btn {
    border:0;border-radius:14px;padding:12px 19px;font-size:15px;
    font-weight:900;box-shadow:0 5px 0 #0002;transition:transform .1s;
}
.btn:active {transform:translateY(3px);box-shadow:0 2px 0 #0002;}
.primary {background:#8664e8;color:white;}
.secondary {background:white;color:#65518f;border:2px solid #e0d6ff;}
.note {text-align:center;color:#766a91;font-size:12px;margin:8px;}
.modal {
    display:none;position:absolute;inset:0;z-index:20;
    background:#23334dbb;align-items:center;justify-content:center;padding:15px;
}
.modal.show {display:flex;}
.card {
    background:#fffdf9;width:min(480px,100%);border-radius:22px;
    padding:20px;border:4px solid #fff;box-shadow:0 10px 0 #b4a1e0;
    text-align:center;max-height:95%;overflow:auto;
}
.card h2 {margin:4px 0 10px;color:#7854c9;font-size:23px;}
.question {font-size:18px;font-weight:900;line-height:1.4;margin:12px 0;}
.answers {display:grid;grid-template-columns:1fr 1fr;gap:9px;}
.answer {
    background:#f0ebff;border:2px solid #d9cdfa;border-radius:12px;
    padding:12px 7px;font-weight:bold;color:#45365f;font-size:14px;
}
.answer:hover {background:#e1d6ff;}
.answer:disabled {cursor:default;opacity:1;}
.answer.correct {background:#c9f7d6;border-color:#56c77c;}
.answer.wrong {background:#ffd5d8;border-color:#ef7884;}
.feedback {font-weight:bold;min-height:24px;margin:12px 0;}
.next {background:#8664e8;color:white;width:100%;margin-top:5px;}
.result-big {font-size:45px;}
@media(max-width:550px) {
    .scene{height:390px}
    .buildings{height:112px;bottom:150px}
    .shop{font-size:10px}
    .sidewalk{bottom:110px}
    .road{height:112px}
    .student .person{font-size:29px}
    .student .name{font-size:9px;padding:2px 3px}
    .student .ride{font-size:19px}
    .ufo{font-size:54px}
    .ufo-counter{top:70px}
    .beam{top:78px;height:220px}
    .answers{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="game">
  <div class="topbar">
    <div class="logo">👽 UFO KHẢO BÀI</div>
    <div class="stat">⭐ Điểm: <span id="score">0</span></div>
    <div class="stat">🛸 Đã hỏi: <span id="round">0</span>/<span id="total">5</span></div>
  </div>

  <div class="scene" id="scene">
    <div class="sun"></div>
    <div class="cloud">☁️</div><div class="cloud two">☁️</div>
    <div class="buildings">
      <div class="shop s1"><span>🥖 BÁNH MÌ</span></div>
      <div class="shop s2"><span>🧋 TRÀ SỮA</span></div>
      <div class="shop s3"><span>📚 NHÀ SÁCH</span></div>
      <div class="shop s4"><span>🍜 BÚN CHẢ</span></div>
      <div class="shop s5"><span>🏪 TẠP HÓA</span></div>
    </div>
    <div class="tree t1">🌳</div><div class="tree t2">🌳</div>
    <div class="sidewalk"></div>
    <div class="lamp l1">💡</div><div class="lamp l2">💡</div>
    <div class="road"></div>
    <div class="ufo" id="ufo">🛸</div>
    <div class="ufo-counter" id="ufoCounter">0 / 5</div>
    <div class="beam" id="beam"></div>
    <div id="students"></div>

    <div class="modal show" id="intro">
      <div class="card">
        <div class="result-big">🛸👽</div>
        <h2>UFO đến khảo bài!</h2>
        <p>Người ngoài hành tinh đang tìm học sinh để hỏi bài. Bạn có trả lời được không?</p>
        <p>🎯 Trả lời đúng: +10 điểm</p>
        <button class="btn primary" onclick="startGame()">🚀 BẮT ĐẦU CHƠI</button>
      </div>
    </div>

    <div class="modal" id="quizModal">
      <div class="card">
        <div class="result-big" id="quizEmoji">👩‍🎓</div>
        <h2 id="quizTitle">Bạn được UFO chọn!</h2>
        <div class="question" id="question"></div>
        <div class="answers" id="answers"></div>
        <div class="feedback" id="feedback"></div>
        <button class="btn next" id="nextBtn" style="display:none" onclick="nextQuestion()">Tiếp tục ➜</button>
      </div>
    </div>

    <div class="modal" id="endModal">
      <div class="card">
        <div class="result-big" id="endEmoji">🏆</div>
        <h2>Hoàn thành buổi khảo bài!</h2>
        <p id="endText"></p>
        <button class="btn primary" onclick="resetGame()">🔄 CHƠI LẠI</button>
      </div>
    </div>
  </div>

  <div class="hint" id="hint">Nhấn bắt đầu để xem UFO chọn học sinh nào nhé!</div>
  <div class="controls">
    <button class="btn primary" onclick="manualPick()">🛸 UFO chọn học sinh</button>
    <button class="btn secondary" onclick="resetGame()">🔄 Chơi lại</button>
  </div>
  <div class="note">📚 Có thể dùng làm trò chơi ôn tập Toán, Tiếng Anh, Khoa học và nhiều môn học khác.</div>
</div>

<script>
const studentsData = [
  {name:"Minh Huy", emoji:"🧑🏻‍🎓", ride:"🛵", x:9},
  {name:"Trúc Mai", emoji:"👧🏻", ride:"🛵", x:21},
  {name:"Phương Mai", emoji:"👩🏻‍🎓", ride:"🛵", x:33},
  {name:"Tuấn Minh", emoji:"👦🏻", ride:"🛵", x:45},
  {name:"Quỳnh Anh", emoji:"👧🏼", ride:"🛵", x:57},
  {name:"Huy Khánh", emoji:"🧑🏽‍🎓", ride:"🛵", x:69},
  {name:"Mai Anh", emoji:"👩🏻", ride:"🛵", x:81},
  {name:"Đăng An", emoji:"👦🏼", ride:"🛵", x:92}
];

const questions = [
 {q:"Giải phương trình: 2x + 6 = 10. Giá trị x là bao nhiêu?", a:["x = 2","x = 3","x = 4","x = 8"], correct:0, explain:"2x = 10 − 6 = 4 nên x = 2."},
 {q:"Trong tiếng Anh, “beautiful” có nghĩa là gì?", a:["Buồn bã","Xinh đẹp","Nhanh chóng","Thông minh"], correct:1, explain:"Beautiful nghĩa là xinh đẹp."},
 {q:"Một tam giác có tổng ba góc bằng bao nhiêu?", a:["90°","180°","270°","360°"], correct:1, explain:"Tổng ba góc trong một tam giác bằng 180°."},
 {q:"Từ nào sau đây là một động từ tiếng Anh?", a:["Beautiful","Happiness","Run","Blue"], correct:2, explain:"Run là động từ, có nghĩa là chạy."},
 {q:"Nếu x² = 25 thì x có thể bằng những giá trị nào?", a:["Chỉ 5","Chỉ −5","5 hoặc −5","Chỉ 25"], correct:2, explain:"Cả 5² và (−5)² đều bằng 25."},
 {q:"Thủ đô của Việt Nam là thành phố nào?", a:["Huế","Đà Nẵng","TP. Hồ Chí Minh","Hà Nội"], correct:3, explain:"Thủ đô của Việt Nam là Hà Nội."},
 {q:"Phân số 1/2 viết dưới dạng số thập phân là gì?", a:["0,2","0,5","1,2","2,0"], correct:1, explain:"1 chia 2 bằng 0,5."},
 {q:"Từ trái nghĩa với “hot” là gì?", a:["Warm","Cold","Tall","Fast"], correct:1, explain:"Cold có nghĩa là lạnh, trái nghĩa với hot."},
 {q:"Nước đóng băng ở nhiệt độ bao nhiêu độ C trong điều kiện thông thường?", a:["0°C","10°C","50°C","100°C"], correct:0, explain:"Nước tinh khiết đóng băng ở khoảng 0°C trong điều kiện thông thường."},
 {q:"Một giờ có bao nhiêu phút?", a:["30 phút","45 phút","60 phút","100 phút"], correct:2, explain:"Một giờ có 60 phút."}
];

let score = 0, round = 0, active = false, waiting = false;
let remaining = [], currentStudent = null, currentQuestion = null, usedQuestions = [];
const $ = id => document.getElementById(id);

function renderStudents() {
  $("students").innerHTML = "";
  studentsData.forEach((s, i) => {
    const el = document.createElement("div");
    el.className = "student";
    el.id = "student" + i;
    el.style.setProperty("--x", s.x + "%");
    el.innerHTML = `<span class="name">${s.name}</span><span class="person">${s.emoji}</span><span class="ride">${s.ride}</span>`;
    $("students").appendChild(el);
  });
}
renderStudents();

function updateStats() {
  $("score").textContent = score;
  $("round").textContent = round;
  $("ufoCounter").textContent = round + " / 5";
}
function startGame() {
  score = 0; round = 0; active = true; waiting = false;
  remaining = studentsData.map((_,i)=>i);
  usedQuestions = [];
  $("intro").classList.remove("show");
  $("endModal").classList.remove("show");
  $("hint").textContent = "UFO đang bay quanh phố... nhấn nút để chọn một học sinh!";
  renderStudents();
  updateStats();
  $("ufo").style.left = "50%";
  $("ufo").style.top = "13px";
}
function manualPick() {
  if (!active) {
    $("intro").classList.add("show");
    return;
  }
  if (waiting) return;
  if (round >= 5 || remaining.length === 0) {
    endGame();
    return;
  }
  waiting = true;
  const randomIndex = Math.floor(Math.random() * remaining.length);
  const studentIndex = remaining.splice(randomIndex,1)[0];
  currentStudent = studentIndex;
  const studentEl = $("student" + studentIndex);
  const s = studentsData[studentIndex];
  studentEl.classList.add("selected");
  $("hint").textContent = "🛸 UFO đang bay đến chỗ " + s.name + "!";
  $("ufo").style.left = s.x + "%";
  $("ufo").style.top = "35px";
  $("beam").style.left = s.x + "%";
  $("beam").classList.add("active");
  setTimeout(() => {
    $("beam").classList.remove("active");
    studentEl.classList.add("captured");
    $("hint").textContent = "✨ " + s.name + " được đưa lên UFO để khảo bài!";
    setTimeout(showQuestion, 700);
  }, 1100);
}
function showQuestion() {
  if (!active) return;
  round++;
  updateStats();
  let available = questions.map((_,i)=>i).filter(i=>!usedQuestions.includes(i));
  if (available.length === 0) { usedQuestions=[]; available=questions.map((_,i)=>i); }
  const qIndex = available[Math.floor(Math.random()*available.length)];
  usedQuestions.push(qIndex);
  currentQuestion = questions[qIndex];
  $("quizEmoji").textContent = studentsData[currentStudent].emoji;
  $("quizTitle").textContent = studentsData[currentStudent].name + " ơi, trả lời nhé!";
  $("question").textContent = currentQuestion.q;
  $("feedback").textContent = "";
  $("nextBtn").style.display = "none";
  $("answers").innerHTML = "";
  currentQuestion.a.forEach((answer,i) => {
    const btn = document.createElement("button");
    btn.className = "answer";
    btn.textContent = ["A. ","B. ","C. ","D. "][i] + answer;
    btn.onclick = () => checkAnswer(i, btn);
    $("answers").appendChild(btn);
  });
  $("quizModal").classList.add("show");
}
function checkAnswer(index, button) {
  const buttons = [...$("answers").querySelectorAll("button")];
  buttons.forEach(b => b.disabled = true);
  if (index === currentQuestion.correct) {
    button.classList.add("correct");
    score += 10;
    $("feedback").textContent = "🎉 Chính xác! +10 điểm";
    $("feedback").style.color = "#21834a";
  } else {
    button.classList.add("wrong");
    buttons[currentQuestion.correct].classList.add("correct");
    $("feedback").textContent = "💡 Chưa đúng! " + currentQuestion.explain;
    $("feedback").style.color = "#c44c61";
  }
  updateStats();
  $("nextBtn").style.display = "block";
}
function nextQuestion() {
  $("quizModal").classList.remove("show");
  const studentEl = $("student" + currentStudent);
  studentEl.classList.remove("selected","captured");
  studentEl.style.opacity = "0.3";
  $("ufo").style.left = "50%";
  $("ufo").style.top = "13px";
  waiting = false;
  if (round >= 5 || remaining.length === 0) {
    endGame();
  } else {
    $("hint").textContent = "Câu tiếp theo đang chờ! Nhấn “UFO chọn học sinh” nhé.";
  }
}
function endGame() {
  active = false;
  waiting = false;
  $("endEmoji").textContent = score >= 40 ? "🏆🎉" : score >= 20 ? "⭐😊" : "📚💪";
  $("endText").textContent = "Bạn đạt " + score + " điểm sau " + round + " câu hỏi. " +
    (score >= 40 ? "Xuất sắc! Bạn là cao thủ khảo bài!" :
    score >= 20 ? "Làm tốt lắm! Ôn thêm một chút nhé!" :
    "Đừng nản nhé, hãy ôn tập rồi thử lại!");
  $("endModal").classList.add("show");
  $("hint").textContent = "Buổi khảo bài đã kết thúc!";
}
function resetGame() {
  $("intro").classList.remove("show");
  $("quizModal").classList.remove("show");
  $("endModal").classList.remove("show");
  score = 0; round = 0; active = false; waiting = false;
  remaining = []; usedQuestions = [];
  renderStudents();
  updateStats();
  $("ufo").style.left = "50%";
  $("ufo").style.top = "13px";
  $("beam").classList.remove("active");
  $("hint").textContent = "Nhấn BẮT ĐẦU CHƠI để bắt đầu buổi khảo bài!";
  $("intro").classList.add("show");
}
</script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=True)
