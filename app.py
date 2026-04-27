import streamlit as st
import pandas as pd

st.set_page_config(page_title="바카라 알파고 시스템", layout="wide")

# 세션 상태 초기화 (데이터 유지용)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("🖥️ 바카라 알파고 시스템")

# 상단 버튼 레이아웃 (사진의 플레이어, 뱅커, 뒤로가기, 초기화)
top_col1, top_col2, top_col3, top_col4 = st.columns(4)
with top_col1:
    if st.button("🔵 플레이어", use_container_width=True):
        st.session_state.history.append("플레이어")
with top_col2:
    if st.button("🔴 뱅커", use_container_width=True):
        st.session_state.history.append("뱅커")
with top_col3:
    if st.button("↩️ 뒤로가기", use_container_width=True):
        if st.session_state.history: st.session_state.history.pop()
with top_col4:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.history = []
        st.session_state.step = 1

# 단계 선택 버튼 (1번~8번)
st.write("### 단계 선택")
step_cols = st.columns(8)
for i in range(1, 9):
    with step_cols[i-1]:
        if st.button(f"{i}번", key=f"step_{i}", use_container_width=True):
            st.session_state.step = i

# 중앙 데이터 표시창 (사진의 넓은 흰색 박스)
st.divider()
c1, c2 = st.columns([1, 3])
with c1:
    st.subheader("현재 설정")
    st.metric("선택된 단계", f"{st.session_state.step}번")
    st.write("**분석 결과:**")
    st.info("뱅커" if len(st.session_state.history) % 2 == 0 else "플레이어")

with c2:
    st.subheader("실시간 입력 기록")
    if st.session_state.history:
        record_df = pd.DataFrame(st.session_state.history, columns=["입력 결과"])
        st.table(record_df.tail(10)) # 최근 10개 기록 표시
    else:
        st.write("데이터가 없습니다. 버튼을 눌러 입력을 시작하세요.")

# 엑셀 다운로드 (기록 저장용)
if st.session_state.history:
    csv = record_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 현재 기록 엑셀 저장", csv, "baccarat_record.csv", "text/csv") 
