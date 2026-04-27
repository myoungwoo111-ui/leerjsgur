import streamlit as st

# 1. 페이지 설정 및 스크롤 차단
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; height: 100vh; }

    /* 전체 컨테이너를 모바일 폭에 맞춤 */
    .main-wrapper { max-width: 450px; margin: auto; padding: 5px; }

    /* 상단 정보창 */
    .info-grid { display: flex; width: 100%; border: 1px solid #333; background: white; margin-bottom: 5px; }
    .info-grid div { flex: 1; text-align: center; padding: 10px; font-size: 20px; font-weight: bold; border-right: 1px solid #333; }

    /* 버튼 행: 무조건 가로 정렬 & 틈새 0 */
    .btn-container { display: flex; width: 100%; gap: 0px; margin-bottom: 2px; }
    .btn-container > button { 
        flex: 1; height: 45px; border-radius: 0; border: 0.5px solid #444; 
        background: #f0f0f0; font-weight: bold; font-size: 13px; cursor: pointer;
    }

    /* 차트 영역 */
    .chart-board {
        background: white; border: 1px solid #333; height: calc(100vh - 180px);
        padding: 5px; display: flex; gap: 5px; overflow-x: auto; margin-top: 5px;
    }
    .chart-col { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [HTML 구조 시작] ---
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# 1. 정보창
st.markdown(f"""
    <div class="info-grid">
        <div style="border-right:1px solid #333;">1,000</div>
        <div style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# 2. 첫째 줄 (플, 뱅, 뒤로, 초기) - columns를 쓰되 gap을 0으로 강제
c1, c2, c3, c4 = st.columns(4, gap="small")
with c1: 
    if st.button("플", key="p_btn", use_container_width=True): st.session_state.history.append("P")
with c2: 
    if st.button("뱅", key="b_btn", use_container_width=True): st.session_state.history.append("B")
with c3: 
    if st.button("뒤로", key="undo_btn", use_container_width=True): 
        if st.session_state.history: st.session_state.history.pop()
with c4: 
    if st.button("초기", key="reset_btn", use_container_width=True): st.session_state.history = []

# 3. 둘째 줄 (1~8번) - columns 8개 강제 밀착
s_cols = st.columns(8, gap="small")
for i in range(1, 9):
    with s_cols[i-1]:
        st.button(str(i), key=f"s_{i}", use_container_width=True)

# 4. 바카라 차트
def get_chart_html(history):
    if not history: return "<div class='chart-board'></div>"
    cols, curr = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: curr.append(history[i])
        else: cols.append(curr); curr = [history[i]]
    cols.append(curr)
    html = "<div class='chart-board'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(get_chart_html(st.session_state.history), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
