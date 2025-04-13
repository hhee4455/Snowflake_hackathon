import streamlit as st

st.set_page_config(page_title="플랫폼 요약 및 향후 계획", layout="wide")

# ---------------------- 헤더 ----------------------
st.markdown("""
    <div style='padding: 2.5rem 2rem; background: linear-gradient(90deg, #10B981, #4F46E5); border-radius: 1rem; color: white; text-align: center;'>
        <h1 style='margin-bottom: 0.5rem;'>플랫폼 요약 및 향후 계획</h1>
        <p style='font-size: 1.1rem;'>젠트리피케이션 위험도 분석 플랫폼의 구성 요약, 데이터 처리 방식, 확장 방향을 정리합니다.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------- 플랫폼 구성 ----------------------
st.markdown("## 플랫폼 구성 요약")
st.markdown("""
- 위험도 지도 시각화: 지역별 월간 젠트리피케이션 점수를 시각적으로 표현
- 데이터 분석 대시보드: 주요 지표 요약, 결측치 현황, 월별 및 지역별 분석
- LLM 리포트 생성: 지역·연도별 정책 분석 요약 자동 생성 (Snowflake Cortex 사용)
""")

# ---------------------- 데이터 구조 ----------------------
st.markdown("## 데이터 출처 및 처리 구조")

st.markdown("### 데이터 출처")
st.markdown("""
- **DataKnows**
  - 아파트 시세 (리치고 AI 시세 기반, 2020–2024)
  - 인구 데이터 및 여성·영유아 인구 (2025년 1월 기준)
- **SPH**
  - SKT 유동인구 데이터 (2021–2023, 월별)
  - KCB 자산·소득 데이터 (2021–2023, 월별)
  - 신한카드 소비 내역 (2021–2023, 월별)
- **공공데이터포털**
  - 프랜차이즈 점포 수, 창·폐업률, 업종별 매출, 점포 통계 등
- **Snowflake Marketplace & Cortex**
  - 데이터 저장 및 SQL 분석 환경
  - LLM 기반 정책 리포트 자동 생성 (Claude 3.5)
""")

st.markdown("### 데이터 처리 테이블 구조")
st.code("""
MART_DB.RAW           원천 데이터
DEV_DB.RAW            표준화 및 정제 전처리
DEV_DB.MART           월별 트렌드 집계
RESULT_DB.RESULT      최종 점수, 정규화 지표, 위험 등급 포함
""", language="sql")

st.markdown("### 전처리 및 정규화 방식")
st.markdown("""
1. 지역명 표준화 (`LOWER + TRIM`)
2. 날짜 통일 (`YYYY-MM-01`)
3. 결측치 제거 및 이상치 필터링
4. `Log + MinMax 정규화`: 가격, 유동인구, 매출 등
5. `MinMax 정규화`: 폐업률, 비율 지표 등
6. 가중합 기반 `FINAL_SCORE` 산출 → `DANGER_LEVEL` 분류
""")

# ---------------------- 지표 및 점수 산출 ----------------------
st.markdown("## 젠트리피케이션 위험도 점수 산출 기준")

st.markdown("""
| 지표 | 가중치 |
|------|--------|
| 아파트 시세           | 20% |
| 유동인구              | 12% |
| 자산 수준             | 10% |
| 전체 매출             | 10% |
| 폐업률                | 8%  |
| 프랜차이즈 비중        | 10% |
| 음식 매출             | 10% |
| 전문업종 비중          | 5%  |
| 업종 다양성           | 5%  |
| 브랜드 지배율          | 10% |

- `FINAL_SCORE`에 따라 `높음`, `보통`, `낮음`으로 위험 등급 분류
""")

# ---------------------- 확장 가능성 ----------------------
st.markdown("## 향후 확장 방향")

st.markdown("""
- 행정동/건물 단위로 정밀도 확대
- 이메일 및 슬랙 연동 리포트 자동 전송
- 사용자 로그인 기반 개인화 리포트 제공
- 다국어 지원, GPT-4 Vision 연계
- 행정기관·지역언론용 데이터 API 제공
""")

# ---------------------- 제작 정보 ----------------------
st.divider()
st.markdown("## 프로젝트 정보")

st.markdown("""
- 프로젝트명: 젠트리피케이션 위험도 분석 플랫폼
- 목적: 공공데이터 기반의 지역 상권 변화 진단 및 정책 판단 보조
- 개발 스택: Streamlit, Snowflake, Cortex LLM, Pandas, Altair
- 데이터 기준일: 2020 ~ 2023년
""")

st.success("플랫폼에 방문해주셔서 감사합니다. 상단 탭을 통해 다시 기능을 체험해보실 수 있습니다.")
