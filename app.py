import streamlit as st
import pandas as pd
import altair as alt
from utils.data_loader import load_score_data

# ---------------------- 페이지 설정 ----------------------
st.set_page_config(
    page_title="젠트리피케이션 위험도 분석 플랫폼",
    layout="wide"
)

# ---------------------- 데이터 로딩 ----------------------
@st.cache_data(show_spinner="데이터 로딩 중...")
def get_data():
    return load_score_data(strict=True)

def preprocess_month_column(df):
    if not pd.api.types.is_datetime64_any_dtype(df["MONTH"]):
        df["MONTH"] = pd.to_datetime(df["MONTH"], errors="coerce")
    df["월"] = df["MONTH"].dt.to_period("M").dt.to_timestamp()
    return df

# ---------------------- Hero ----------------------
def render_hero():
    st.markdown("""
    <div style='background: linear-gradient(90deg, #4F46E5, #10B981); padding: 3rem 2rem; border-radius: 1.5rem; color: white;'>
        <h1 style='font-size: 2.5rem;'>젠트리피케이션 위험도 분석 플랫폼</h1>
        <p style='font-size: 1.1rem; margin-top: 1rem;'>서울시 데이터를 기반으로 지역별 위험도 지표를 분석하고 시각화하는 Streamlit 기반 대시보드입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

# ---------------------- 데이터 요약 ----------------------
def render_data_overview(df):
    st.subheader("데이터 구성 요약")

    key_columns = {
        "FINAL_SCORE": "최종 점수",
        "NORM_CLOSE": "폐업률 지수",
        "NORM_PRICE": "가격 지수",
        "NORM_MOBILITY": "유동인구 지수",
        "NORM_ASSETS": "자산 지수",
        "NORM_FOOD": "음식 매출 지수",
        "NORM_DOMINANT": "지배 브랜드 비율 지수"
    }

    summary = df[list(key_columns.keys())].agg(["mean", "min", "max"]).T
    summary = summary.rename(index=key_columns).round(3)
    summary.columns = ["평균", "최솟값", "최댓값"]

    st.dataframe(summary, use_container_width=True)

    st.divider()
    st.markdown("#### 결측치 분석")
    null_info = pd.DataFrame({
        "결측치 수": df.isnull().sum(),
        "결측치 비율(%)": (df.isnull().sum() / len(df) * 100).round(1)
    }).sort_values("결측치 비율(%)", ascending=False)

    st.dataframe(null_info, use_container_width=True)

# ---------------------- 월별 평균 점수 ----------------------
def render_score_trend(df):
    st.subheader("월별 평균 위험 점수")
    df = preprocess_month_column(df)

    monthly_score = (
        df.groupby("월")["FINAL_SCORE"]
        .mean()
        .reset_index()
        .sort_values("월")
    )

    chart = alt.Chart(monthly_score).mark_line(point=True).encode(
        x=alt.X("월:T", title="월"),
        y=alt.Y("FINAL_SCORE:Q", title="평균 위험 점수"),
        tooltip=["월", "FINAL_SCORE"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

# ---------------------- 위험 등급 분포 ----------------------
def render_danger_distribution(df):
    st.subheader("월별 위험 등급 분포")
    df = preprocess_month_column(df)

    danger_dist = (
        df.groupby(["월", "DANGER_LEVEL"])
        .size()
        .reset_index(name="건수")
        .sort_values("월")
    )

    chart = alt.Chart(danger_dist).mark_bar().encode(
        x=alt.X("월:T", title="월"),
        y=alt.Y("건수:Q"),
        color="DANGER_LEVEL:N",
        tooltip=["월", "DANGER_LEVEL", "건수"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

# ---------------------- 지역별 탐색 ----------------------
def render_region_explorer(df):
    st.subheader("지역별 위험도 탐색")
    region = st.selectbox("지역 선택", sorted(df["REGION_NAME"].dropna().unique()))
    region_df = df[df["REGION_NAME"] == region].copy()
    region_df = preprocess_month_column(region_df)

    columns_to_plot = [
        "NORM_PRICE", "NORM_MOBILITY", "NORM_ASSETS",
        "NORM_FOOD", "NORM_CLOSE", "FINAL_SCORE"
    ]
    column_labels = {
        "NORM_PRICE": "가격 지수", "NORM_MOBILITY": "유동인구 지수",
        "NORM_ASSETS": "자산 지수", "NORM_FOOD": "음식 매출 지수",
        "NORM_CLOSE": "폐업률", "FINAL_SCORE": "최종 점수"
    }

    region_df["월"] = region_df["MONTH"].dt.strftime("%Y-%m")

    monthly_avg = (
        region_df.groupby("월")[columns_to_plot]
        .mean()
        .rename(columns=column_labels)
        .sort_index()
    )
    st.line_chart(monthly_avg, use_container_width=True)

    table_df = (
        region_df[["월"] + columns_to_plot + ["DANGER_LEVEL"]]
        .rename(columns={**column_labels, "DANGER_LEVEL": "위험 등급"})
        .groupby("월", as_index=False)
        .agg({
            **{label: "mean" for label in column_labels.values()},
            "위험 등급": lambda x: x.mode().iloc[0] if not x.mode().empty else None
        })
        .sort_values("월")
    )

    st.markdown("#### 월별 지역 위험도 요약 테이블")
    st.dataframe(table_df, use_container_width=True)

# ---------------------- 실행 ----------------------
def main():
    render_hero()

    try:
        df = get_data()
    except Exception as e:
        st.error(f"❌ 데이터 로딩 실패: {e}")
        st.stop()

    tabs = st.tabs(["데이터 요약", "월별 트렌드", "위험등급 분포", "지역별 탐색"])

    with tabs[0]: render_data_overview(df)
    with tabs[1]: render_score_trend(df)
    with tabs[2]: render_danger_distribution(df)
    with tabs[3]: render_region_explorer(df)

    # 푸터
    st.divider()
    st.markdown("""
        <div style='text-align: center; font-size: 0.9rem; color: gray;'>
            ⓒ 2025 Gentrification Insight. Powered by Streamlit & Snowflake  
            <br>데이터 출처: 서울열린데이터광장, 공공데이터포털, Snowflake Marketplace(SPH, DataKnows, LOPLAT), 국세청, 소상공인시장진흥공단 
            <br>Contact: hhee200456@gmail.com
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
