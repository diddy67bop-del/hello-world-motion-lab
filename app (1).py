import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Hello World Motion Lab")
st.write("A tiny creative playground for names, fonts, colors, and motion.")

# Controls
st.sidebar.header("Customize your canvas")
name = st.sidebar.text_input("Your name or message", value="Hello World", max_chars=100)
font_family = st.sidebar.selectbox(
    "Font family",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
     "Trebuchet MS", "Impact", "Comic Sans MS", "monospace", "serif", "sans-serif"],
)
font_size = st.sidebar.slider("Font size", min_value=20, max_value=100, value=52, step=2)
font_weight = st.sidebar.select_slider(
    "Font weight", options=["Normal", "Bold", "Extra bold"], value="Bold"
)
name_mode = st.sidebar.selectbox(
    "Name display mode", ["Centered", "Ticker Tape", "Repeated"]
)
background = st.sidebar.selectbox(
    "Background",
    ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
)
effect = st.sidebar.selectbox(
    "Dynamic action",
    ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
)
animation_speed = st.sidebar.slider(
    "Animation speed", min_value=0.5, max_value=2.5, value=1.0, step=0.1,
    help="Lower values move more slowly; higher values move more quickly.",
)
show_effects = st.sidebar.checkbox("Show motion effects", value=True)

themes = {
    "Light": ("#f8fafc", "#172033", "#dbeafe"),
    "Dark": ("#10131c", "#f8fafc", "#272d3d"),
    "Ocean": ("#06283d", "#eafaff", "#136b82"),
    "Sunset": ("#3b164a", "#fff4e8", "#9c3d66"),
    "Forest": ("#102a21", "#f0fff4", "#285943"),
    "Lavender": ("#f1eaff", "#30204d", "#d8c6ff"),
}
bg_color, text_color, accent_color = themes[background]
escaped_name = html.escape(name or "Hello World", quote=True)
safe_font = font_family.replace('"', "").replace("'", "")
weight = {"Normal": "400", "Bold": "700", "Extra bold": "900"}[font_weight]
speed = max(0.2, animation_speed)

# Build decorative particles. CSS performs the animation in the browser, so it loops
# continuously without repeatedly rerunning the Streamlit script.
rng = random.Random(42)
particles = []
if show_effects and effect != "None":
    particle_count = 65 if effect in ("Rain", "Snow", "Confetti") else 38
    for i in range(particle_count):
        left = rng.randint(0, 100)
        delay = rng.uniform(-12, 0)
        duration = rng.uniform(2.8, 6.5) / speed
        size = rng.randint(5, 13)
        drift = rng.randint(-90, 90)
        rotation = rng.randint(180, 900)
        if effect == "Rain":
            symbol = "│"
            cls = "particle rain"
        elif effect == "Snow":
            symbol = rng.choice(["❄", "✳", "❅", "•"])
            cls = "particle snow"
        elif effect == "Hail":
            symbol = "●"
            cls = "particle hail"
        elif effect == "Wind Gust":
            symbol = rng.choice(["〰", "～", "➝", "﹏"])
            cls = "particle wind"
        elif effect == "Confetti":
            symbol = rng.choice(["■", "●", "▲", "◆", "✦", "★"])
            cls = "particle confetti"
        else:  # Tornado
            symbol = rng.choice(["〰", "•", "✦", "∿"])
            cls = "particle tornado"
        particles.append(
            f'<span class="{cls}" style="--left:{left}%;--delay:{delay:.2f}s;'
            f'--duration:{duration:.2f}s;--size:{size}px;--drift:{drift}px;'
            f'--rotation:{rotation}deg">{symbol}</span>'
        )

if name_mode == "Centered":
    name_markup = f'<div class="name centered">{escaped_name}</div>'
elif name_mode == "Ticker Tape":
    name_markup = (
        '<div class="ticker-window"><div class="ticker-track">'
        f'<span>{escaped_name}</span><span>{escaped_name}</span>'
        '</div></div>'
    )
else:
    name_markup = '<div class="repeat-grid">' + "".join(
        f'<div class="name repeat-name">{escaped_name}</div>' for _ in range(6)
    ) + '</div>'

effect_markup = "".join(particles)
effect_class = "effect-layer" if show_effects and effect != "None" else "effect-layer hidden"

document = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; isolation: isolate; overflow: hidden;
  width: 100%; height: 590px; border-radius: 18px;
  background: {bg_color}; color: {text_color};
  font-family: "{safe_font}", sans-serif;
  box-shadow: inset 0 0 0 1px {accent_color};
}}
.stage::before {{
  content: ""; position: absolute; inset: -30%;
  background: radial-gradient(circle at 20% 25%, {accent_color}88, transparent 38%),
              radial-gradient(circle at 80% 75%, {accent_color}55, transparent 35%);
  opacity: .65; z-index: -1; animation: glow 9s ease-in-out infinite alternate;
}}
.effect-layer {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
.effect-layer.hidden {{ display: none; }}
.particle {{ position: absolute; top: -12%; left: var(--left); font-size: var(--size);
  animation-delay: var(--delay); animation-duration: var(--duration);
  animation-timing-function: linear; animation-iteration-count: infinite;
  will-change: transform, opacity; user-select: none; }}
.rain {{ color: #42a5f5; opacity: .8; font-weight: 300; animation-name: fall; }}
.snow {{ color: #fff; text-shadow: 0 0 8px #b8e9ff; animation-name: snow-fall; }}
.hail {{ color: #bfeaff; text-shadow: 0 0 5px white; animation-name: hail-fall; }}
.wind {{ color: {accent_color}; opacity: .9; animation-name: gust; }}
.confetti {{ color: hsl(calc(var(--left) * 3.6), 90%, 65%); animation-name: confetti-fall; }}
.tornado {{ color: {accent_color}; animation-name: swirl; }}
.content {{ position: relative; z-index: 2; width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center; padding: 32px; }}
.name {{ font-size: {font_size}px; font-weight: {weight}; line-height: 1.18;
  overflow-wrap: anywhere; text-shadow: 0 3px 16px #0002; }}
.centered {{ text-align: center; max-width: 100%; animation: arrive 700ms ease-out both; }}
.ticker-window {{ width: 100%; overflow: hidden; }}
.ticker-track {{ display: flex; width: max-content; gap: 70px; white-space: nowrap;
  animation: marquee {max(8, 22 / speed):.2f}s linear infinite; }}
.ticker-track span {{ font-size: {font_size}px; font-weight: {weight}; text-shadow: 0 3px 16px #0002; }}
.repeat-grid {{ width: 100%; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px; align-items: center; }}
.repeat-name {{ text-align: center; font-size: {max(18, int(font_size * .62))}px;
  overflow-wrap: anywhere; animation: pulse 3s ease-in-out infinite alternate; }}
.repeat-name:nth-child(even) {{ animation-delay: -1.5s; }}
@keyframes fall {{ from {{ transform: translate3d(0,-5vh,0); }} to {{ transform: translate3d(var(--drift),115vh,0); }} }}
@keyframes snow-fall {{ 0% {{ transform: translate3d(0,-5vh,0) rotate(0); }} 100% {{ transform: translate3d(var(--drift),115vh,0) rotate(360deg); }} }}
@keyframes hail-fall {{ 0% {{ transform: translate3d(0,-5vh,0); }} 100% {{ transform: translate3d(var(--drift),115vh,0); }} }}
@keyframes gust {{ 0% {{ transform: translate3d(-25vw, 10vh,0) rotate(0); opacity:0; }} 20% {{ opacity:.9; }} 100% {{ transform: translate3d(125vw, var(--drift),0) rotate(25deg); opacity:0; }} }}
@keyframes confetti-fall {{ 0% {{ transform: translate3d(0,-8vh,0) rotate(0); }} 100% {{ transform: translate3d(var(--drift),115vh,0) rotate(var(--rotation)); }} }}
@keyframes swirl {{ 0% {{ transform: translate3d(0,-5vh,0) rotate(0) scale(.6); }} 50% {{ transform: translate3d(var(--drift),50vh,0) rotate(220deg) scale(1.1); }} 100% {{ transform: translate3d(0,115vh,0) rotate(480deg) scale(.6); }} }}
@keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
@keyframes arrive {{ from {{ opacity:0; transform: translateY(12px) scale(.98); }} to {{ opacity:1; transform: translateY(0) scale(1); }} }}
@keyframes pulse {{ from {{ opacity:.65; transform:scale(.97); }} to {{ opacity:1; transform:scale(1.03); }} }}
@keyframes glow {{ from {{ transform: translateX(-2%) rotate(0); }} to {{ transform: translateX(2%) rotate(8deg); }} }}
@media (max-width: 600px) {{
  .stage {{ height: 520px; }}
  .content {{ padding: 20px; }}
  .repeat-grid {{ gap: 14px; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.001ms !important; animation-iteration-count: 1 !important; }}
}}
</style>
</head>
<body>
<div class="stage">
  <div class="{effect_class}">{effect_markup}</div>
  <div class="content">{name_markup}</div>
</div>
</body>
</html>
"""

components.html(document, height=610, scrolling=False)

st.caption(
    "Tip: Choose a display mode and an effect in the sidebar. The motion runs in CSS inside the preview, "
    "so it loops smoothly without repeatedly refreshing the Streamlit page."
)
