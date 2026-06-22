import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้รองรับการแสดงผลบนมือถือได้อย่างเหมาะสม
st.set_page_config(
    page_title="SolidLearn Mobile Guide", 
    page_icon="🎯", 
    layout="centered"
)

# ตกแต่งดีไซน์หน้าจอ (CSS) ให้เช็กลิสต์ในมือถือตัวใหญ่และกดง่าย
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
# 🔌 เชื่อมต่อ Google Sheets (DB ล่าสุดของครู)
# ==========================================
sheet_id = "1vlsIREA8AV20KldPNCipfeAYSovRH3jGK4N1cA_mZl8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=2) # ลดการจำสติถิเหลือ 2 วินาที เพื่อให้ครูขยับรูปใน Google Sheets แล้วหน้าเว็บเปลี่ยนตามทันที
def load_data(url):
    try:
        return pd.read_csv(url, encoding='utf-8')
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {str(e)}")
        return None

df = load_data(sheet_url)

# ==========================================
# 📊 แสดงผลข้อมูลและรูปภาพจากคอลัมน์ที่ 4
# ==========================================
if df is not None:
    # เคลียร์ช่องว่างตรงชื่อคอลัมน์
    df.columns = [c.strip() for c in df.columns]
    
    # ดึงรายชื่อโจทย์จากคอลัมน์ที่ 1 (lesson_name)
    lesson_list = df.iloc[:, 0].dropna().tolist() 
    selected_lesson = st.selectbox("🎯 เลือกใบงานที่ต้องการทำ:", lesson_list)
    
    # ดึงข้อมูลแถวที่นักเรียนเลือก
    lesson_data = df[df.iloc[:, 0] == selected_lesson].iloc[0]
    
    st.markdown("---")
    st.subheader(f"📌 {selected_lesson}")
    
    # --- 📸 ส่วนแสดงรูปภาพจากคอลัมน์ที่ 4 (คอลัมน์ D) ---
    # หากครูใส่รูปไว้ในคอลัมน์ 4 ระบบจะประมวลผลดึงไฟล์รูปภาพต้นฉบับมาโชว์ให้อัตโนมัติ
    try:
        # ดึงเลขแถวจริงใน Google Sheets เพื่อระบุตำแหน่งรูปภาพ
        row_index = df[df.iloc[:, 0] == selected_lesson].index[0] + 2 
        
        # คํานวณลิงก์ดึงภาพพิเศษจากระบบหลังบ้าน Google Sheets คอลัมน์ที่ 4 (คอลัมน์ D)
        direct_image_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/embed/oimg?id={sheet_id}&oid=1&row={row_index}&col=4"
        
        st.image(
            direct_image_url, 
            caption="แบบ Drawing ต้นแบบจาก Google Sheets (กางนิ้วบนจอมือถือเพื่อซูมดูขนาดได้)", 
            use_container_width=True
        )
    except Exception:
        st.warning("⚠️ ไม่สามารถโหลดรูปภาพจากคอลัมน์ที่ 4 ได้ กรุณาตรวจสอบการใส่รูปใน Google Sheets")
        
    st.markdown("---")
    st.subheader("📋 ขั้นตอนการฝึกทำตามสเต็ป")
    st.caption("ทำสเต็ปไหนใน SolidWorks เสร็จแล้ว ให้กดติ๊กถูกเพื่อไล่ขั้นตอนไปเรื่อยๆ")

    # --- ส่วนที่ 3: แยกข้อความขั้นตอนสเต็ปการวาดด้วยเครื่องหมาย | ---
    # ดึงข้อมูลขั้นตอนจากคอลัมน์ที่ 2 (คอลัมน์ B)
    raw_steps = lesson_data.iloc[1] 
    if isinstance(raw_steps, str):
        # แยกข้อความเมื่อเจอเครื่องหมาย |
        step_list = [s.strip() for s in raw_steps.split('|')]
        
        for index, step_text in enumerate(step_list):
            if step_text:
                st.checkbox(step_text, key=f"step_{index}")
                
        st.success("🎉 หากทำครบถ้วนทุกข้อแล้ว อย่าลืมตรวจเช็คความถูกต้องและมิติของชิ้นงานใน SolidWorks อีกรอบนะครับนักเรียน!")
    else:
        st.info("💡 ยังไม่ได้ใส่ข้อความขั้นตอนการสอนในคอลัมน์ที่ 2")