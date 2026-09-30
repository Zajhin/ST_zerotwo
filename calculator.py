import streamlit as st

# หัวข้อแอป
st.title("Simple Calculator App")

# ช่องสำหรับกรอกตัวเลข 2 ค่า
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# ตัวเลือกการคำนวณ (Add, Subtract, Multiply, Divide)
operation = st.selectbox(
    "Select operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

# ปุ่มกดคำนวณและแสดงผลลัพธ์
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
        st.success(f"Result: {num1} + {num2} = {result}")
    elif operation == "Subtract":
        result = num1 - num2
        st.success(f"Result: {num1} - {num2} = {result}")
    elif operation == "Multiply":
        result = num1 * num2
        st.success(f"Result: {num1} × {num2} = {result}")
    elif operation == "Divide":
        if num2 != 0:
            result = num1 / num2
            st.success(f"Result: {num1} ÷ {num2} = {result}")
        else:
            st.error("Error: Cannot divide by zero!")