import pandas as pd
import streamlit as st
from utils.snowflake import get_snowflake_connection

@st.cache_data(show_spinner="데이터를 불러오는 중입니다...")
def load_score_data(strict: bool = True):
    conn = get_snowflake_connection()
    table_name = "GENTRIFICATION_STRICT" if strict else "GENTRIFICATION_SCORE"
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df
