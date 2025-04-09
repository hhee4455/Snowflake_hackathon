import streamlit as st
import pandas as pd
from utils.snowflake import get_connection

st.header("📊 서울시 젠트리피케이션 리스크 대시보드")
st.caption("서울 3개 자치구(서초구, 영등포구, 중구)의 유동, 소비, 시세 데이터를 기반으로 상권 리스크를 분석합니다.")

# 연결
try:
    conn = get_connection()
except Exception as e:
    st.error(f"Snowflake 연결 오류: {e}")
    st.stop()

