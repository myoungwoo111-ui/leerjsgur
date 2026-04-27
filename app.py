import streamlit as st
import pandas as pd

# 페이지 레이아웃 설정
st.set_page_config(page_title="바카라 알파고 시스템", layout="wide")

# 모바일에서도 버튼이 한눈에 보이도록 CSS 스타일 추가
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 50px; font-weight: bold; margin-bottom: -10px; }
    div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
    div[data-testid="stExpander"] { border: 1px solid #ccc; background-color: white; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화 (데이터 유지용)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("🖥️ 바카라 알파고 시스템")

# --- [상단] 현재 상태 요약 (사진의 1,000 / 플레이어 창) ---
st.divider()
res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
with res_col2:
    st.markdown("<h3 style='text-align: center; color: black; background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;'>현재 결과</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # 배팅금 계산 수식 (나중에 알려주시면 수정해 드릴게요!)
        bet_amount = 1000 if st.session_state.step == 1 else 3000 * st.session_state.step
        st.metric(label="배팅금", value=f"{bet_amount:,}원")
    with col2:
        # 분석 로직 (나중에 알려주시면 수정해 드릴게요!)
        recommend = "뱅커" if len(st.session_state.history) % 2 == 0 else "플레이어"
        st.metric(label="추천", value=recommend)

st.divider()

# --- [중단] 메인 컨트롤 버튼 (사진의 버튼 배열) ---
st.write("### 입력 컨트롤")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("플레이어", key="p_btn"):
        st.session_state.history.append("P")
with col2:
    if st.button("뱅커", key="b_btn"):
        st.session_state.history.append("B")
with col3:
    if st.button("뒤로가기", key="back_btn"):
        if st.session_state.history: st.session_state.history.pop()
with col4:
    if st.button("초기화", key="reset_btn"):
        st.session_state.history = []
        st.session_state.step = 1

# --- [하단] 단계 선택 버튼 (1번~8번, 4개씩 2줄 배치) ---
st.write("### 🔢 단계 선택")
for i in range(0, 8, 4):
    cols = st.columns(4)
    for j in range(4):
        step_num = i + j + 1
        if cols[j].button(f"{step_num}번", key=f"step_{step_num}"):
            st.session_state.step = step_num

# --- [최하단] 엑셀 기록창 완벽 구현 (Expander 활용) ---
st.divider()
st.subheader("📋 실시간 기록표")
with st.expander("입력 기록 보기", expanded=True):
    if st.session_state.history:
        # 기록을 표로 정리
        df = pd.DataFrame(st.session_state.history, columns=["입력 결과"])
        st.dataframe(df.tail(15)) # 최근 15개 기록 표시
        st.write(f"최근 기록: {' > '.join(st.session_state.history[-20:])}") # 텍스트로도 한눈에 표시
    else:
        st.write("데이터가 없습니다. 버튼을 눌러 입력을 시작하세요.")
