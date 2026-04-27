import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

# 2. 버튼 밀착 및 차트 전용 CSS
st.markdown("""
    <style>
    /* 여백 완전히 제거 */
    .block-container { padding: 5px !important; max-width: 450px !important; margin: auto !important; }
    
    /* 버튼 가로로 다닥다닥 붙이기 */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; gap: 1px !important; }
    [data-testid="column"] { flex: 1 !important; min-width: 0px !important; padding: 0px !important; }

    /* 버튼 스타일 (엑셀 유저폼 스타일) */
    .stButton>button {
        width: 100% !important; height: 45px !important; border-radius: 0px !important;
        border: 1px solid #444 !important; font-size: 14px !important; font-weight: bold !important;
    }

    /* 정보 표시창 */
    .info-box { border: 1px solid #444; text-align: center; padding: 10px; font-size: 20px; font-weight: bold; background: white; margin-bottom: 5px; }

    /* 차트판 스타일 */
    .chart-area { background: white; border: 1px solid #444; min-height: 250px; padding: 10px; display: flex; gap: 5px; overflow-x: auto; }
    .chart-column { display: flex; flex-direction: column; width: 22px; text-align: center; }
    .p-mark { color: blue; font-weight: bold; font-size: 18px; }
    .b-mark { color: red; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'history' not in st.session_state: st.session_state.history = []

# --- [상단] 금액/추천창 ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- [중단] 메인 버튼 (4개 밀착) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("플"): st.session_state.history.append("P")
if c2.button("뱅"): st.session_state.history.append("B")
if c3.button("🔙"): 
    if st.session_state.history: st.session_state.history.pop()
if c4.button("🔄"): st.session_state.history = []

# --- [중단] 단계 버튼 (8개 밀착) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(f"{i}")

st.write("")

# --- [하단] 바카라 차트 로직 (같으면 아래, 틀리면 옆) ---
st.caption("📋 실시간 기록 차트")

def render_baccarat_logic(history):
    if not history: return "<div class='chart-area'>기록 없음</div>"
    
    columns = []
    current_col = [history[0]]
    
    for i in range(1, len(history)):
        # 앞의 글자와 같으면 같은 컬럼(아래로), 틀리면 새로운 컬럼(옆으로)
        if history[i] == history[i-1]:
            current_col.append(history[i])
        else:
            columns.append(current_col)
            current_col = [history[i]]
    columns.append(current_col)
    
    # HTML 생성
    html = "<div class='chart-area'>"
    for col in columns:
        html += "<div class='chart-column'>"
        for item in col:
            cls = "p-mark" if item == "P" else "b-mark"
            html += f"<span class={cls}>{item}</span>"
        html += "</div>"
    html += "</div>"
    return html

st.markdown(render_baccarat_logic(st.session_state.history), unsafe_allow_html=True)
