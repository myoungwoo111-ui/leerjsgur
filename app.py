import streamlit as st

# 1. 페이지 설정 및 브라우저 기본 여백 완전 제거
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    /* 상단 메뉴 및 불필요한 공간 삭제 */
    header, footer {visibility: hidden;}
    [data-testid="stAppViewContainer"] {
        overflow: hidden !important; /* 스크롤 절대 방지 */
        height: 100vh;
        background-color: #f0f0f0;
    }
    .block-container {
        padding: 5px !important;
        max-width: 100vw !important; /* 핸드폰 화면 폭에 100% 맞춤 */
        margin: 0 !important;
    }

    /* 버튼 행: 무조건 가로로 꽉 채우기 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 줄바꿈 차단 */
        gap: 1px !important;
        width: 100% !important;
    }
    
    /* 컬럼 간격 및 여백 제로 */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        min-width: 0px !important;
        flex: 1 !important;
    }

    /* 버튼 디자인: 엑셀 유저폼 스타일 */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 0px !important;
        border: 1px solid #333 !important;
        background-color: #e1e1e1 !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* 상단 정보창 */
    .info-container {
        display: flex;
        border: 1px solid #333;
        background: white;
        margin-bottom: 3px;
    }
    .info-item {
        flex: 1;
        text-align: center;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        border-right: 1px solid #333;
    }

    /* 바카라 차트 영역: 정석 로직 고정 */
    .chart-box {
        background: white;
        border: 1.5px solid #333;
        height: calc(100vh - 190px); /* 버튼 높이 제외한 나머지 꽉 채움 */
        padding: 5px;
        display: flex;
        gap: 3px;
        overflow-x: auto;
    }
    .c-col { display: flex; flex-direction: column; width: 20px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 16px; }
    .b-mark { color: red; font-weight: bold; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 레이아웃 구현 ---

# 1. 정보창
st.markdown(f"""
    <div class="info-container">
        <div class="info-item">1,000</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# 2. 첫째 줄: 메인 버튼 4개 (플, 뱅, 뒤로, 초기)
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

# 3. 둘째 줄: 단계 버튼 8개 (1~8)
row2 = st.columns(8)
for i in range(1, 9):
    with row2[i-1]:
        st.button(str(i))

# 4. 바카라 로직 차트
def get_chart(history):
    if not history: return "<div class='chart-box'></div>"
    cols, temp = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            temp.append(history[i])
        else:
            cols.append(temp)
            temp = [history[i]]
    cols.append(temp)
    
    html = "<div class='chart-box'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(get_chart(st.session_state.history), unsafe_allow_html=True)
