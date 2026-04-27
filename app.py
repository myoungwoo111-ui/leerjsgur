import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 모바일에서 컬럼이 세로로 쌓이는 것을 방지하는 핵심 CSS
st.markdown("""
    <style>
    /* 모든 가로 블록(st.columns)이 모바일에서도 가로로 유지되게 함 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 4px !important; /* 버튼 사이 간격 최소화 */
    }
    
    /* 각 버튼의 너비를 균등하게 조절 */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 버튼 텍스트 크기 및 높이 최적화 */
    .stButton>button {
        width: 100%;
        padding: 0px;
        height: 40px;
        font-size: 13px !important;
        font-weight: bold;
    }

    /* 상단 정보 박스 스타일 */
    .info-box {
        background-color: #f0f2f6;
        border: 1px solid #777;
        text-align: center;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
    }
    
    /* 차트 영역 스타일 */
    .chart-container {
        background-color: white;
        border: 2px solid #444;
        min-height: 250px;
        padding: 10px;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보 표시창 (가로 2열) ---
col_top1, col_top2 = st.columns(2)
col_top1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
col_top2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

st.write("")

# --- [중단] 메인 액션 버튼 (가로 4열 강제 유지) ---
# 엑셀의 플레이어, 뱅커, 뒤로가기, 초기화 버튼 배치
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("🔙"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("🔄"): st.session_state.history = []

# --- [중단] 단계 버튼 (가로 8열 강제 유지) ---
# 모바일에서 8개가 한 줄에 나오도록 설정
step_cols = st.columns(8)
for i in range(1, 9):
    step_cols[i-1].button(f"{i}번")

st.write("")

# --- [하단] 기록 차트 현황 ---
st.caption("📊 실시간 기록 현황")
def get_chart_html(history):
    if not history: return "<div class='chart-container'>기록 대기 중...</div>"
    
    columns = []
    if history:
        current_col = [history[0]]
        for i in range(1, len(history)):
            if history[i] == history[i-1]:
                current_col.append(history[i])
            else:
                columns.append(current_col)
                current_col = [history[i]]
        columns.append(current_col)
    
    html = "<div class='chart-container' style='display: flex; gap: 10px;'>"
    for col in columns:
        html += "<div style='display: flex; flex-direction: column; align-items: center;'>"
        for item in col:
            color = "blue" if item == "P" else "red"
            html += f"<span style='color: {color}; font-weight: bold; font-size: 18px;'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(get_chart_html(st.session_state.history), unsafe_allow_html=True)
