import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าเว็บให้รองรับการแสดงผลบนมือถือได้อย่างเหมาะสม
st.set_page_config(
    page_title="SolidLearn Mobile Guide", 
    page_icon="🎯", 
    layout="centered" # จัดหน้าให้อยู่ตรงกลาง เหมาะกับจอมือถือ
)

# สไตล์ตกแต่งเพิ่มเติม (CSS) เพื่อให้เช็กลิสต์ในมือถือตัวใหญ่ขึ้นและกดง่ายเหมาะกับนิ้วมือ
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
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧱 SolidLearn Mobile Guide")
st.write("📱 สื่อการสอนเขียนแบบสำหรับเปิดบนมือถือควบคู่การเรียน")

# ==========================================
# 🔌 เชื่อมต่อ Google Sheets (DB)
# ==========================================
# 🛑 สแตนด์บายลิงก์ Google Sheets ของคุณครู 🛑
sheet_url = "https://docs.google.com/spreadsheets/d/1vlsIREA8AV20KldPNCipfeAYSovRH3jGK4N1cA_mZl8/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=5) # จำค่าไว้แค่ 5 วินาที เพื่อให้ดึงข้อมูลใหม่จาก Google Sheets ได้ไวตอนครูอัปเดตโจทย์
def load_data(url):
    try:
        # บังคับอ่านเข้ารหัสแบบ utf-8 เพื่อรองรับภาษาไทยใน Sheets
        return pd.read_csv(url, encoding='utf-8')
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {str(e)}")
        return None

df = load_data(sheet_url)

# ==========================================
# 📊 แสดงผลและประมวลผลข้อมูล
# ==========================================
if df is not None:
    # เคลียร์ช่องว่างตรงชื่อคอลัมน์เพื่อความปลอดภัยไว้ก่อน
    df.columns = [c.strip() for c in df.columns]
    
    # 🕵️‍♂️ ตัวตรวจจับข้อผิดพลาด: ถ้าใน Google Sheets ของครู พิมพ์ชื่อหัวคอลัมน์ไม่ตรงกับในโค้ด
    if 'lesson_name' not in df.columns:
        st.warning("⚠️ ตรวจพบปัญหา! ระบบเชื่อมต่อ Google Sheets ได้แล้ว แต่หาคอลัมน์ชื่อ 'lesson_name' ไม่เจอ")
        st.write("👉 หัวคอลัมน์ที่ระบบอ่านได้จากตารางของครูในปัจจุบันคือ:")
        st.code(list(df.columns))
        st.write("💡 วิธีแก้: โปรดกลับไปเปลี่ยนชื่อหัวคอลัมน์ในแถวแรก (Row 1) ของ Google Sheets ให้เป็นคำว่า `lesson_name`, `image_url` และ `steps` ตามลำดับครับ")
        st.stop() # หยุดการทำงานชั่วคราวเพื่อให้แก้ไขจุดนี้ก่อน

    # --- ส่วนที่ 1: ดึงรายชื่อโจทย์มาทำ Dropdown ---
    lesson_list = df['lesson_name'].dropna().tolist()
    selected_lesson = st.selectbox("🎯 เลือกใบงานที่ต้องการทำ:", lesson_list)
    
    # ดึงข้อมูลของโจทย์แถวที่นักเรียนเลือก
    lesson_data = df[df['lesson_name'] == selected_lesson].iloc[0]
    
    st.markdown("---")
    st.subheader(f"📌 {selected_lesson}")
    
    # --- ส่วนที่ 2: แสดงรูปภาพใบงาน (Blueprint) ---
    if 'image_url' in df.columns and pd.notna(lesson_data['image_url']) and str(lesson_data['image_url']).startswith('http'):
        st.image(
            lesson_data['image_url'], 
            caption="แบบ Drawing ต้นแบบ (คุณสามารถใช้นิ้วซูมหรือกดค้างเพื่อบันทึกรูปภาพได้)", 
            use_container_width=True
        )
    else:
        st.warning("⚠️ ยังไม่มีรูปภาพใบงานสำหรับโจทย์ข้อนี้ หรือลิงก์รูปภาพไม่ถูกต้อง")
        
    st.markdown("---")
    st.subheader("📋 ขั้นตอนการฝึกทำตามสเต็ป")
    st.caption("ทำสเต็ปไหนใน SolidWorks เสร็จแล้ว ให้กดติ๊กถูกเพื่อไล่ขั้นตอนไปเรื่อยๆ")

    # --- ส่วนที่ 3: แยกข้อความขั้นตอนสเต็ปการวาดด้วยเครื่องหมาย | ---
    if 'steps' in df.columns:
        raw_steps = lesson_data['steps']
        if isinstance(raw_steps, str):
            # แยกข้อความเมื่อเจอเครื่องหมาย |
            step_list = [s.strip() for s in raw_steps.split('|')]
            
            # วาด Checkbox ขนาดใหญ่สำหรับกดเลือกบนหน้าจอมือถือ
            for index, step_text in enumerate(step_list):
                if step_text:
                    st.checkbox(step_text, key=f"step_{index}")
                    
            st.success("🎉 หากทำครบถ้วนทุกข้อแล้ว อย่าลืมตรวจเช็คความถูกต้องและมิติของชิ้นงานใน SolidWorks อีกรอบนะครับนักเรียน!")
        else:
            st.info("💡 ยังไม่ได้ใส่ข้อความขั้นตอนในคอลัมน์ steps")
