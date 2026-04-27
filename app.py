import streamlit as st
import pandas as pd

st.title("📋 사용자 관리 시스템 (Web)")

# 폼 만들기
with st.form("user_form"):
    st.subheader("정보 입력")
    name = st.text_input("이름")
    phone = st.text_input("전화번호")
    content = st.text_area("내용")
    
    submit = st.form_submit_button("엑셀 저장 및 전송")

if submit:
    st.success(f"{name}님 정보가 접수되었습니다.")
    # 간단한 표 보여주기
    df = pd.DataFrame([{"이름": name, "전화번호": phone, "내용": content}])
    st.table(df)
