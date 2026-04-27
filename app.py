import streamlit as st

# 1. 페이지 레이아웃 및 여백 완전 제거
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    /* 상단 헤더 및 기본 패딩 제거 */
    header, footer {visibility: hidden;}
    .block-container { padding: 5px !important; max-width: 100% !important; margin: 0 !important; }
    
    /* 화면 스크롤 금지 */
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; height: 100vh; }

    /* HTML 버튼 행 컨테이너: 무조건 가로 정렬 & 다닥다닥 밀착 */
    .btn-row {
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
        gap: 0px !important; /* 간격 0 */
        margin-bottom: 2px !important;
    }
    
    /* 개별 버튼 스타일 */
    .btn-item {
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
    }
    
    /* 상단 정보창 */
    .info-box { display: flex; border: 1px solid #444; margin-bottom: 5px; width: 100%; background: white; }
    .info-item { flex: 1; text-align: center; padding: 10px; font-size: 18px; font-weight: bold; border-right: 1px solid #444; }

    /* 차트 영역 */
    .chart-box {
        background: white; border: 1px solid #444; height: calc(100vh - 180px);
        padding: 5px; display: flex; gap: 5px; overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- [1] 상단 정보창 ---
st.markdown(f"""
    <div class="info-box">
        <div class="info-item">1,000</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# --- [2] 가로 1열 버튼 (4개 밀착) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기"): st.session_state.history = []

# --- [3] 가로 2열 버튼 (8개 밀착) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(str(i))

# --- [4] 하단 차트 로직 ---
def render_chart(history):
    if not history: return "<div class='chart-box'></div>"
    cols, curr = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: curr.append(history[i])
        else: cols.append(curr); curr = [history[i]]
    cols.append(curr)
    html = "<div class='chart-box'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            color = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{color}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
