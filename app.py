import streamlit as st
import pandas as pd
import os

# 파일 이름 (반드시 GitHub에 올린 이름과 똑같이 적으세요!)
EXCEL_FILE = "바카라 알파고.xlsm" 

st.title("📊 현재 엑셀 데이터 현황")

# 1. 파일이 존재하는지 먼저 확인
if os.path.exists(EXCEL_FILE):
    try:
        df = pd.read_excel(EXCEL_FILE)
        st.dataframe(df)
        
        # 다운로드 버튼
        with open(EXCEL_FILE, "rb") as f:
            st.download_button(
                label="📥 엑셀 다운로드",
                data=f,
                file_name=EXCEL_FILE,
                mime="application/vnd.ms-excel.sheet.macroEnabled.12"
            )
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    # 파일이 없을 경우 에러 대신 안내 메시지 출력
    st.error(f"'{EXCEL_FILE}' 파일을 찾을 수 없습니다. GitHub에 올린 파일명과 일치하는지 확인해주세요.")
    st.info("현재 저장소에 있는 파일 목록을 확인해보세요.")
