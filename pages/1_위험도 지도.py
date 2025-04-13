import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.data_loader import load_score_data

# ---------------------- 설정 ----------------------
st.set_page_config(page_title="젠트리피케이션 지도", layout="wide")

@st.cache_data(show_spinner="데이터 로딩 중...")
def get_data():
    return load_score_data(strict=True)

@st.cache_data
def load_coordinates(csv_path="data/seoul_gu_coordinates.csv"):
    return pd.read_csv(csv_path)

def add_lat_lon(df, coord_df):
    merged = df.merge(coord_df, on="REGION_NAME", how="left")
    if merged["LAT"].isnull().sum() > 0:
        st.warning("⚠️ 좌표 누락 지역이 존재합니다.")
    return merged

def preprocess(df):
    df["MONTH"] = pd.to_datetime(df["MONTH"], errors="coerce")
    df["월"] = df["MONTH"].dt.to_period("M").dt.to_timestamp()
    return df

# ---------------------- 헤더 ----------------------
st.markdown("""
    <div style='padding: 2rem; background: linear-gradient(90deg, #10B981, #4F46E5); border-radius: 1rem; color: white; text-align: center;'>
        <h1 style='margin-bottom: 0.5rem;'>서울시 젠트리피케이션 위험도 지도</h1>
        <p style='font-size: 1.1rem;'>지역별 위험도를 색상 및 크기로 시각화하여, 흐름과 패턴을 직관적으로 파악할 수 있습니다.</p>
    </div>
""", unsafe_allow_html=True)
st.divider()

# ---------------------- 본문 ----------------------
try:
    df = preprocess(get_data())
    coord_df = load_coordinates()
    df = add_lat_lon(df, coord_df)
except Exception as e:
    st.error(f"❌ 데이터 로딩 실패: {e}")
    st.stop()

months = df["월"].dt.strftime("%Y-%m").unique().tolist()
selected_month = st.selectbox("📅 분석할 월 선택", sorted(months)[::-1])
map_df = df[df["월"].dt.strftime("%Y-%m") == selected_month].copy()

required_cols = {"LAT", "LON", "FINAL_SCORE", "REGION_NAME"}
if not required_cols.issubset(map_df.columns):
    st.error(f"❌ 지도 시각화를 위해 {required_cols} 컬럼이 필요합니다.")
    st.stop()

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position='[LON, LAT]',
    get_radius="500 + 2000 * FINAL_SCORE",
    get_fill_color="""
        [
            255 * FINAL_SCORE,
            255 * (1 - FINAL_SCORE),
            0,
            160
        ]
    """,
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "<b>{REGION_NAME}</b><br/>위험도: {FINAL_SCORE}",
    "style": {"backgroundColor": "black", "color": "white"}
}

view_state = pdk.ViewState(
    latitude=37.5165,
    longitude=126.9780,
    zoom=11,
    pitch=0
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
))

st.divider()
st.markdown("""
    <div style='text-align: center; font-size: 0.9rem; color: gray;'>
        ⓒ 2025 Gentrification Insight. Powered by Streamlit & Snowflake  
        <br>데이터 출처: 서울열린데이터광장, 공공데이터포털, Snowflake Marketplace(SPH, DataKnows, LOPLAT), 국세청, 소상공인시장진흥공단  
        <br>Contact: hhee200456@gmail.com
    </div>
""", unsafe_allow_html=True)
