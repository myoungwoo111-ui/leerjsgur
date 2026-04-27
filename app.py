import streamlit as st
import pandas as pd

# 페이지 레이아웃을 넓게 설정
st.set_page_config(page_title="바카라 알파고", layout="wide", initial_sidebar_state="collapsed")

# 모바일에서도 한눈에 보이도록 CSS 스타일 추가
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 18px !important; font-weight: bold; margin-bottom: -10px; }
    div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = "1번"

# --- [상단] 현재 상태 요약 (엑셀의 핵심 정보창) ---
st.title("🖥️ 바카라 알파고 시스템")
res_col1, res_col2, res_col3 = st.columns(3)
with res_col1:
    st.metric("현재 단계", st.session_state.step)
with res_col2:
    # 엑셀 로직에 따른 다음 배팅 추천 (예시)
    st.metric("배팅 추천", "뱅커" if len(st.session_state.history) % 2 == 0 else "플레이어")
with res_col3:
    st.metric("배팅 금액", "4,000" if st.session_state.step == "1번" else "12,000")

st.divider()

# --- [중단] 메인 컨트롤 버튼 (플레이어/뱅커 2열 배치) ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔵 플레이어", key="p_btn"): st.session_state.history.append("P")
with col2:
    if st.button("🔴 뱅커", key="b_btn"): st.session_state.history.append("B")

# 뒤로가기/초기화 (작은 버튼으로 배치)
sub_col1, sub_col2 = st.columns(2)
with sub_col1:
    if st.button("↩️ 뒤로가기"): 
        if st.session_state.history: st.session_state.history.pop()
with sub_col2:
    if st.button("🔄 초기화"): 
        st.session_state.history = []
        st.session_state.step = "1번"

# --- [하단] 단계 선택 버튼 (4열씩 2줄 배치) ---
st.write("### 🔢 단계 선택")
step_list = ["1번", "2번", "3번", "4번", "5번", "6번", "7번", "8번"]
for i in range(0, 8, 4):
    cols = st.columns(4)
    for j in range(4):
        step_name = step_list[i+j]
        if cols[j].button(step_name):
            st.session_state.step = step_name

# --- [최하단] 기록 테이블 ---
with st.expander("📊 입력 기록 보기", expanded=True):
    if st.session_state.history:
        st.write(f"최근 기록: {' > '.join(st.session_state.history[-10:])}")
