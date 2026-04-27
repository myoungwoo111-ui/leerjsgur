import streamlit as st

# 1. EXE 프로그램 스타일의 환경 설정
st.set_page_config(
    page_title="Baccarat Macro System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 강력한 모바일 고정 및 EXE 스타일 UI 디자인 (CSS)
st.markdown("""
    <style>
    /* 메뉴 및 헤더 완전 제거 */
    header, footer, #MainMenu {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    
    /* 화면 고정 및 배경색 설정 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
        background-color: #f0f0f2;
    }

    /* 메인 컨테이너: 어떤 폰에서도 중앙 고정 */
    .app-main {
        max-width: 380px;
        margin: 0 auto;
        padding: 8px;
        display: flex;
        flex-direction: column;
    }

    /* 버튼 행: 절대 찢어지지 않게 고정 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; 
        gap: 2px !important;
        margin-bottom: 3px !important;
    }
    
    /* 버튼 내부 스타일: 엑셀 매크로 버튼 느낌 */
    .stButton > button {
        width: 100% !important;
        height: 44px !important;
        border-radius: 2px !important;
        border: 1.5px solid #333 !important;
        background-color: #e8e8e8 !important;
        font-weight: bold !important;
        font-size: 14px !important;
        color: #000 !important;
    }
    .stButton > button:active { background-color: #999 !important; }

    /* 단계 표시 전용 버튼 스타일 (선택된 단계 강조) */
    .step-active > div > button {
        background-color: #ffd700 !important; /* 현재 단계 황금색 강조 */
    }

    /* 상단 상태 바 */
    .status-panel {
        display: flex;
        border: 2px solid #333;
        background: #fff;
        margin-bottom: 6px;
    }
    .status-val {
        flex: 1;
        text-align: center;
        padding: 12px;
        font-size: 20px;
        font-weight: bold;
        border-right: 2px solid #333;
    }

    /* 하단 정석 차트 보드 */
    .baccarat-board {
        flex-grow: 1;
        background: white;
        border: 2px solid #333;
        margin-top: 6px;
        padding: 10px;
        display: flex;
        gap: 4px;
        overflow-x: auto;
    }
    .col-unit { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: #0000ff; font-weight: bold; font-size: 18px; }
    .b-mark { color: #ff0000; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 내부 매크로 로직 (시스템 상태 관리)
if 'history' not in st.session_state: st.session_state.history = []
if 'current_step' not in st.session_state: st.session_state.current_step = 1

def add_record(result):
    st.session_state.history.append(result)
    # 승리 시 1단계 복귀, 패배 시 다음 단계 (사진 속 매크로 로직 반영)
    # 여기서는 예시로 기록만 추가하는 기본 동작 구현
    pass

# --- 화면 구현 ---
st.markdown('<div class="app-main">', unsafe_allow_html=True)

# [상단] 정보 표시
st.markdown(f"""
    <div class="status-panel">
        <div class="status-val">{st.session_state.current_step}단계</div>
        <div class="status-val" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# [중단] 메인 조작 버튼 (4열 고정)
row1 = st.columns(4)
with row1[0]:
    if st.button("플"): add_record("P")
with row1[1]:
    if st.button("뱅"): add_record("B")
with row1[2]:
    if st.button("뒤로"):
        if st.session_state.history: st.session_state.history.pop()
with row1[3]:
    if st.button("초기"):
        st.session_state.history = []
        st.session_state.current_step = 1

# [중단] 단계 선택 버튼 (8열 고정)
row2 = st.columns(8)
for i in range(1, 9):
    with row2[i-1]:
        if st.button(str(i)):
            st.session_state.current_step = i

# [하단] 바카라 정석 차트 (사진 분석 기반 로직)
def render_macro_chart(history):
    if not history: return "<div class='baccarat-board'></div>"
    
    # 같으면 아래로, 틀리면 옆으로 이동하는 2차원 배열 로직
    cols, current_col = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            cols.append(current_col)
            current_col = [history[i]]
    cols.append(current_col)
    
    html = "<div class='baccarat-board'>"
    for col in cols:
        html += "<div class='col-unit'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_macro_chart(st.session_state.history), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
