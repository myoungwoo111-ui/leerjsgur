import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 페이지 설정
st.set_page_config(page_title="사용자 관리 시스템 (엑셀 연동)", layout="centered")

# 저장된 엑셀 파일 이름 (사용자님이 올린 파일명과 일치해야 함)
EXCEL_FILE = "바카라 아르고.xlsx.xlsm"

st.title("📊 엑셀 데이터 연동 시스템")

# 엑셀 파일이 있는지 확인하고 데이터 불러오기
if os.path.exists(EXCEL_FILE):
    try:
        # 시트 이름이 다를 경우 수정이 필요할 수 있습니다.
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
        df = pd.DataFrame(columns=["일시", "이름", "전화번호", "내용"])
else:
    st.warning("저장소에 엑셀 파일이 없습니다. 새로 생성을 시작합니다.")
    df = pd.DataFrame(columns=["일시", "이름", "전화번호", "내용"])

# 입력 폼
with st.form("user_form", clear_on_submit=True):
    st.subheader("새 정보 입력")
    name = st.text_input("이름")
    phone = st.text_input("전화번호")
    content = st.text_area("내용")
    submit = st.form_submit_button("엑셀에 저장")

if submit:
    if name and phone:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = {"일시": now, "이름": name, "전화번호": phone, "내용": content}
        
        # 데이터 추가
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # 엑셀 파일로 다시 저장 (웹 서버 환경에서는 임시 저장입니다)
        df.to_excel(EXCEL_FILE, index=False)
        st.success(f"{name}님의 정보가 엑셀 로직에 추가되었습니다.")
    else:
        st.error("필수 정보를 입력해주세요.")

# 현재 데이터 표시
st.divider()
st.subheader("현재 엑셀 데이터 현황")
st.dataframe(df)

# 수정된 엑셀 다운로드 버튼
with open(EXCEL_FILE, "rb") as f:
    st.download_button(
        label="📥 업데이트된 엑셀 파일 다운로드",
        data=f,
        file_name=f"updated_{EXCEL_FILE}",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
