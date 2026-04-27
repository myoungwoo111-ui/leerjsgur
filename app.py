import streamlit as st

# 1. 페이지 레이아웃 및 브라우저 기본 스타일 초기화
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* 1. 기본 여백 및 스크롤 완전 차단 */
    header, footer {visibility: hidden;}
    [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        background-color: #f5f5f5;
    }
    .block-container {
        padding: 5px !important;
        max-width: 380px !important; /* 화면을 더 좁게 잡아 버튼을 중앙으로 강제 밀착 */
        margin: auto !important;
    }

    /* 2. 가로 배치(st.columns) 내부의 여백을 0으로 박살 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important; /* 버튼 사이 틈새 제거 */
        justify-content: center !important;
    }
    
    /* 3. 각 컬럼 칸의 너비와 여백 강제 조정 */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        min-width: 0px !important;
        flex: 1 !important;
    }

    /* 4. 버튼 디자인: 엑셀 유저폼과 동일하게 각진 디자인 */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 0px !important;
        border: 1px solid #666 !important;
        background-color: #e1e1e1 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: #000 !important;
        padding: 0px !important;
    }
    .stButton > button:active {
        background-color: #bbb !important;
    }

    /* 5. 상단 정보창 (중앙 밀착) */
    .info-container {
        display: flex;
        border: 1.5px solid #444;
        background: white;
        margin-bottom: 4px;
        width: 100%;
    }
    .info-item {
        flex: 1;
        text-align: center;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
        border-right: 1.5px solid #444;
    }

    /* 6. 바카라 차트 영역: 정석 로직 고정 */
    .baccarat-chart {
        background: white;
        border: 1.5px solid #444;
        height: calc(100vh - 190px);
        margin-top: 5px;
        padding: 5px;
        display: flex;
        gap: 2px;
        overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-txt { color: #0000ff; font-weight: bold; font-size: 18px; line-height: 1.2; }
    .b-txt { color: #ff0000; font-weight: bold; font-size: 18px; line-height: 1.2; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 상태 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- 레이아웃 시작 ---

# 1. 정보 박스
st.markdown(f"""
    <div class="info-container">
        <div class="info-item">1,000</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# 2. 첫 번째 줄: 메인 버튼 (4개 강제 밀착)
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

# 3. 두 번째 줄: 단계 버튼 (8개 강제 밀착)
row2 = st.columns(8)
for i in range(1, 9):
    with row2[i-1]:
        st.button(str(i))

# 4. 바카라 정석 차트 로직 (같으면 아래, 틀리면 옆)
def get_baccarat_html(history):
    if not history: return "<div class='baccarat-chart'></div>"
    
    cols = []
    temp = [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            temp.append(history[i])
        else:
            cols.append(temp)
            temp = [history[i]]
    cols.append(temp)
    
    html = "<div class='baccarat-chart'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "p-txt" if item == "P" else "b-txt"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(get_baccarat_html(st.session_state.history), unsafe_allow_html=True)
