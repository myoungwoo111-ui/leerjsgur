import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 버튼 밀착 및 차트 전용 CSS
st.markdown("""
    <style>
    /* 여백 완전히 제거 및 모바일 폭 고정 */
    .block-container { padding: 10px 5px !important; max-width: 450px !important; margin: auto !important; }
    
    /* 가로 버튼 강제 밀착 - 절대 줄바꿈 안되게 설정 */
    [data-testid="stHorizontalBlock"] { 
        display: flex !important; 
        flex-direction: row !important; 
        flex-wrap: nowrap !important; 
        gap: 1px !important; 
        margin-bottom: 5px !important;
    }
    
    /* 각 컬럼 너비를 동일하게 배분 */
    [data-testid="column"] { 
        flex: 1 !important; 
        min-width: 0px !important; 
        padding: 0px !important; 
    }

    /* 버튼 스타일 (엑셀 유저폼 스타일) */
    .stButton>button {
        width: 100% !important; 
        height: 45px !important; 
        border-radius: 0px !important;
        border: 0.5px solid #444 !important; 
        font-size: 13px !important; 
        font-weight: bold !important;
        background-color: #f0f0f0 !important;
        padding: 0px !important;
    }

    /* 정보 표시창 */
    .info-box { border: 1px solid #444; text-align: center; padding: 10px; font-size: 20px; font-weight: bold; background: white; margin-bottom: 10px; }

    /* 차트판 스타일 (바카라 로직 전용) */
    .chart-area { background: white; border: 1px solid #444; min-height: 250px; padding: 10px; display: flex; gap: 5px; overflow-x: auto; }
    .chart-column { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 1

# --- [상단] 정보창 ---
t_col1, t_col2 = st.columns(2)
t_col1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t_col2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- [중단 첫째줄] 메인 버튼 4개 (플, 뱅, 뒤로, 초기화) ---
# 무조건 한 줄에 가로로 배치됩니다.
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
if m_col1.button("플"): st.session_state.history.append("P")
if m_col2.button("뱅"): st.session_state.history.append("B")
if m_col3.button("뒤로"): 
    if st.session_state.history: st.session_state.history.pop()
if m_col4.button("초기"): st.session_state.history = []

# --- [중단 둘째줄] 단계 버튼 8개 (1번 ~ 8번) ---
# 무조건 한 줄에 가로로 배치됩니다.
s_cols = st.columns(8)
for i in range(1, 9):
    if s_cols[i-1].button(str(i)):
        st.session_state.step = i

st.write("")

# --- [하단] 차트 로직 (같으면 아래, 틀리면 옆) ---
def render_baccarat_chart(history):
    if not history: return "<div class='chart-area'>기록 없음</div>"
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

st.markdown(render_baccarat_chart(st.session_state.history), unsafe_allow_html=True)
