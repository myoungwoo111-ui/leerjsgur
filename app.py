import streamlit as st

# 1. 페이지 설정 (최대한 앱처럼 보이게 설정)
st.set_page_config(
    page_title="Baccarat Manager",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. EXE 프로그램 수준의 강력한 레이아웃 고정 CSS
st.markdown("""
    <style>
    /* 메뉴 및 여백 완전 제거 */
    header, footer, #MainMenu {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    
    /* 전체 화면 고정 (스크롤 금지) */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
        background-color: #f0f0f0;
    }

    /* 전체 폭을 모바일 최적 폭(360px~390px)으로 중앙 고정 */
    .app-wrapper {
        max-width: 400px;
        margin: 0 auto;
        padding: 5px;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* 버튼 행: 무조건 가로 정렬 고정 (CSS Grid 사용) */
    .btn-row-4 {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 1px !important;
        margin-bottom: 2px !important;
    }
    .btn-row-8 {
        display: grid !important;
        grid-template-columns: repeat(8, 1fr) !important;
        gap: 1px !important;
    }

    /* 버튼 스타일 (각진 엑셀 폼 디자인) */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 0px !important;
        border: 1px solid #444 !important;
        background-color: #e1e1e1 !important;
        color: #000 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        padding: 0 !important;
    }
    .stButton > button:active { background-color: #bbb !important; }

    /* 상단 정보창 */
    .status-bar {
        display: flex;
        border: 1.5px solid #333;
        background: #fff;
        margin-bottom: 5px;
    }
    .status-item {
        flex: 1;
        text-align: center;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        border-right: 1.5px solid #333;
    }

    /* 하단 차트 영역 (정석 로직 적용) */
    .chart-box {
        flex-grow: 1;
        background: white;
        border: 1.5px solid #333;
        margin-top: 5px;
        padding: 8px;
        display: flex;
        gap: 3px;
        overflow-x: auto;
        align-content: flex-start;
    }
    .chart-col { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 16px; line-height: 1.3; }
    .b-mark { color: red; font-weight: bold; font-size: 16px; line-height: 1.3; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- 메인 레이아웃 ---
st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

# 1. 정보 박스
st.markdown(f"""
    <div class="status-bar">
        <div class="status-item">1,000</div>
        <div class="status-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# 2. 첫째 줄 버튼 (플, 뱅, 뒤로, 초기)
# st.columns의 gap을 0으로 만들어 찢어짐 방지
c1, c2, c3, c4 = st.columns(4, gap="small")
with c1: 
    if st.button("플"): st.session_state.history.append("P")
with c2: 
    if st.button("뱅"): st.session_state.history.append("B")
with c3: 
    if st.button("뒤로"): 
        if st.session_state.history: st.session_state.history.pop()
with c4: 
    if st.button("초기"): st.session_state.history = []

# 3. 둘째 줄 단계 버튼 (1~8)
s_cols = st.columns(8, gap="small")
for i in range(1, 9):
    with s_cols[i-1]:
        st.button(str(i))

# 4. 차트 로직 (P-P 아래로, P-B 옆열로)
def get_chart_html(history):
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

st.markdown(get_chart_html(st.session_state.history), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
