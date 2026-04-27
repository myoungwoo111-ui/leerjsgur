import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 강제 레이아웃 고정 CSS (모든 여백 0, 스크롤 차단)
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; height: 100vh; }

    /* 메인 컨테이너: 양옆 찢어짐 방지 */
    .main-wrap { max-width: 420px; margin: auto; padding: 5px; }

    /* 정보창 */
    .info-grid { display: flex; border: 1px solid #333; background: white; margin-bottom: 2px; }
    .info-item { flex: 1; text-align: center; padding: 8px; font-size: 18px; font-weight: bold; border-right: 1px solid #333; }

    /* 버튼 행 강제 정렬 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 1px !important;
        margin-bottom: 2px !important;
    }
    
    /* 개별 버튼: 여백 제거 및 밀착 */
    [data-testid="column"] { flex: 1 !important; padding: 0px !important; margin: 0px !important; min-width: 0px !important; }
    .stButton > button {
        width: 100% !important; height: 42px !important; padding: 0px !important;
        border-radius: 0px !important; border: 1.5px solid #444 !important;
        font-size: 13px !important; font-weight: bold !important;
        background-color: #f2f2f2 !important; color: black !important;
    }

    /* 차트 영역 */
    .chart-container {
        background: white; border: 1px solid #333; height: calc(100vh - 180px);
        padding: 8px; display: flex; gap: 3px; overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-val { color: blue; font-weight: bold; font-size: 18px; }
    .b-val { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보창 ---
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)
st.markdown("""
    <div class="info-grid">
        <div class="info-item">1,000</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# --- [중단] 가로 1열 (플, 뱅, 뒤로, 초기) ---
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

# --- [중단] 가로 2열 (1~8번 단계) ---
s_cols = st.columns(8)
for i in range(1, 9):
    with s_cols[i-1]:
        st.button(str(i))

# --- [하단] 차트 영역 (바카라 정석 로직) ---
def render_chart(history):
    if not history: return "<div class='chart-container'></div>"
    cols, curr = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: curr.append(history[i])
        else: cols.append(curr); curr = [history[i]]
    cols.append(curr)
    
    html = "<div class='chart-container'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "p-val" if item == "P" else "b-val"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
