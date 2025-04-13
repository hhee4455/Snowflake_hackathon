import pandas as pd
import streamlit as st

@st.cache_data
def load_coordinates(csv_path="data/seoul_region_coordinates.csv"):
    """행정동 지역명 기반 위도/경도 매핑 테이블 불러오기"""
    return pd.read_csv(csv_path)  # REGION_NAME, LAT, LON 포함되어 있어야 함

def add_lat_lon(df, coord_df):
    """REGION_NAME 기준으로 좌표 병합"""
    merged = df.merge(coord_df, on="REGION_NAME", how="left")
    missing = merged["LAT"].isnull().sum()
    if missing > 0:
        st.warning(f"⚠️ 좌표가 누락된 지역이 {missing}개 있습니다. 지도에서 표시되지 않을 수 있습니다.")
    return merged
