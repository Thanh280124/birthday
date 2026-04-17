import streamlit as st
import os
import base64
from PIL import Image

st.set_page_config(
    page_title="Birthday 🎂",
    layout="wide"
)

# =========================
# 🔧 Convert image -> base64
# =========================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# =========================
# 🎂 Title
# =========================
st.markdown(
    """
    <h1 style='text-align:center;color:#ff4b6e;font-size:60px;'>
        🎂 Happy Birthday 🎂
    </h1>
    """,
    unsafe_allow_html=True
)

# =========================
# 💖 Floating hearts + Fireworks (auto, no click needed)
# =========================
st.components.v1.html("""
<div id="hearts-container" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;"></div>
<canvas id="fireworks" style="position:fixed;top:0;left:0;pointer-events:none;z-index:9998;"></canvas>

<style>
.heart {
  position: fixed;
  font-size: 24px;
  animation: floatUp linear forwards;
  pointer-events: none;
}

@keyframes floatUp {
  from {
    transform: translateY(100vh) scale(1);
    opacity: 1;
  }
  to {
    transform: translateY(-10vh) scale(0.5);
    opacity: 0;
  }
}
</style>

<script>
// Auto floating hearts (no click needed - works on iPad/phone)
const emojis = ["💖", "💕", "💗", "💓", "🌸", "✨"];

function createHeart() {
  const heart = document.createElement("div");
  heart.className = "heart";
  heart.innerHTML = emojis[Math.floor(Math.random() * emojis.length)];
  heart.style.left = (Math.random() * 100) + "vw";
  heart.style.bottom = "-50px";
  const duration = 4 + Math.random() * 4;
  heart.style.animationDuration = duration + "s";
  heart.style.fontSize = (18 + Math.random() * 18) + "px";

  document.getElementById("hearts-container").appendChild(heart);

  setTimeout(() => heart.remove(), duration * 1000);
}

setInterval(createHeart, 350);

// Fireworks canvas
const canvas = document.getElementById("fireworks");
const ctx = canvas.getContext("2d");

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

const particles = [];

function spawnFirework() {
  const x = Math.random() * canvas.width;
  const y = Math.random() * canvas.height * 0.5;
  const colors = ["#ff4b6e","#ff9ee0","#ffd700","#ff6b35","#c77dff","#90e0ef"];
  const color = colors[Math.floor(Math.random() * colors.length)];

  for (let i = 0; i < 30; i++) {
    const angle = (Math.PI * 2 / 30) * i;
    const speed = 1.5 + Math.random() * 2.5;
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      alpha: 1,
      color,
      radius: 2 + Math.random() * 2
    });
  }
}

function animateFireworks() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx;
    p.y += p.vy;
    p.vy += 0.05; // gravity
    p.alpha -= 0.018;

    if (p.alpha <= 0) {
      particles.splice(i, 1);
      continue;
    }

    ctx.globalAlpha = p.alpha;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.globalAlpha = 1;
  requestAnimationFrame(animateFireworks);
}

animateFireworks();
setInterval(spawnFirework, 1200);
</script>
""", height=0)

# =========================
# 🃏 Flip Card - FIXED using st.components.v1.html
# =========================
st.markdown("## 🃏 Mở thiệp")

cover_path = "images/cover.jpg"
inside_path = "images/inside.jpg"

if os.path.exists(cover_path) and os.path.exists(inside_path):
    cover_b64 = img_to_base64(cover_path)
    inside_b64 = img_to_base64(inside_path)

    # Detect image extension for correct mime type
    cover_ext = cover_path.split(".")[-1].lower()
    inside_ext = inside_path.split(".")[-1].lower()
    cover_mime = "image/jpeg" if cover_ext in ["jpg", "jpeg"] else "image/png"
    inside_mime = "image/jpeg" if inside_ext in ["jpg", "jpeg"] else "image/png"

    # Use st.components.v1.html to properly render the flip card with base64 images
    st.components.v1.html(f"""
    <style>
    body {{ margin: 0; background: transparent; }}

    .flip-card {{
      background-color: transparent;
      width: 320px;
      height: 420px;
      perspective: 1000px;
      margin: 30px auto;
      cursor: pointer;
    }}

    .flip-card-inner {{
      position: relative;
      width: 100%;
      height: 100%;
      transition: transform 0.8s;
      transform-style: preserve-3d;
    }}

    /* Hover for desktop */
    .flip-card:hover .flip-card-inner {{
      transform: rotateY(180deg);
    }}

    /* Tap toggle for mobile/iPad */
    .flip-card.flipped .flip-card-inner {{
      transform: rotateY(180deg);
    }}

    .flip-card-front, .flip-card-back {{
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 32px rgba(255,75,110,0.3);
    }}

    .flip-card-back {{
      transform: rotateY(180deg);
    }}

    .flip-card img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .hint {{
      text-align: center;
      color: #ff4b6e;
      font-size: 14px;
      font-family: sans-serif;
      margin-top: -10px;
    }}
    </style>

    <div class="flip-card" id="card" onclick="this.classList.toggle('flipped')">
      <div class="flip-card-inner">

        <div class="flip-card-front">
          <img src="data:{cover_mime};base64,{cover_b64}" alt="Cover">
        </div>

        <div class="flip-card-back">
          <img src="data:{inside_mime};base64,{inside_b64}" alt="Inside">
        </div>

      </div>
    </div>
    <p class="hint">👆 Chạm / rê chuột để lật thiệp</p>
    """, height=500)

else:
    st.warning("⚠️ Chưa có ảnh cover.jpg hoặc inside.jpg trong thư mục images/")
    st.info("Tạo thư mục `images/` và thêm file `cover.jpg` + `inside.jpg` vào nhé!")

# =========================
# 💌 Text typing effect
# =========================
st.markdown("## 💌 Lời chúc")

st.components.v1.html("""
<div id="text" style="font-size:22px;text-align:center;color:#ff4b6e;font-family:sans-serif;padding:20px;"></div>

<script>
let text = "Chúc bạn sinh nhật vui vẻ, hạnh phúc và luôn cười thật nhiều 💖";
let i = 0;

function type(){
  if(i < text.length){
    document.getElementById("text").innerHTML += text.charAt(i);
    i++;
    setTimeout(type, 60);
  }
}
type();
</script>
""", height=100)

# =========================
# 📸 Gallery
# =========================
folder = "images"

if os.path.exists(folder):
    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(("jpg", "png", "jpeg"))
        and f not in ["cover.jpg", "inside.jpg"]
    ]

    if files:
        st.markdown("## 📸 Kỷ niệm")
        cols = st.columns(3)
        for i, file in enumerate(files):
            img = Image.open(os.path.join(folder, file))
            cols[i % 3].image(img, use_container_width=True)

# =========================
# 🎵 Music
# =========================
music_path = "music/song.mp3"

if os.path.exists(music_path):
    st.markdown("## 🎵 Nhạc")
    audio = open(music_path, "rb")
    st.audio(audio.read(), format="audio/mp3")

# =========================
# 🎥 Video
# =========================
video_path = "video/video.mp4"

if os.path.exists(video_path):
    st.markdown("## 🎥 Video")
    video = open(video_path, "rb")
    st.video(video.read())