import streamlit as st
import os
import base64
from PIL import Image

st.set_page_config(page_title="Birthday 🎂", layout="wide")

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =========================
# TITLE + GLOBAL EFFECTS (Hearts + Fireworks + Music)
# =========================
st.markdown("""
    <h1 style='text-align:center;color:#ff4b6e;font-size:30px;'>
        🎂 Happy Birthday 🎂
    </h1>
    """, unsafe_allow_html=True)

# Global Music + Hearts + Fireworks (đặt ngoài tabs để tránh lỗi)
music_path = "music/song.mp3"
if os.path.exists(music_path):
    music_b64 = img_to_base64(music_path)
    st.components.v1.html(f"""
    <audio id="bgMusic" loop>
      <source src="data:audio/mp3;base64,{music_b64}" type="audio/mpeg">
    </audio>
    <div id="playBtn" onclick="toggleMusic()" style="position:fixed;bottom:16px;right:16px;width:50px;height:50px;background:#ff4b6e;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;z-index:99999;box-shadow:0 4px 15px rgba(255,75,110,0.6);">▶️</div>

    <script>
    const music = document.getElementById("bgMusic");
    let playing = false;
    function toggleMusic() {{
        if(!playing) {{
            music.play().then(() => {{ playing = true; document.getElementById("playBtn").textContent = "🎵"; }});
        }} else {{
            music.pause(); playing = false; document.getElementById("playBtn").textContent = "▶️";
        }}
    }}
    // Auto play khi click lần đầu
    document.addEventListener("click", () => {{ if(!playing) toggleMusic(); }}, {{once: true}});
    </script>
    """, height=80)

# Hearts + Fireworks (global)
st.components.v1.html("""
<!DOCTYPE html><html><head><style>
* {margin:0;padding:0;box-sizing:border-box;}
html,body {width:100%;height:100%;background:transparent;overflow:hidden;}
.heart {position:fixed; animation:floatUp linear forwards; pointer-events:none; z-index:9999;}
@keyframes floatUp {0%{transform:translateY(110vh) scale(1);opacity:1;} 100%{transform:translateY(-10vh) scale(0.5);opacity:0;}}
#fireworks {position:fixed;top:0;left:0;pointer-events:none;z-index:9998;}
</style></head><body>
<div id="hc"></div><canvas id="fireworks"></canvas>
<script>
const emojis = ["💖","💕","💗","💓","🌸","✨","🎀","💝"];
function createHeart() {
  const h = document.createElement("div"); h.className="heart";
  h.textContent = emojis[Math.floor(Math.random()*emojis.length)];
  h.style.left = (Math.random()*98)+"vw";
  const dur = 4 + Math.random()*4;
  h.style.animationDuration = dur + "s";
  h.style.fontSize = (18 + Math.random()*24) + "px";
  document.getElementById("hc").appendChild(h);
  setTimeout(()=>h.remove(), dur*1000);
}
setInterval(createHeart, 350);
for(let i=0;i<15;i++) setTimeout(createHeart, i*70);

// Fireworks đơn giản
const canvas = document.getElementById("fireworks");
const ctx = canvas.getContext("2d");
function resize(){canvas.width = window.innerWidth; canvas.height = window.innerHeight;}
resize(); window.addEventListener("resize", resize);
const parts = [];
const COLORS = ["#ff4b6e","#ffb3c6","#ffd700","#ff6b35","#c77dff"];
function boom(){
  const x = Math.random() * canvas.width;
  const y = Math.random() * (canvas.height * 0.4);
  const col = COLORS[Math.floor(Math.random()*COLORS.length)];
  for(let i=0;i<35;i++){
    const a = Math.random()*Math.PI*2;
    const s = 1.5 + Math.random()*3.5;
    parts.push({x,y, vx:Math.cos(a)*s, vy:Math.sin(a)*s - 2, alpha:1, color:col, r:2.5+Math.random()*2, decay:0.015+Math.random()*0.01});
  }
}
function draw(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for(let i=parts.length-1; i>=0; i--){
    const p = parts[i];
    p.x += p.vx; p.y += p.vy; p.vy += 0.08; p.vx *= 0.985;
    p.alpha -= p.decay;
    if(p.alpha <= 0){ parts.splice(i,1); continue; }
    ctx.globalAlpha = p.alpha;
    ctx.fillStyle = p.color;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
  }
  requestAnimationFrame(draw);
}
draw();
setInterval(boom, 1800); boom();
</script></body></html>
""", height=420)

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🃏 Thiệp", "💌 Lời chúc", "📸 Kỷ niệm"])

