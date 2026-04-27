import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="사용자 관리 시스템", layout="centered")

# 데이터 저장을 위한 세션 상태 초기화
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = pd.DataFrame(columns=["일시", "이름", "전화번호", "내용"])

st.title("📋 사용자 관리 시스템 (Web)")

# 입력 폼
with st.form("user_form", clear_on_submit=True):
    st.subheader("정보 입력")
    name = st.text_input("이름")
    phone = st.text_input("전화번호")
    content = st.text_area("내용")
    
    submit = st.form_submit_button("정보 전송")

if submit:
    if name and phone:
        # 데이터 생성 및 추가
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = {"일시": now, "이름": name, "전화번호": phone, "내용": content}
        
        # 세션에 데이터 누적 저장
        st.session_state['user_data'] = pd.concat([st.session_state['user_data'], pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"{name}님의 정보가 전송되었습니다.")
    else:
        st.error("이름과 전화번호를 입력해주세요.")

# 누적된 데이터 보여주기
if not st.session_state['user_data'].empty:
    st.divider()
    st.subheader("현재까지 접수된 명단")
    st.dataframe(st.session_state['user_data'])

    # 엑셀(CSV) 다운로드 버튼 추가
    csv = st.session_state['user_data'].to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 전체 명단 엑셀로 다운로드",
        data=csv,
        file_name=f"user_list_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
