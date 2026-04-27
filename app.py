import streamlit as st

# 1. 페이지 설정 (모바일 최적화)
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* 여백 및 메뉴 완전 제거 */
    header, footer {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    [data-testid="stAppViewContainer"] { overflow: hidden !important; background-color: #f0f0f0; }

    /* 모바일 버튼 컨테이너 (강제 가로 정렬) */
    .mobile-row {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 방지 */
        width: 100% !important;
        gap: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 버튼 스타일 (픽셀 단위로 모바일 최적화) */
    .stButton > button {
        width: 100% !important;
        height: 40px !important;
        border-radius: 0px !important;
        border: 0.5px solid #333 !important;
        background-color: #e1e1e1 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        color: black !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 정보창 (중앙 정렬) */
    .info-bar {
        display: flex;
        width: 100%;
        background: white;
        border-bottom: 1px solid #333;
    }
    .info-box {
        flex: 1;
        text-align: center;
        padding: 8px;
        font-size: 16px;
        font-weight: bold;
        border-right: 1px solid #333;
    }

    /* 바카라 보드 고정 */
    .baccarat-board {
        background: white;
        border: 1px solid #333;
        height: calc(100vh - 165px);
        margin: 5px;
        display: flex;
        overflow-x: auto;
        padding: 5px;
    }
    .board-col { display: flex; flex-direction: column; width: 18px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 14px; line-height: 1.2; }
    .b-mark { color: red; font-weight: bold; font-size: 14px; line-height: 1.2; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 레이아웃 시작 ---

# 1. 상단 정보창
st.markdown("""
    <div class="info-bar">
        <div class="info-box">1,000</div>
        <div class="info-box" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# 2. 메인 버튼 4개 (강제 1줄 배치)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("플"): st.session_state.history.append("P")
with c2: 
    if st.button("뱅"): st.session_state.history.append("B")
with c3: 
    if st.button("뒤로"): 
        if st.session_state.history: st.session_state.history.pop()
with c4: 
    if st.button("초기"): st.session_state.history = []

# 3. 단계 버튼 8개 (강제 1줄 배치)
s_cols = st.columns(8)
for i in range(1, 9):
    with s_cols[i-1]:
        st.button(str(i))

# 4. 바카라 정석 로직 (P-P 아래로, P-B 옆으로)
def render_baccarat(history):
    if not history: return "<div class='baccarat-board'></div>"
    cols, temp = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: temp.append(history[i])
        else: cols.append(temp); temp = [history[i]]
    cols.append(temp)
    
    html = "<div class='baccarat-board'>"
    for col in cols:
        html += "<div class='board-col'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_baccarat(st.session_state.history), unsafe_allow_html=True)
