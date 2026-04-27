import streamlit as st

# 1. 페이지 설정 및 제목 숨기기
st.set_page_config(layout="wide")

# 2. 버튼 가로 배치를 위한 CSS (간격 최소화)
st.markdown("""
    <style>
    /* 버튼 높이와 폰트 조절 */
    .stButton>button { 
        width: 100%; 
        height: 42px; 
        padding: 0px; 
        font-size: 14px !important; 
        font-weight: bold;
    }
    /* 컬럼 사이 간격 줄이기 */
    div[data-testid="stHorizontalBlock"] { 
        gap: 5px !important; 
    }
    /* 상단 박스 스타일 */
    .main-box { 
        background-color: white; 
        border: 1px solid #777; 
        text-align: center; 
        font-size: 22px; 
        font-weight: bold; 
        padding: 10px; 
    }
    /* 차트 기록판 스타일 */
    .record-board { 
        background-color: white; 
        border: 1px solid #777; 
        min-height: 300px; 
        padding: 15px; 
        overflow-x: auto; 
    }
    .col-container { display: flex; align-items: flex-start; gap: 12px; }
    .record-column { display: flex; flex-direction: column; min-width: 25px; text-align: center; font-family: monospace; font-size: 18px; }
    .p-text { color: blue; font-weight: bold; }
    .b-text { color: red; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기 세팅
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 1

# --- [상단] 엑셀 정보창 ---
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("<div class='main-box'>1,000</div>", unsafe_allow_html=True)
with col_info2:
    recom = "플레이어" if len(st.session_state.history) % 2 == 0 else "뱅커"
    st.markdown(f"<div class='main-box'>{recom}</div>", unsafe_allow_html=True)

st.write("") # 한 줄 띄움

# --- [중단] 메인 버튼 4개 (가로 한 줄 배치) ---
# 왼쪽 이미지처럼 가로로 나열
c1, c2, c3, c4 = st.columns(4)
if c1.button("플레이어"): st.session_state.history.append("P")
if c2.button("뱅커"): st.session_state.history.append("B")
if c3.button("뒤로가기"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기화"): st.session_state.history = []

st.write("") # 한 줄 띄움

# --- [중단] 단계 버튼 8개 (가로 한 줄 배치) ---
# 한 줄에 8개가 모두 들어가도록 컬럼 생성
step_cols = st.columns(8)
for i in range(1, 9):
    if step_cols[i-1].button(f"{i}번"):
        st.session_state.step = i

# --- [하단] 기록 차트 (같은 글자 아래로, 틀리면 옆으로) ---
st.write("---")
st.caption("📋 실시간 기록 현황")

def render_baccarat_chart(history):
    if not history: return "<div class='record-board'>기록 없음</div>"
    
    # 같은 글자 아래로, 틀리면 옆으로 이동하는 로직
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
    
    html = "<div class='record-board'><div class='col-container'>"
    for col in columns:
        html += "<div class='record-column'>"
        for item in col:
            color_class = "p-text" if item == "P" else "b-text"
            html += f"<span class='{color_class}'>{item}</span>"
        html += "</div>"
    html += "</div></div>"
    return html

st.markdown(render_baccarat_chart(st.session_state.history), unsafe_allow_html=True)
