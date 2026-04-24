import streamlit as st
import math

# ==========================
# 🎨 UI STYLE
# ==========================
st.markdown("""
<style>
body, .stApp {background:#000;color:#D4B200;}
h1,h2,h3{color:#D4B200!important;}
.result{background:#D4B200;padding:20px;border-radius:12px;color:black;font-weight:bold;font-size:26px;text-align:center;}
.result-box{background:#111;padding:10px;border-radius:10px;margin:6px 0;border:1px solid #D4B200;}
</style>
""", unsafe_allow_html=True)

st.title("حاسبة شركة beck")

mode = st.radio("", ["حساب الحروف", "حساب المونتاج", "حساب الكلادينج"])

# ==========================
# 🔤 الحروف + اللوجو
# ==========================
if mode == "حساب الحروف":

    if "rows" not in st.session_state:
        st.session_state.rows = [{"type":"حروف"}]

    def normalize_width(w):
        return 50 if w<=50 else math.ceil(w/50)*50

    def get_factor(h):
        if h<=60:return 1
        elif h<=70:return 1.5
        elif h<=100:return 2
        elif h<=150:return 3
        else:return 4

    total=0

    for i in range(len(st.session_state.rows)):

        st.markdown(f"### عنصر {i+1}")

        row_type=st.selectbox("نوع",["حروف","لوجو"],key=f"type{i}")
        w=st.number_input("عرض",key=f"w{i}",value=100.0)
        h=st.number_input("ارتفاع",key=f"h{i}",value=30.0)

        if row_type=="حروف":
            meters=(normalize_width(w)/100)*get_factor(h)

        else:
            M = max(w, h)

            if M <= 60:
                base = 1
            elif M <= 70:
                base = 1.5
            elif M <= 100:
                base = 2
            elif M <= 130:
                base = 2.5
            elif M <= 150:
                base = 3
            elif M <= 170:
                base = 4
            elif M <= 200:
                base = 5
            else:
                base = 6

            R = min(w, h) / M

            if R < 0.4:
                base -= 1
            elif R < 0.7:
                base -= 0.5
            elif R >= 0.9 and M > 120:
                base += 0.5

            meters = max(base, 1)
            meters = round(meters * 2) / 2

        total+=meters

        st.markdown(f"<div class='result-box'>{meters:,.2f} متر</div>",unsafe_allow_html=True)

    if st.button("➕ إضافة"):
        st.session_state.rows.append({"type":"حروف"})

    st.markdown(f"<div class='result'>{total:,.2f} متر</div>",unsafe_allow_html=True)

# ==========================
# 📦 المونتاج
# ==========================
if mode == "حساب المونتاج":

    w=st.number_input("عرض القطعة",value=30.0)
    h=st.number_input("ارتفاع القطعة",value=20.0)
    qty=st.number_input("عدد",value=1)

    gap=0.5

    sheets=[("تمن",25,130),("ربع",50,130),("نص",100,130),("لوح",200,130)]

    def fit(sw,sh):
        u_w=sw-1
        u_h=sh-1
        f1=(u_w//(w+gap))*(u_h//(h+gap))
        f2=(u_w//(h+gap))*(u_h//(w+gap))
        return int(max(f1,f2))

    data=[(n,fit(sw,sh)) for n,sw,sh in sheets]

    best=None
    waste=999999

    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    combo=[a,b,c,d]
                    total_pieces=sum(combo[i]*data[i][1] for i in range(4))
                    if total_pieces>=qty:
                        wst=total_pieces-qty
                        if wst<waste:
                            waste=wst
                            best=combo

    if best:
        names=["تمن","ربع","نص","لوح"]
        result=" + ".join([f"{best[i]} {names[i]}" for i in range(4) if best[i]>0])
        st.markdown(f"<div class='result'>{result}</div>",unsafe_allow_html=True)

# ==========================
# 🧱 الكلادينج
# ==========================
if mode == "حساب الكلادينج":

    def f(v):
        try:return float(v)
        except:return 0

    w=f(st.text_input("عرض","400"))
    h=f(st.text_input("ارتفاع","100"))
    d=f(st.text_input("عمق","10"))
    ds=f(st.text_input("دوسر","2"))

    fw=w+2*d+2*ds
    fh=h+2*d+2*ds

    base=fw*fh

    if "cols" not in st.session_state:
        st.session_state.cols=[{}]

    add=st.checkbox("أعمدة")

    col_area=0

    if add:
        for i in range(len(st.session_state.cols)):

            st.markdown(f"عمود {i+1}")

            fw=f(st.text_input(f"fw{i}","50"))
            fh=f(st.text_input(f"fh{i}","100"))
            s1w=f(st.text_input(f"s1w{i}","30"))
            s1h=f(st.text_input(f"s1h{i}","100"))
            s2w=f(st.text_input(f"s2w{i}","30"))
            s2h=f(st.text_input(f"s2h{i}","100"))

            cnt=st.number_input(f"عدد{i}",1,10,1)

            single=(fw*fh)+(s1w*s1h)+(s2w*s2h)
            col_area+=single*cnt

        if st.button("➕ عمود"):
            st.session_state.cols.append({})

    total=base+col_area

    st.markdown(f"<div class='result'>{total:,.2f}</div>",unsafe_allow_html=True)

    big=350*150
    small=320*125

    sol=[]

    for b in range(1,20):
        t=b*big
        if t>=total:sol.append(("كبير",b,0,t-total))

    for s in range(1,20):
        t=s*small
        if t>=total:sol.append(("صغير",0,s,t-total))

    for b in range(1,10):
        for s in range(1,10):
            t=(b*big)+(s*small)
            if t>=total:sol.append(("ميكس",b,s,t-total))

    sol=sorted(sol,key=lambda x:x[3])[:5]

    st.subheader("أفضل الحلول")

    for x in sol:
        st.markdown(f"<div class='result-box'>{x[0]} → كبير:{x[1]} صغير:{x[2]} | هالك:{x[3]:,.2f}</div>",unsafe_allow_html=True)
