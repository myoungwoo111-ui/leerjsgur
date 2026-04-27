import streamlit as st

# 1. 페이지 설정 (앱처럼 보이게)
st.set_page_config(page_title="Baccarat Macro", layout="wide", initial_sidebar_state="collapsed")

# 2. 사진 속 엑셀 폼과 똑같은 레이아웃 구현 (CSS)
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .block-container { padding: 0px !important; margin: 0px !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        overflow: hidden !important; background-color: #f0f0f2; 
    }
    .main-box { max-width: 380px; margin: 0 auto; padding: 10px; }

    /* 버튼 가로 정렬 강제 고정 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 2px !important;
    }
    div[data-testid="column"] { flex: 1 !important; min-width: 0 !important; }

    /* 엑셀 스타일 버튼 */
    .stButton > button {
        width: 100% !important; height: 45px !important; border-radius: 0px !important;
        border: 1px solid #333 !important; background-color: #e1e1e1 !important;
        font-weight: bold !important; font-size: 14px !important; color: black !important;
    }
    
    /* 상단 정보창 */
    .info-bar { display: flex; border: 2px solid #333; background: white; margin-bottom: 5px; }
    .info-item { flex: 1; text-align: center; padding: 12px; font-size: 18px; font-weight: bold; border-right: 2px solid #333; }

    /* 바카라 정석 차트 영역 */
    .chart-area {
        background: white; border: 2px solid #333; height: 350px; margin-top: 8px;
        padding: 10px; display: flex; gap: 4px; overflow-x: auto;
    }
    .chart-col { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 매크로 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 1

# 결과 입력 함수 (사진 분석 로직 반영)
def record(res):
    st.session_state.history.append(res)
    # 여기에 승/패에 따른 단계 자동 조절 매크로 로직을 추가할 수 있습니다.
    # 현재는 기록 기능 위주로 구성되었습니다.

# --- 화면 렌더링 ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

# [상단] 현재 단계 및 정보
st.markdown(f"""
    <div class="info-bar">
        <div class="info-item">{st.session_state.step}단계</div>
        <div class="info-item" style="border-right:0;">플레이어</div>
    </div>
""", unsafe_allow_html=True)

# [중단] 조작 버튼 (4열)
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("플"): record("P")
with c2: 
    if st.button("뱅"): record("B")
with c3: 
    if st.button("뒤로"): 
        if st.session_state.history: st.session_state.history.pop()
with c4: 
    if st.button("초기"): 
        st.session_state.history = []; st.session_state.step = 1

# [중단] 단계 버튼 (8열)
s_cols = st.columns(8)
for i in range(1, 9):
    with s_cols[i-1]:
        if st.button(str(i)): st.session_state.step = i

# [하단] 바카라 정석 출목표 로직
def draw_chart(history):
    if not history: return "<div class='chart-area'></div>"
    cols, tmp = [], [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]: tmp.append(history[i])
        else: cols.append(tmp); tmp = [history[i]]
    cols.append(tmp)
    
    html = "<div class='chart-area'>"
    for col in cols:
        html += "<div class='chart-col'>"
        for item in col:
            tag = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{tag}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(draw_chart(st.session_state.history), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
