import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้รองรับการแสดงผลบนมือถือได้อย่างเหมาะสม
st.set_page_config(
    page_title="SolidLearn Mobile Guide", 
    page_icon="🎯", 
    layout="centered" # จัดหน้าให้อยู่ตรงกลาง เหมาะกับจอมือถือ
)

# สไตล์ตกแต่งเพิ่มเติม (CSS) เพื่อให้เช็กลิสต์ในมือถือตัวใหญ่ขึ้นและกดง่าย
st.markdown("""
    <style>
    .stCheckbox {
        background-color: #343a40;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 5px solid #00ffcc;
    }
    .stCheckbox label {
        color: white !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧱 SolidLearn Mobile Guide")
st.write("📱 สื่อการสอนเขียนแบบสำหรับเปิดบนมือถือควบคู่การเรียน")

# ==========================================
# 🔌 เชื่อมต่อ Google Sheets (DB)
# ==========================================
# 🛑 ให้ครูนำลิงก์ Google Sheets ของครูมาวางแทนที่ตรงนี้ครับ 🛑
# (ต้องเปลี่ยนคำว่า /edit... ที่ท้ายลิงก์ ให้เป็น /gviz/tq?tqx=out:csv แทน)
sheet_url = "https://docs.google.com/spreadsheets/d/1vlsIREA8AV20KldPNCipfeAYSovRH3jGK4N1cA_mZl8/edit?usp=sharing"

@st.cache_data(ttl=60) # รีเฟรชข้อมูลจาก Google Sheet ทุกๆ 60 วินาที
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error("ไม่สามารถเชื่อมต่อฐานข้อมูล Google Sheets ได้ กรุณาเช็กลิสต์การเปิดแชร์")
        return None

df = load_data(sheet_url)

if df is not None:
    # --- ส่วนที่ 1: ดึงรายชื่อโจทย์มาทำ Dropdown ---
    lesson_list = df['lesson_name'].tolist()
    selected_lesson = st.selectbox("🎯 เลือกใบงานที่ต้องการทำ:", lesson_list)
    
    # ดึงข้อมูลของโจทย์ที่เลือก
    lesson_data = df[df['lesson_name'] == selected_lesson].iloc[0]
    
    st.markdown("---")
    st.subheader(f"📌 {selected_lesson}")
    
    # --- ส่วนที่ 2: แสดงรูปภาพใบงาน (Blueprint) ---
    if pd.notna(lesson_data['image_url']) and str(lesson_data['image_url']).startswith('http'):
        st.image(
            lesson_data['image_url'], 
            caption="แบบ Drawing ต้นแบบ (กดค้างที่รูปเพื่อบันทึกหรือขยายได้)", 
            use_container_width=True
        )
    else:
        st.warning("⚠️ ยังไม่มีรูปภาพใบงานสำหรับโจทย์ข้อนี้")
        
    st.markdown("---")
    st.subheader("📋 ขั้นตอนการฝึกทำตามสเต็ป")
    st.caption("ทำสเต็ปไหนเสร็จแล้ว ให้กดติ๊กถูกเพื่อไล่ขั้นตอน")

    # --- ส่วนที่ 3: แยกข้อความยาวๆ ออกมาเป็นข้อย่อยด้วยเครื่องหมาย | ---
    raw_steps = lesson_data['steps']
    if isinstance(raw_steps, str):
        # แยกข้อความเมื่อเจอเครื่องหมาย |
        step_list = [s.strip() for s in raw_steps.split('|')]
        
        # วาด Checkbox ขนาดใหญ่สำหรับกดบนมือถือ
        for index, step_text in enumerate(step_list):
            if step_text:
                st.checkbox(step_text, key=f"step_{index}")
                
    st.success("🎉 ทำครบถ้วนแล้ว อย่าลืมตรวจเช็คความถูกต้องใน SolidWorks อีกรอบนะครับ!")