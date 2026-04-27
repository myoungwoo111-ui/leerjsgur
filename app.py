import streamlit as st

# 1. 페이지 전체를 가장 넓게 설정
st.set_page_config(layout="wide")

# 2. 모든 여백을 죽이고 버튼을 강제로 밀착시키는 강력한 CSS
st.markdown("""
    <style>
    /* 1. 기본 컨테이너 여백 제거 (좌우 꽉 차게) */
    .block-container { 
        padding-top: 5px !important; 
        padding-bottom: 0px !important; 
        padding-left: 5px !important; 
        padding-right: 5px !important; 
    }
    
    /* 2. 가로 배치(st.columns) 시 발생하는 모든 여백과 줄바꿈 차단 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 0px !important; /* 버튼 사이 간격 0 */
    }
    
    /* 3. 각 컬럼 칸 사이의 여백 제거 */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* 4. 버튼 스타일: 엑셀처럼 각지고 테두리 있게, 여백 없이 꽉 참 */
    .stButton>button {
        width: 100% !important;
        height: 50px !important;
        margin: 0px !important;
        padding: 0px !important;
        border-radius: 0px !important; /* 각지게 */
        border: 0.5px solid #444 !important; /* 얇은 테두리 */
        font-weight: bold !important;
        background-color: #f0f0f0;
    }
    
    /* 상단 텍스트 박스 밀착 */
    .info-box {
        border: 1px solid #444;
        text-align: center;
        padding: 10px 0;
        font-size: 20px;
        font-weight: bold;
        background: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [상단] 정보창 (2열 밀착) ---
t1, t2 = st.columns(2)
t1.markdown("<div class='info-box'>1,000</div>", unsafe_allow_html=True)
t2.markdown("<div class='info-box'>플레이어</div>", unsafe_allow_html=True)

# --- [중단] 메인 버튼 (4열 밀착) ---
c1, c2, c3, c4 = st.columns(4)
c1.button("플")
c2.button("뱅")
c3.button("뒤로")
c4.button("초기")

# --- [중단] 단계 버튼 (8열 밀착) ---
s_cols = st.columns(8)
for i in range(1, 9):
    s_cols[i-1].button(f"{i}")

# --- [하단] 기록 현황판 (테두리 꽉 차게) ---
st.markdown("""
    <div style='border: 1px solid #444; height: 300px; padding: 5px; background: white;'>
        <p style='color:blue; font-weight:bold; margin:0;'>P</p>
        <p style='color:red; font-weight:bold; margin:0;'>B</p>
    </div>
    """, unsafe_allow_html=True)
