import pandas as pd
import streamlit as st
from utils.snowflake import get_snowflake_connection

@st.cache_data(show_spinner="데이터를 불러오는 중입니다...")
def load_score_data(strict: bool = True):
    conn = get_snowflake_connection()
    table_name = "GENTRIFICATION_STRICT" if strict else "GENTRIFICATION_SCORE"
    
    query = f"SELECT * FROM {table_name}"
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()

    cur.close()
    conn.close()

    # MONTH 처리
    if "MONTH" in df.columns:
        df["MONTH"] = pd.to_datetime(df["MONTH"], errors="coerce")
        df["MONTH"] = df["MONTH"].dt.strftime("%Y-%m-%d")  # Arrow-safe
        df["연도"] = pd.to_datetime(df["MONTH"], errors="coerce").dt.year

    return df