import streamlit as st

# 1. 화면 설정 (중앙 집중형을 위해 wide 대신 centered 검토 가능하나, 커스텀 CSS가 핵심)
st.set_page_config(layout="wide")

# 2. 강제 밀착 및 반응형 오류 수정 CSS
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 */
    .stApp { background-color: #f5f5f5; }
    
    /* 본문 컨테이너 폭 제한 (양 끝으로 찢어짐 방지) */
    .block-container {
        max-width: 500px !important; /* 모바일 최적 폭 */
        padding: 10px !important;
        margin: auto !important;
    }
    
    /* 가로 행(Row) 설정: 강제로 버튼들을 다닥다닥 붙임 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 방지 */
        gap: 2px !important; /* 미세한 간격 */
        width: 100% !important;
    }
    
    /* 각 칸(Column) 설정 */
    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* 버튼 스타일: 엑셀 유저폼 느낌 극대화 */
    .stButton>button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 2px !important;
        border: 1px solid #999 !important;
        background-color: #eeeeee !important;
        color: black !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 0px !important;
    }

    /* 상단 정보 박스 */
    .info-box {
        background: white;
        border: 1px solid #999;
        text-align: center;
        padding: 8px 0;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'history' not in st.session_state: st.session_state.history = []

# --- 상단 (2등분) ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- 메인 버튼 (4등분 밀착) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기"): st.session_state.history = []

# --- 단계 버튼 (8등분 밀착) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(f"{i}")

st.write("")

# --- 하단 기록장 ---
st.markdown("<p style='font-weight:bold; margin-bottom:5px;'>📊 실시간 기록 현황</p>", unsafe_allow_html=True)
record_html = f"""
<div style='background:white; border:1px solid #999; height:200px; padding:10px; overflow-x:auto; display:flex; gap:10px;'>
    {' '.join([f"<b style='color:{('blue' if x=='P' else 'red')}'>{x}</b>" for x in st.session_state.history])}
</div>
"""
st.markdown(record_html, unsafe_allow_html=True)