# Tab 1: Chỉ Flip Card
with tab1:
    st.markdown("### 🃏 Mở thiệp chúc mừng")
    cover_path = "images/cover.jpg"
    inside_path = "images/inside.jpg"
    if os.path.exists(cover_path) and os.path.exists(inside_path):
        cover_b64 = img_to_base64(cover_path)
        inside_b64 = img_to_base64(inside_path)
        mime_type = "image/png" if cover_path.endswith(".png") else "image/jpeg"

        st.components.v1.html(f"""
        <style>
        .flip-card {{width:320px;height:420px;perspective:1200px;margin:30px auto;cursor:pointer;}}
        .flip-card-inner {{position:relative;width:100%;height:100%;transition:transform 0.9s;transform-style:preserve-3d;}}
        .flip-card.flipped .flip-card-inner {{transform:rotateY(180deg);}}
        .flip-card-front, .flip-card-back {{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(255,75,110,0.5);}}
        .flip-card-back {{transform:rotateY(180deg);}}
        .flip-card img {{width:100%;height:100%;object-fit:cover;}}
        </style>
        <div class="flip-card" id="card">
          <div class="flip-card-inner">
            <div class="flip-card-front"><img src="data:{mime_type};base64,{cover_b64}"></div>
            <div class="flip-card-back"><img src="data:{mime_type};base64,{inside_b64}"></div>
          </div>
        </div>
        <p style="text-align:center;color:#ff4b6e;">👆 Chạm hoặc click để lật thiệp</p>
        <script>
        const card = document.getElementById("card");
        card.addEventListener("click", () => card.classList.toggle("flipped"));
        card.addEventListener("touchend", (e) => {{ e.preventDefault(); card.classList.toggle("flipped"); }});
        </script>
        """, height=520)
    else:
        st.warning("Vui lòng thêm file `images/cover.jpg` và `images/inside.jpg`")

# Tab 2: Lời chúc (chữ chạy lại mỗi lần chuyển vào tab)
with tab2:
    st.markdown("## 💌 Lời chúc")
    st.components.v1.html("""
    <div id="typing" style="font-size:26px;text-align:center;color:#ff4b6e;padding:40px 20px;min-height:180px;line-height:1.7;"></div>
    <script>
    const txt = "Chúc bạn sinh nhật vui vẻ, hạnh phúc ngập tràn và luôn cười thật nhiều mỗi ngày 💖🌸✨";
    function startType() {
      const el = document.getElementById("typing");
      el.innerHTML = "";
      let i = 0;
      const intv = setInterval(() => {
        if (i < txt.length) {
          el.innerHTML += txt.charAt(i);
          i++;
        } else clearInterval(intv);
      }, 65);
    }
    startType();
    </script>
    """, height=280)

# Tab 3: Kỷ niệm
with tab3:
    st.markdown("## 📸 Kỷ niệm")

    # Gallery
    folder = "images"
    if os.path.exists(folder):
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg','.jpeg','.png')) and f not in ["cover.jpg","inside.jpg"]]
        if files:
            cols = st.columns(3)
            for i, f in enumerate(files):
                cols[i%3].image(Image.open(os.path.join(folder, f)), use_container_width=True)

    # Video
    video_path = "video/video.mp4"
    if os.path.exists(video_path):
        st.markdown("### 🎥 Video kỷ niệm")
        video_b64 = base64.b64encode(open(video_path, "rb").read()).decode()
        st.components.v1.html(f"""
        <video width="100%" controls autoplay loop muted playsinline>
          <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        """, height=520)
    else:
        st.info("Đặt video/video.mp4 để hiển thị video.")
