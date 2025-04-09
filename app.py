import streamlit as st
import pandas as pd
from utils.snowflake import get_connection

# 페이지 기본 설정
st.set_page_config(
    page_title="젠트리피케이션 리스크 예측 시스템",
    layout="wide"
)

st.title("🏙️ 젠트리피케이션 리스크 예측 시스템")

# Snowflake 연결
try:
    conn = get_connection()
    st.success("Snowflake 연결 성공")
except Exception as e:
    st.error(f"Snowflake 연결 실패: {e}")
    st.stop()

# 예시 쿼리 실행
try:
    df = pd.read_sql("SELECT CURRENT_DATE AS today", conn)
    st.write("오늘 날짜 (Snowflake 기준):", df.iloc[0]["TODAY"])
except Exception as e:
    st.error(f"쿼리 실행 중 오류 발생: {e}")
