import streamlit as st

# 1. 페이지 설정 (최대한 넓게)
st.set_page_config(layout="wide")

# 2. 엑셀 유저폼 스타일 재현 (CSS)
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 40px; padding: 0px; font-size: 13px !important; margin-bottom: -10px; }
    .main-box { background-color: white; border: 1px solid #777; padding: 5px; text-align: center; 
                font-size: 22px; font-weight: bold; color: black; min-height: 50px; display: flex; align-items: center; justify-content: center; }
    /* 기록창 스타일 */
    .record-board { background-color: white; border: 1px solid #777; min-height: 250px; padding: 10px; font-family: monospace; overflow-x: auto; }
    .col-container { display: flex; align-items: flex-start; gap: 10px; }
    .record-column { display: flex; flex-direction: column; min-width: 20px; text-align: center; }
    .p-text { color: blue; font-weight: bold; }
    .b-text { color: red; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 데이터 초기화
if 'history' not in st.session_state: st.session_state.history = []
if 'step' not in st.session_state: st.session_state.step = 1

# --- [상단] 엑셀 정보창 (금액 / 추천) ---
st.write("")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("<div class='main-box'>1,000</div>", unsafe_allow_html=True)
with col_info2:
    recom = "플레이어" if len(st.session_state.history) % 2 == 0 else "뱅커"
    st.markdown(f"<div class='main-box'>{recom}</div>", unsafe_allow_html=True)

# --- [중단] 메인 버튼 (가로 4열) ---
st.write("")
c1, c2, c3, c4 = st.columns(4)
if c1.button("플레이어"): st.session_state.history.append("P")
if c2.button("뱅커"): st.session_state.history.append("B")
if c3.button("뒤로가기"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("초기화"): st.session_state.history = []

# --- [중단] 단계 버튼 (가로 8열) ---
st.write("")
step_cols = st.columns(8)
for i in range(1, 9):
    if step_cols[i-1].button(f"{i}번"):
        st.session_state.step = i

# --- [하단] 기록 차트 (같은 글자 아래로, 틀리면 옆으로) ---
st.write("---")
st.write("📋 **실시간 기록 차트**")

def render_chart(history):
    if not history: return ""
    
    columns = []
    current_col = [history[0]]
    
    for i in range(1, len(history)):
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            columns.append(current_col)
            current_col = [history[i]]
    columns.append(current_col)
    
    # HTML로 차트 그리기
    html = "<div class='record-board'><div class='col-container'>"
    for col in columns:
        html += "<div class='record-column'>"
        for item in col:
            color_class = "p-text" if item == "P" else "b-text"
            html += f"<span class='{color_class}'>{item}</span>"
        html += "</div>"
    html += "</div></div>"
    return html

st.markdown(render_chart(st.session_state.history), unsafe_allow_html=True)
