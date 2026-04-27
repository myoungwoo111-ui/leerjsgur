import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 모든 간섭을 차단하고 엑셀 유저폼을 그대로 박아넣는 CSS
st.markdown("""
    <style>
    /* 화면 고정 및 스크롤 차단 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
        margin: 0; padding: 0;
    }
    .block-container { 
        padding: 5px !important; 
        max-width: 420px !important; 
        margin: auto !important; 
    }
    
    /* 버튼 컨테이너: 절대 세로로 안 변하게 고정 */
    .btn-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100%;
        margin-bottom: 2px;
    }
    
    /* 개별 버튼 스타일 */
    .custom-btn {
        flex: 1;
        height: 45px;
        border: 0.5px solid #444;
        background-color: #f0f0f0;
        font-size: 13px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        user-select: none;
    }
    .custom-btn:active { background-color: #ddd; }

    /* 정보창 */
    .info-box {
        display: flex;
        width: 100%;
        border: 1px solid #444;
        background: white;
        margin-bottom: 5px;
    }
    .info-item {
        flex: 1;
        padding: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        border-right: 1px solid #444;
    }

    /* 차트 영역 */
    .chart-area {
        background: white;
        border: 1px solid #444;
        height: calc(100vh - 200px);
        padding: 10px;
        display: flex;
        gap: 5px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보창 ---
st.markdown(f"""
    <div class="info-box">
        <div class="info-item">1,000</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# --- [중단] 가로 1열 버튼 (HTML 버튼으로 강제 구현) ---
# Streamlit 버튼 대신 HTML/CSS로 한 줄에 4개 배치
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기"): st.session_state.history = []

# --- [중단] 가로 2열 단계 버튼 (1~8번) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(str(i))

# --- [하단] 바카라 차트 로직 ---
def render_chart(history):
    if not history: return "<div class='chart-area'></div>"
    columns = []
    current_col = [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            columns.append(current_col)
            current_col = [history[i]]
    columns.append(current_col)
    
    html = "<div class='chart-area'>"
    for col in columns:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
