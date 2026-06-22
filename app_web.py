import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บให้เหมาะสมกับโทรศัพท์มือถือ (Responsive Design)
st.set_page_config(
    page_title="SolidLearn Mobile Guide", 
    page_icon="🎯", 
    layout="centered"
)

# ตกแต่งดีไซน์เช็กลิสต์ (CSS) ขนาดใหญ่กดง่ายเหมาะกับนิ้วมือบนหน้าจอมือถือ
st.markdown("""
    <style>
    .stCheckbox {
        background-color: #343a40;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 10px;
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
sheet_id = "1vlsIREA8AV20KldPNCipfeAYSovRH3jGK4N1cA_mZl8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=2) # หน่วงเวลาจำข้อมูลแค่ 2 วินาทีเพื่อให้ดึงข้อมูลใหม่ทันทีเมื่อครูเปลี่ยนชีต
def load_data(url):
    try:
        return pd.read_csv(url, encoding='utf-8')
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล Sheets: {str(e)}")
        return None

df = load_data(sheet_url)

# ==========================================
# 📊 ประมวลผลข้อมูลและแสดงรูปภาพใบงานตามเลขข้อ
# ==========================================
if df is not None:
    # เคลียร์ช่องว่างชื่อคอลัมน์เพื่อความปลอดภัย
    df.columns = [c.strip() for c in df.columns]
    
    # 1. ดึงรายชื่อโจทย์จากคอลัมน์ที่ 1 (lesson_name)
    lesson_list = df.iloc[:, 0].dropna().tolist() 
    selected_lesson = st.selectbox("🎯 เลือกใบงานที่ต้องการทำ:", lesson_list)
    
    # ดึงข้อมูลแถวของโจทย์ที่นักเรียนเลือก
    lesson_data = df[df.iloc[:, 0] == selected_lesson].iloc[0]
    
    st.markdown("---")
    st.subheader(f"📌 {selected_lesson}")
    
    # 2. 📸 ระบบจับคู่รูปภาพจาก Google Sheets คอลัมน์ C (image_url) อัตโนมัติ
    try:
        # ดึงลำดับแถวจริงใน Google Sheets เพื่อใช้เป็นแผนสำรองในกรณีลืมพิมพ์เลขข้อ
        row_num = df[df.iloc[:, 0] == selected_lesson].index[0] + 2
        
        # คํานวณลิงก์ดึงภาพหลังบ้านจาก Google Sheets (ซึ่งกูเกิลแอบแคชภาพจากไดรฟ์ของครูไว้ให้แล้ว)
        # วิธีนี้เสถียรที่สุดในการดึงภาพที่ฝังหรือระบุพิกัดผ่านตารางชีต
        final_image_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/embed/oimg?id={sheet_id}&oid=1&row={row_num}&col=3"
        
        # แสดงผลรูปภาพแบบ Responsive ล้อมกรอบสีขาวให้เห็นมิติ Drawing ชัดเจน
        st.markdown(f"""
            <div style="display: flex; justify-content: center; background-color: #ffffff; padding: 10px; border-radius: 8px;">
                <img src="{final_image_url}" style="max-width: 100%; height: auto; border: 1px solid #ddd;" alt="กำลังโหลดรูปภาพใบงาน...">
            </div>
        """, unsafe_allow_html=True)
        st.caption("📱 แบบ Drawing ต้นแบบ (นักเรียนสามารถกางนิ้วบนจอมือถือเพื่อซูมดูขนาดได้)")
        
    except Exception as e:
        st.warning(f"⚠️ ไม่สามารถดึงรูปภาพได้: {str(e)}")
        
    st.markdown("---")
    st.subheader("📋 ขั้นตอนการฝึกทำตามสเต็ป")
    st.caption("ทำสเต็ปไหนใน SolidWorks เสร็จแล้ว ให้กดติ๊กถูกเพื่อไล่ขั้นตอนไปเรื่อยๆ")

    # 3. แยกข้อความขั้นตอนจากคอลัมน์ที่ 2 (คอลัมน์ B - steps) ด้วยเครื่องหมาย |
    raw_steps = lesson_data.iloc[1] 
    if isinstance(raw_steps, str):
        step_list = [s.strip() for s in raw_steps.split('|')]
        
        for index, step_text in enumerate(step_list):
            if step_text:
                st.checkbox(step_text, key=f"step_{index}")
                
        st.success("🎉 หากทำครบถ้วนทุกข้อแล้ว อย่าลืมตรวจเช็คความถูกต้องใน SolidWorks อีกรอบนะครับนักเรียน!")
    else:
        st.info("💡 ยังไม่ได้ใส่ข้อความขั้นตอนการสอนในคอลัมน์ที่ 2")