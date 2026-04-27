import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 스크롤 방지 및 화면 압축 CSS
st.markdown("""
    <style>
    /* 화면 전체 스크롤 차단 및 여백 최소화 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }
    .block-container { 
        padding: 5px !important; 
        max-width: 450px !important; 
        margin: auto !important; 
    }
    
    /* 버튼 행 간격 제거 */
    [data-testid="stHorizontalBlock"] { 
        display: flex !important; 
        gap: 1px !important; 
        margin-bottom: 2px !important;
    }
    
    /* 버튼 스타일: 높이를 더 줄여서 한 화면에 밀어넣음 */
    .stButton>button {
        width: 100% !important; 
        height: 38px !important; 
        border-radius: 0px !important;
        border: 0.5px solid #444 !important; 
        font-size: 12px !important; 
        font-weight: bold !important;
        padding: 0px !important;
    }

    /* 정보 표시창 크기 축소 */
    .info-box { 
        border: 1px solid #444; 
        text-align: center; 
        padding: 5px; 
        font-size: 18px; 
        font-weight: bold; 
        background: white; 
    }

    /* 차트 영역: 남은 화면 높이에 맞춤 */
    .chart-area { 
        background: white; 
        border: 1px solid #444; 
        height: calc(100vh - 220px); /* 버튼 제외 남은 공간 모두 활용 */
        padding: 5px; 
        display: flex; 
        gap: 3px; 
        overflow-x: auto; 
    }
    .chart-column { display: flex; flex-direction: column; width: 18px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 16px; }
    .b-mark { color: red; font-weight: bold; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보창 (압축형) ---
t_col1, t_col2 = st.columns(2)
t_col1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t_col2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- [중단] 가로 1번줄 (플, 뱅, 뒤로, 초기) ---
m_col = st.columns(4)
if m_col[0].button("플"): st.session_state.history.append("P")
if m_col[1].button("뱅"): st.session_state.history.append("B")
if m_col[2].button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if m_col[3].button("초기"): st.session_state.history = []

# --- [중단] 가로 2번줄 (1~8번) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(str(i))

# --- [하단] 바카라 차트 (스크롤 없이 고정) ---
def render_chart(history):
    if not history: return "<div class='chart-area'></div>"
    columns = []
    current_col = [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            columns.append(current_col)
            current_col = [history[i]]
    columns.append(current_col)
    
    html = "<div class='chart-area'>"
    for col in columns:
        html += "<div class='chart-column'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class='{cls}'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
