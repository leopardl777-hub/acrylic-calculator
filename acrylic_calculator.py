import streamlit as st
import math

# ==========================
# 🎨 إعداد الصفحة
# ==========================
st.set_page_config(page_title="Beck Acrylic", layout="wide")

# ==========================
# 🎨 UI STYLE
# ==========================
st.markdown("""
<style>
body, .stApp {background:#000;color:#D4B200;}
h1,h2,h3{color:#D4B200!important;}

.section {
    background:#111;
    padding:20px;
    border-radius:12px;
    margin-bottom:15px;
    border:1px solid #333;
}

.result {
    background:#D4B200;
    padding:20px;
    border-radius:12px;
    color:black;
    font-weight:bold;
    font-size:30px;
    text-align:center;
}

.small {
    color:#aaa;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# 🏷️ العنوان
# ==========================
st.title("Beck Acrylic System")

# ==========================
# 🔘 اختيار النوع
# ==========================
st.markdown("### اختر نوع الحساب")

mode = st.radio(
    "",
    ["🔤 حروف", "🟩 لوجو", "🧱 كلادينج"],
    horizontal=True
)

# ==========================
# 🔤 حروف
# ==========================
if mode == "🔤 حروف":

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        w = st.number_input("عرض الحرف (سم)", value=100.0)
        h = st.number_input("ارتفاع الحرف (سم)", value=50.0)
        st.markdown("</div>", unsafe_allow_html=True)

    def get_factor(h):
        if h <= 60: return 1
        elif h <= 70: return 1.5
        elif h <= 100: return 2
        elif h <= 150: return 3
        else: return 4

    meters = (w / 100) * get_factor(h)

    st.markdown(f"<div class='result'>{meters:.2f} متر طولي</div>", unsafe_allow_html=True)

# ==========================
# 🟩 لوجو
# ==========================
if mode == "🟩 لوجو":

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        w = st.number_input("عرض اللوجو (سم)", value=100.0)
        h = st.number_input("ارتفاع اللوجو (سم)", value=100.0)
        st.markdown("</div>", unsafe_allow_html=True)

    M = max(w, h)

    # Base
    if M <= 60: base = 1
    elif M <= 70: base = 1.5
    elif M <= 100: base = 2
    elif M <= 130: base = 2.5
    elif M <= 150: base = 3
    elif M <= 170: base = 4
    elif M <= 200: base = 5
    else: base = 6

    # شكل
    R = min(w, h) / M

    if R < 0.4:
        base -= 1
    elif R < 0.7:
        base -= 0.5
    elif R >= 0.9 and M > 120:
        base += 0.5

    meters = max(base, 1)
    meters = round(meters * 2) / 2

    st.markdown(f"<div class='result'>{meters:.2f} متر طولي</div>", unsafe_allow_html=True)

# ==========================
# 🧱 كلادينج
# ==========================
if mode == "🧱 كلادينج":

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        w = st.number_input("عرض (سم)", value=400.0)
        h = st.number_input("ارتفاع (سم)", value=100.0)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        qty = st.number_input("عدد", value=10)
        depth = st.number_input("دوسر", value=2.0)
        st.markdown("</div>", unsafe_allow_html=True)

    total = (w * h * qty) / 10000  # متر مربع

    st.markdown(f"<div class='result'>{total:,.2f} متر مربع</div>", unsafe_allow_html=True)

# ==========================
# 🧠 Footer
# ==========================
st.markdown("<div class='small'>Developed for Beck Advertising</div>", unsafe_allow_html=True)
