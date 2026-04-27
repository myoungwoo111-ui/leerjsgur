import streamlit as st

# 1. 페이지 설정 및 스크롤 완전 차단
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    /* 전체 화면 고정 및 여백 제거 */
    header, footer {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        overflow: hidden !important; 
        height: 100vh; 
        background-color: #f0f0f0;
    }

    /* 버튼 컨테이너: 절대 찢어지지 않게 중앙 집중 */
    .custom-container {
        max-width: 380px; /* 폭을 좁혀서 중앙으로 모음 */
        margin: auto;
        padding-top: 10px;
    }

    /* 버튼 행: 무조건 가로 유지 */
    .btn-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100%;
        gap: 1px; /* 미세 간격 */
        margin-bottom: 2px;
    }

    /* 개별 버튼 디자인 (엑셀 스타일) */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 0px !important;
        border: 1px solid #444 !important;
        background-color: #e1e1e1 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        padding: 0px !important;
    }
    
    /* 숫자 버튼 전용 (더 촘촘하게) */
    .step-row [data-testid="column"] {
        flex: 1 !important;
    }

    /* 차트 영역 고정 */
    .baccarat-board {
        background: white;
        border: 1.5px solid #444;
        height: calc(100vh - 185px);
        margin-top: 5px;
        padding: 10px;
        display: flex;
        gap: 4px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .blue-p { color: blue; font-weight: bold; font-size: 18px; }
    .red-b { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [메인 레이아웃 박스 시작] ---
st.markdown('<div class="custom-container">', unsafe_allow_html=True)

# 1. 상단 정보창
t1, t2 = st.columns(2)
with t1: st.markdown("<div style='border:1px solid #444; background:white; text-align:center; padding:8px; font-size:20px; font-weight:bold;'>1,000</div>", unsafe_allow_html=True)
with t2: st.markdown("<div style='border:1px solid #444; background:white; text-align:center; padding:8px; font-size:20px; font-weight:bold;'>플레이어</div>", unsafe_allow_html=True)

# 2. 메인 버튼 4개 (가로 밀착)
row1 = st.columns(4)
with row1[0]: 
    if st.button("플"): st.session_state.history.append("P")
with row1[1]: 
    if st.button("뱅"): st.session_state.history.append("B")
with row1[2]: 
    if st.button("뒤로"): 
        if st.session_state.history: st.session_state.history.pop()
with row1[3]: 
    if st.button("초기"): st.session_state.history = []

# 3. 단계 버튼 8개 (가로 밀착)
row2 = st.columns(8)
for i in range(1, 9):
    with row2[i-1]:
        st.button(str(i))

# 4. 바카라 정석 차트 로직
def draw_chart(history):
    if not history: return "<div class='baccarat-board'></div>"
    cols, curr = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: curr.append(history[i])
        else: cols.append(curr); curr = [history[i]]
    cols.append(curr)
    
    html = "<div class='baccarat-board'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "blue-p" if item == "P" else "red-b"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(draw_chart(st.session_state.history), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
