import streamlit as st
import pandas as pd
from utils.snowflake import get_snowpark_session
from utils.pdf_utils import generate_pdf

# ---------------------- 페이지 설정 ----------------------
st.set_page_config(
    page_title="젠트리피케이션 지역별 요약 리포트",
    layout="wide"
)

# ---------------------- 헤더 ----------------------
st.markdown("""
    <div style='padding: 2.5rem 2rem; background: linear-gradient(90deg, #4F46E5, #9333EA); border-radius: 1rem; color: white; text-align: center;'>
        <h1 style='margin-bottom: 0.5rem;'>📄 젠트리피케이션 지역별 요약 리포트</h1>
        <p style='font-size: 1.1rem;'>선택한 지역과 연도를 기반으로 위험도 데이터를 분석하고, LLM이 자동 작성한 정책 보고서를 제공합니다.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------- 유도 메시지 (최초 1회) ----------------------
if "shown_tip" not in st.session_state:
    st.info("⚠️ 리포트 생성은 서버 리소스를 사용하므로 꼭 필요한 경우에만 눌러주세요.")
    st.session_state.shown_tip = True

# ---------------------- 데이터 로딩 ----------------------
try:
    session = get_snowpark_session()
    df = session.table("RESULT_DB.RESULT.GENTRIFICATION_STRICT").to_pandas()
except Exception as e:
    st.error(f"❌ Snowflake 연결 실패: {e}")
    st.stop()

df["YEAR"] = pd.to_datetime(df["MONTH"]).dt.year
df["MONTH_STR"] = pd.to_datetime(df["MONTH"]).dt.strftime("%Y-%m")

region_list = sorted(df["REGION_NAME"].dropna().unique())
year_list = sorted(df["YEAR"].dropna().unique(), reverse=True)

selected_region = st.selectbox("📍 지역 선택", region_list)
selected_year = st.selectbox("📅 연도 선택", year_list)

filtered = df[(df["REGION_NAME"] == selected_region) & (df["YEAR"] == selected_year)]

# ---------------------- 버튼 및 LLM 실행 ----------------------
if st.button("🧠 LLM 분석 리포트 생성"):
    if filtered.empty:
        st.warning("선택한 조건에 맞는 데이터가 없습니다.")
    else:
        with st.spinner("⏳ 분석 중입니다..."):
            try:
                # 📄 프롬프트 구성
                prompt = f"""
다음은 {selected_year}년 동안 {selected_region}의 월별 젠트리피케이션 위험도 데이터입니다.
각 항목은 [월 - 지역명: 점수 (등급)] 형식입니다.

""" + "\n".join(
    f"{row.MONTH_STR} - {row.REGION_NAME}: 위험도 {round(row.FINAL_SCORE, 2)} ({row.DANGER_LEVEL})"
    for row in filtered.itertuples()
) + f"""

이 데이터를 바탕으로 아래 내용을 포함한 정책 분석 보고서를 작성해주세요 (16~18줄 이내):

1. 연중 평균 및 최고 위험도 수준과 해당 월
2. 점수 상승/하락 시기와 원인에 대한 추론
3. 유동인구, 매출, 폐업률 등 상권 변화 요소와의 관련성
4. 자영업자 및 저소득층에 미치는 사회적 영향
5. 향후 정책 개입 또는 모니터링 방향 제언

문체는 도시 정책 보고서처럼 전문적이고 신뢰성 있게 작성해주세요.
"""

                # 🤖 LLM 호출
                cortex_query = f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'claude-3-5-sonnet',
                    $$ {prompt} $$
                ) AS SUMMARY
                """
                result_df = session.sql(cortex_query).to_pandas()
                summary_text = result_df.iloc[0, 0]

                # 📋 결과 출력
                st.success("✅ 리포트 생성 완료!")
                st.markdown("#### 📋 LLM 분석 결과")
                st.text_area("LLM이 생성한 정책 보고서 요약", summary_text, height=300)

                # 📄 PDF 다운로드
                pdf_bytes = generate_pdf(selected_region, selected_year, summary_text)

                st.download_button(
                    label="📄 리포트 다운로드 (PDF)",
                    data=pdf_bytes,
                    file_name=f"{selected_region}_{selected_year}_젠트리피케이션_리포트.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"❌ 리포트 생성 실패: {e}")

st.divider()
st.markdown("""
    <div style='text-align: center; font-size: 0.9rem; color: gray;'>
        ⓒ 2025 Gentrification Insight. Powered by Streamlit & Snowflake  
        <br>데이터 출처: 서울열린데이터광장, 공공데이터포털, Snowflake Marketplace(SPH,DataKnows,LOPLAT), 국세청, 소상공인시장진흥공단 
        <br>Contact: hhee200456@gmail.com
    </div>
""", unsafe_allow_html=True)