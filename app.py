import streamlit as st

# 1. 페이지 레이아웃 설정
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 2. 강제 레이아웃 고정 CSS (모바일 반응형 차단)
st.markdown("""
    <style>
    /* 상단 메뉴 및 불필요한 여백 완전 제거 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding: 5px !important;
        max-width: 100% !important;
        margin: 0 !important;
    }

    /* 화면 스크롤 금지 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }

    /* 버튼 행: 무조건 가로 정렬, 여백 0 */
    .row-container {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 1px !important;
        margin-bottom: 2px !important;
    }

    /* 버튼 개별 스타일: 높이 조절 */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        padding: 0 !important;
        border-radius: 0px !important;
        border: 1px solid #333 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        background-color: #f8f9fa !important;
    }

    /* 상단 정보창 */
    .info-box {
        display: flex;
        border: 1px solid #333;
        background: white;
        margin-bottom: 5px;
        width: 100%;
    }
    .info-box div {
        flex: 1;
        text-align: center;
        padding: 8px;
        font-size: 18px;
        font-weight: bold;
    }

    /* 차트 영역: 바카라 정석 로직 전용 */
    .chart-container {
        background: white;
        border: 1px solid #333;
        height: calc(100vh - 180px); /* 버튼 높이 제외 나머지 꽉 채움 */
        padding: 10px;
        display: flex;
        gap: 4px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-txt { color: blue; font-weight: bold; font-size: 18px; }
    .b-txt { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태
if 'history' not in st.session_state: st.session_state.history = []

# --- [1] 상단 정보창 ---
st.markdown("""
    <div class="info-box">
        <div style="border-right: 1px solid #333;">1,000</div>
        <div>플레이어</div>
    </div>
""", unsafe_allow_html=True)

# --- [2] 첫 번째 줄: 메인 버튼 4개 (플, 뱅, 뒤로, 초기) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기"): st.session_state.history = []

# --- [3] 두 번째 줄: 단계 버튼 8개 (1~8) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(str(i))

# --- [4] 하단: 바카라 정석 차트 로직 ---
def draw_baccarat_chart(history):
    if not history: return "<div class='chart-container'></div>"
    
    cols = []
    curr = [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            curr.append(history[i])
        else:
            cols.append(curr)
            curr = [history[i]]
    cols.append(curr)
    
    html = "<div class='chart-container'>"
    for c in cols:
        html += "<div class='chart-col'>"
        for item in c:
            cls = "p-txt" if item == "P" else "b-txt"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(draw_baccarat_chart(st.session_state.history), unsafe_allow_html=True)
