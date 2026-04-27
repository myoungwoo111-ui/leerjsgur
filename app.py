import streamlit as st

# 1. 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 2. 모바일 최적화 및 차트 전용 CSS
st.markdown("""
    <style>
    /* 전체 폭을 모바일 사이즈로 고정하여 찢어짐 방지 */
    .block-container { 
        max-width: 400px !important; 
        padding: 10px 5px !important; 
        margin: auto !important; 
    }
    
    /* 가로 버튼 강제 밀착 (사이 간격 0) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important;
    }
    
    /* 컬럼 여백 제거 및 너비 균등 배분 */
    [data-testid="column"] {
        flex: 1 !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 버튼 스타일: 엑셀 유저폼 디자인 */
    .stButton>button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 0px !important;
        border: 0.5px solid #444 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        background-color: #f0f0f0 !important;
    }

    /* 상단 정보창 */
    .info-box {
        border: 1px solid #444;
        text-align: center;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
        background: white;
        margin-bottom: 5px;
    }

    /* 차트 영역: 가로 스크롤 가능 */
    .chart-area {
        background: white;
        border: 1px solid #444;
        min-height: 200px;
        padding: 10px;
        display: flex;
        flex-direction: row;
        gap: 5px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-val { color: blue; font-weight: bold; font-size: 16px; }
    .b-val { color: red; font-weight: bold; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- 상단 정보 (2열) ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- 메인 버튼 (4열 밀착) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("뒤"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초"): st.session_state.history = []

# --- 단계 버튼 (8열 밀착) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(str(i))

st.write("")

# --- 바카라 차트 로직 ---
def draw_chart(history):
    if not history: return "<div class='chart-area'>기록 없음</div>"
    
    # 묶음 생성 로직: 같으면 아래로, 틀리면 옆으로
    groups = []
    if history:
        temp = [history[0]]
        for i in range(1, len(history)):
            if history[i] == history[i-1]:
                temp.append(history[i])
            else:
                groups.append(temp)
                temp = [history[i]]
        groups.append(temp)
    
    html = "<div class='chart-area'>"
    for group in groups:
        html += "<div class='chart-col'>"
        for item in group:
            color_class = "p-val" if item == "P" else "b-val"
            html += f"<span class='{color_class}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(draw_chart(st.session_state.history), unsafe_allow_html=True)
