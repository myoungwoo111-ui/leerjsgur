import streamlit as st
import pandas as pd

# 1. 페이지 설정: 화면을 넓게 쓰고 제목 숨김
st.set_page_config(page_title="AlphaGo", layout="wide")

# 2. 디자인 커스텀: 버튼 크기를 줄이고 가로로 촘촘하게 배치
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 45px; padding: 0px; font-size: 14px !important; margin-bottom: -15px; }
    div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
    .main-box { background-color: #f0f0f0; border: 2px solid #999; padding: 10px; text-align: center; font-size: 24px; font-weight: bold; color: black; min-height: 60px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 1

# --- [상단] 핵심 정보창 (사진의 상단 박스 2개) ---
col_info1, col_info2 = st.columns(2)
with col_info1:
    bet_val = "18,000" if st.session_state.step == 6 else "1,000" # 엑셀 값 예시
    st.markdown(f"<div class='main-box'>{bet_val}</div>", unsafe_allow_html=True)
with col_info2:
    recom_val = "뱅커" if len(st.session_state.history) % 2 == 0 else "플레이어"
    st.markdown(f"<div class='main-box'>{recom_val}</div>", unsafe_allow_html=True)

st.write("") # 간격 조절

# --- [중단] 메인 버튼 4개 (가로 한 줄 배치) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플레이어"): st.session_state.history.append("P")
if c2.button("뱅커"): st.session_state.history.append("B")
if c3.button("뒤로가기"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기화"): 
    st.session_state.history = []
    st.session_state.step = 1

# --- [중단] 단계 버튼 8개 (가로 한 줄로 촘촘하게) ---
st.write("")
step_cols = st.columns(8)
for i in range(1, 9):
    if step_cols[i-1].button(f"{i}번"):
        st.session_state.step = i

# --- [하단] 기록창 (사진의 큰 화이트 박스) ---
st.markdown("### 📋 기록현황")
# 엑셀 유저폼 느낌을 주기 위해 높이가 고정된 텍스트 영역 또는 테이블 사용
record_text = " ".join(st.session_state.history)
st.text_area(label="Record Board", value=record_text, height=150, label_visibility="collapsed")

# 최근 5개 로그 출력 (선택 사항)
if st.session_state.history:
    st.caption(f"최근 입력: {' > '.join(st.session_state.history[-5:])}")
