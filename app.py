import streamlit as st
import joblib
import numpy as np
import os

# 1. ตั้งค่าหน้าเว็บ Streamlit (Wide Layout)
st.set_page_config(
    page_title="Iris Flower Prediction",
    page_icon="🌸",
    layout="wide"
)

# รายชื่อสายพันธุ์ดอกไม้ Iris (ตามลำดับ Target 0, 1, 2)
CLASS_NAMES = ['Setosa', 'Versicolor', 'Virginica']

# ดึงชื่อไฟล์โดยตรง (ระบบจะค้นหาไฟล์ในโฟลเดอร์เดียวกันอัตโนมัติ)
MODEL_NAME = 'iris_model.pkl'

# 2. ฟังก์ชันสำหรับโหลดโมเดลอัตโนมัติ
@st.cache_resource
def load_model_auto():
    # หาตำแหน่งโฟลเดอร์ปัจจุบันที่ app.py รันอยู่
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, MODEL_NAME)
    
    if os.path.exists(model_path):
        try:
            return joblib.load(model_path)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดขณะอ่านไฟล์โมเดล: {e}")
            return None
    else:
        st.error(f"ไม่พบไฟล์ `{MODEL_NAME}` ในโฟลเดอร์เดียวกับ app.py กรุณาตรวจสอบการวางไฟล์")
        return None

# โหลดโมเดลทันทีเมื่อเปิดหน้าเว็บ
model = load_model_auto()

# 3. ส่วนหัวของเว็บแอปพลิเคชัน
st.title("🌸 ระบบทำนายชนิดดอกไม้ Iris (Iris Flower Classification)")
st.markdown("ปรับค่าคุณลักษณะของดอกไม้ที่ฝั่งซ้าย เพื่อดูผลการทำนายที่ฝั่งขวา")
st.markdown("---")

# ตรวจสอบว่าโหลดโมเดลสำเร็จหรือไม่
if model is not None:
    # แบ่งหน้าเป็น 2 คอลัมน์ (ซ้าย: กรอกข้อมูล / ขวา: แสดงผล)
    col_input, col_result = st.columns([1, 1], gap="large")

    # --- คอลัมน์ซ้าย: แถบปรับค่า Features ---
    with col_input:
        st.subheader("⚙️ กำหนดค่าคุณลักษณะ (Input Features)")
        
        sepal_length = st.slider("Sepal Length (ความยาวกลีบเลี้ยง) [cm]", 4.0, 8.0, 5.4, 0.1)
        sepal_width  = st.slider("Sepal Width (ความกว้างกลีบเลี้ยง) [cm]", 2.0, 4.5, 3.4, 0.1)
        petal_length = st.slider("Petal Length (ความยาวกลีบดอก) [cm]", 1.0, 7.0, 1.5, 0.1)
        petal_width  = st.slider("Petal Width (ความกว้างกลีบดอก) [cm]", 0.1, 2.5, 0.2, 0.1)

    # --- คอลัมน์ขวา: ผลการประมวลผล ---
    with col_result:
        st.subheader("📊 ผลการทำนาย (Prediction Result)")
        
        # จัดรูปแบบข้อมูลนำเข้า
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        
        # ทำนายผล
        prediction = model.predict(input_data)[0]
        predicted_class = CLASS_NAMES[prediction]
        
        # แสดงสายพันธุ์ที่ทำนายได้
        st.success(f"### ผลลัพธ์: **Iris-{predicted_class}**")
        
        # แสดงเปอร์เซ็นต์ความน่าจะเป็น (ถ้าโมเดลรองรับ predict_proba)
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data)[0]
            st.write("**ระดับความมั่นใจของโมเดล (Probability):**")
            for i, name in enumerate(CLASS_NAMES):
                prob_pct = probabilities[i] * 100
                st.write(f"- **{name}**: {prob_pct:.2f}%")
                st.progress(float(probabilities[i]))