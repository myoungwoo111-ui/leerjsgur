import streamlit as st

# 1. 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 2. 버튼 가로 꽉 참 & 모바일 고정 CSS
st.markdown("""
    <style>
    /* 상단 메뉴 등 불필요한 여백 제거 */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    /* 가로 블록 강제 고정 및 꽉 채우기 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 2px !important; /* 버튼 사이 아주 미세한 간격 */
    }
    
    /* 각 컬럼이 정확히 N등분 되도록 설정 */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 버튼 스타일: 테두리 강조 및 꽉 채우기 */
    .stButton>button {
        width: 100% !important;
        height: 45px !important;
        padding: 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        border: 1px solid #777 !important;
        border-radius: 0px !important; /* 엑셀 느낌을 위해 각지게 */
    }

    /* 상단 정보 박스 꽉 채우기 */
    .info-box {
        background-color: white;
        border: 1px solid #777;
        text-align: center;
        padding: 10px 0;
        font-size: 22px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 데이터 관리
if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 정보창 (2등분 꽉 참) ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

st.write("")

# --- [중단] 메인 액션 버튼 (4등분 꽉 참) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("🔙"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("🔄"): st.session_state.history = []

st.write("")

# --- [중단] 단계 버튼 (8등분 꽉 참) ---
step_cols = st.columns(8)
for i in range(1, 9):
    step_cols[i-1].button(f"{i}")

st.write("")

# --- [하단] 기록 차트 ---
def get_chart_html(history):
    if not history: return "<div style='border:1px solid #ccc; height:200px; padding:10px;'>기록 대기 중...</div>"
    
    columns = []
    current_col = [history[0]]
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            columns.append(current_col)
            current_col = [history[i]]
    columns.append(current_col)
    
    html = "<div style='display: flex; gap: 8px; border:1px solid #777; padding:10px; background:white; overflow-x:auto;'>"
    for col in columns:
        html += "<div style='display: flex; flex-direction: column;'>"
        for item in col:
            color = "blue" if item == "P" else "red"
            html += f"<span style='color: {color}; font-weight: bold; font-size: 18px;'>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(get_chart_html(st.session_state.history), unsafe_allow_html=True)
