import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

st.set_page_config(
    page_title="Watermark Studio",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}

.main .block-container {
    background-color: #0d1117 !important;
    padding-top: 40px !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22, #0d1117) !important;
    border-right: 1px solid #30363d;
}

.stDownloadButton button {
    background-color: #238636 !important;
    color: white !important;
    border-radius: 8px !important;
    height: 46px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    width: 100% !important;
}

.stButton button {
    background-color: #238636 !important;
    color: white !important;
    border-radius: 6px !important;
    height: 38px !important;
    font-weight: 600 !important;
    width: 100%;
}

.stImage img {
    border-radius: 8px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.6);
}

.app-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 22px;
}

.app-title {
    font-size: 24px;
    font-weight: 800;
    color: #58a6ff;
}
</style>
""", unsafe_allow_html=True)

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_font(size):
    paths = [
        "arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def reset_defaults():
    st.session_state.size = 5
    st.session_state.opacity = 85
    st.session_state.position = "Bottom Right"

defaults = {
    "mode": "Text",
    "size": 5,
    "opacity": 85,
    "position": "Bottom Right",
    "text": "© Copyright",
    "color": "#FFFFFF",
    "color_draft": "#FFFFFF",
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

def apply_watermark(base, logo=None):
    base = base.convert("RGBA")
    w, h = base.size
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pad = int(min(w, h) * 0.03)
    alpha = int(st.session_state.opacity * 2.55)

    positions = {
        "Bottom Right": (1, 1),
        "Bottom Left": (0, 1),
        "Top Right": (1, 0),
        "Top Left": (0, 0),
        "Center": (0.5, 0.5),
    }

    px, py = positions[st.session_state.position]

    if st.session_state.mode == "Text":
        font_size = max(10, int(h * st.session_state.size / 100))
        font = get_font(font_size)
        bbox = draw.textbbox((0, 0), st.session_state.text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x = int(px * (w - tw - pad * 2) + pad)
        y = int(py * (h - th - pad * 2) + pad)

        rgb = tuple(int(st.session_state.color[i:i+2], 16) for i in (1, 3, 5))
        draw.text((x, y), st.session_state.text, font=font, fill=rgb + (alpha,))
    else:
        if logo is None:
            return base

        target_h = max(10, int(h * st.session_state.size / 100))
        ratio = logo.width / logo.height
        lw, lh = int(target_h * ratio), target_h
        logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)

        r, g, b, a = logo.split()
        a = a.point(lambda p: int(p * alpha / 255))
        logo.putalpha(a)

        x = int(px * (w - lw - pad * 2) + pad)
        y = int(py * (h - lh - pad * 2) + pad)

        overlay.paste(logo, (x, y), logo)

    return Image.alpha_composite(base, overlay)

with st.sidebar:
    if os.path.exists("logo-icon.png"):
        logo64 = img_to_base64("logo-icon.png")
        st.markdown(f"""
        <div class="app-header">
            <img src="data:image/png;base64,{logo64}" width="26">
            <div class="app-title">WATERMARK STUDIO</div>
        </div>
        """, unsafe_allow_html=True)

    src = st.file_uploader("SOURCE IMAGE", ["png", "jpg", "jpeg"])

    new_mode = st.segmented_control("MODE", ["Text", "Logo"], default=st.session_state.mode)
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode
        reset_defaults()

    logo_img = None
    if st.session_state.mode == "Logo":
        logo_file = st.file_uploader("LOGO FILE", ["png"])
        logo_img = Image.open(logo_file).convert("RGBA") if logo_file else None

    st.divider()

    if st.session_state.mode == "Text":
        st.session_state.text = st.text_input("TEXT", st.session_state.text)
        st.session_state.color_draft = st.color_picker("COLOR PICKER", st.session_state.color_draft)
        hex_input = st.text_input("HEX COLOR", st.session_state.color_draft)
        if st.button("✔ Apply Color"):
            if hex_input.startswith("#") and len(hex_input) == 7:
                st.session_state.color = hex_input.upper()
                st.session_state.color_draft = hex_input.upper()

    st.divider()

    st.session_state.position = st.selectbox(
        "POSITION",
        ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"]
    )

    st.caption(f"SIZE: {st.session_state.size}")
    c1, c2, c3 = st.columns([1, 4, 1])
    if c1.button("◀", key="size_minus"):
        st.session_state.size = max(1, st.session_state.size - 1)
    st.session_state.size = c2.slider("Size", 1, 100, st.session_state.size, label_visibility="collapsed")
    if c3.button("▶", key="size_plus"):
        st.session_state.size = min(100, st.session_state.size + 1)

    st.caption(f"OPACITY: {st.session_state.opacity}%")
    c1, c2, c3 = st.columns([1, 4, 1])
    if c1.button("◀", key="op_minus"):
        st.session_state.opacity = max(0, st.session_state.opacity - 1)
    st.session_state.opacity = c2.slider("Opacity", 0, 100, st.session_state.opacity, label_visibility="collapsed")
    if c3.button("▶", key="op_plus"):
        st.session_state.opacity = min(100, st.session_state.opacity + 1)

    if src:
        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        preview = apply_watermark(Image.open(src), logo_img if st.session_state.mode == "Logo" else None)
        buf = io.BytesIO()
        preview.convert("RGB").save(buf, format="JPEG", quality=95)
        st.download_button("💾 EXPORT IMAGE", buf.getvalue(), "watermarked.jpg", "image/jpeg")

if src:
    final_img = apply_watermark(Image.open(src), logo_img if st.session_state.mode == "Logo" else None)
    st.image(final_img, use_container_width=True)
else:
    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            height:70vh;
            font-size:24px;
            color:#6b7280;">
            Open an image to begin
        </div>
        """,
        unsafe_allow_html=True
    )
