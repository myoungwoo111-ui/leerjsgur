import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 버튼 간격 축소 및 중앙 정렬 핵심 CSS
st.markdown("""
    <style>
    /* 상단 여백 및 스크롤 차단 */
    header, footer {visibility: hidden;}
    .block-container { 
        padding: 10px !important; 
        max-width: 400px !important; /* 전체 폭을 좁게 제한하여 중앙으로 모음 */
        margin: auto !important; 
    }
    
    /* 가로 블록(행) 설정: 버튼 사이 간격 최소화 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important; /* 중앙 정렬 */
        gap: 2px !important; /* 버튼 사이 간격을 2픽셀로 축소 */
        width: 100% !important;
    }
    
    /* 각 컬럼의 불필요한 패딩 제거 */
    [data-testid="column"] {
        flex: 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        min-width: 0px !important;
    }

    /* 버튼 스타일: 엑셀 유저폼 느낌 */
    .stButton>button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 0px !important;
        border: 1px solid #444 !important;
        font-size: 13px !important;
        font-weight: bold !important;
        background-color: #f2f2f2 !important;
        padding: 0px !important;
    }

    /* 상단 정보 박스 */
    .info-box {
        border: 1px solid #444;
        text-align: center;
        padding: 8px;
        font-size: 20px;
        font-weight: bold;
        background: white;
        margin-bottom: 5px;
    }

    /* 차트 영역 */
    .chart-box {
        background: white;
        border: 1px solid #444;
        height: calc(100vh - 200px);
        padding: 8px;
        display: flex;
        gap: 4px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보창 ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- [중단] 메인 버튼 (4개 밀착 정렬) ---
# gap="small"을 추가하여 더 촘촘하게 만듭니다.
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

# --- [중단] 숫자 버튼 (8개 밀착 정렬) ---
s_cols = st.columns(8)
for i in range(1, 9):
    with s_cols[i-1]:
        st.button(str(i))

# --- [하단] 차트 영역 ---
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
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
