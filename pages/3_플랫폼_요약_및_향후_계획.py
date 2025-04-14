import streamlit as st

st.set_page_config(page_title="플랫폼 요약 및 향후 계획", layout="wide")

# ---------------------- 헤더 ----------------------
def render_header():
    st.markdown("""
        <div style='padding: 2.5rem 2rem; background: linear-gradient(90deg, #10B981, #4F46E5); border-radius: 1rem; color: white; text-align: center;'>
            <h1 style='margin-bottom: 0.5rem;'>젠트리피케이션 플랫폼 요약 및 확장 전략</h1>
            <p style='font-size: 1.1rem;'>젠트리피케이션 위험도 분석 플랫폼의 구조, 데이터 파이프라인, 기술 활용도, 확장 전략을 소개합니다.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    ### 플랫폼 목표
    공공 데이터와 상권 데이터를 결합하여 젠트리피케이션 리스크를 조기에 진단하고,  
    정책 수립 및 사회적 개입 타이밍을 지원하는 데이터 기반 플랫폼입니다.

    > "우리는 단순한 시각화가 아닌, **데이터 기반 정책 의사결정 도구**를 만드는 것이 목표입니다."
    """)
    st.divider()

# ---------------------- 구성 설명 ----------------------
def render_summary():
    st.markdown("## 🔧 시스템 구성")
    st.markdown("""
    ### 전체 데이터 플로우
    
    ```text
    [외부 데이터 수집] → [Snowflake ETL 정제] → [표준화된 RAW/MART 테이블 저장] →
    [분석 결과 RESULT 테이블 생성] → [Streamlit 시각화 & LLM 기반 리포트 생성]
    ```

    ### 데이터베이스 구조
    
    - **MART_DB.RAW**: 원천 데이터 (API, CSV, Marketplace 등 직접 수집)
    - **DEV_DB.RAW**: 정제 중간 단계 (필터링, 파싱, 매핑 적용 전)
    - **DEV_DB.MART**: 정규화 완료 테이블 (지표별로 Aggregation 및 스코어 계산)
    - **RESULT_DB.RESULT**: 최종 점수, 정규화 지표, 위험 등급 포함된 테이블

    > 최종적으로 사용되는 테이블은 `RESULT_DB.RESULT.GENTRIFICATION_STRICT`입니다.

    ### 주요 컬럼 설명 (RESULT.GENTRIFICATION_STRICT)

    | 컬럼명           | 설명                          |
    |------------------|-------------------------------|
    | REGION_NAME      | 행정구 이름                  |
    | MONTH            | 연-월 날짜 정보               |
    | FINAL_SCORE      | 가중합으로 계산된 최종 위험 점수 |
    | DANGER_LEVEL     | 점수에 따른 위험 등급 (낮음/보통/높음) |
    | NORM_PRICE       | 정규화된 평균 가격 지표        |
    | NORM_CLOSE       | 폐업률 정규화 지표             |
    | NORM_FOOD        | 음식 매출 정규화 지표          |
    | NORM_MOBILITY    | 유동인구 지표                  |
    | NORM_DOMINANT    | 브랜드 지배율 지표             |

    ### 처리 방식 요약
    - SQL 기반 분석 뷰에서 지표별 점수를 정규화 후 `FINAL_SCORE`를 생성
    - `DANGER_LEVEL`은 FINAL_SCORE 구간 기준으로 분류 (0.33 이하: 낮음, 0.33~0.66: 보통, 그 이상: 높음)
    - Streamlit에서 이 결과를 기반으로 지도 시각화 및 시계열 분석 진행
    - Cortex LLM을 통해 특정 지역/연도의 결과를 요약 리포트 형태로 출력
    """)

    st.markdown("## 🧩 데이터 수집 & 정제")
    st.markdown("""
    - **데이터 소스**:
        - `DataKnows`: 부동산 시세 (2020–2024), 인구 통계
        - `SPH`: 유동인구, 소비 매출, 자산 정보 (2021–2023)
        - `공공데이터포털`: 점포수, 창·폐업률, 프랜차이즈 분포, 업종별 매출 등
    - **전처리 과정**:
        - 지역명 정제, 월 기준 통일, 결측치 제거 및 이상치 필터링
        - MinMax 정규화 및 로그 스케일링 → 10개 지표 정규화
        - 각 지표별 가중합을 통한 `FINAL_SCORE` 산출 → 위험 등급 (`DANGER_LEVEL`) 분류
    - **파이프라인 운영 방식**:
        - Snowflake SQL로 재사용 가능한 분석 뷰 구축
        - 월 단위 데이터 자동 적재 및 처리 계획 예정
    """)

    st.markdown("## 위험 점수 산정 기준")
    st.markdown("""
    플랫폼은 다양한 도시 지표를 종합해 젠트리피케이션 가능성을 수치화합니다.  
    각 지표의 중요도는 전문가 의견 및 데이터 EDA 기반으로 설정되었습니다:
    """)
    st.dataframe({
        "지표": [
            "아파트 시세", "유동인구", "자산 수준", "전체 매출", "폐업률",
            "프랜차이즈 비중", "음식 매출", "전문업종 비중", "업종 다양성", "브랜드 지배율"
        ],
        "가중치 (%)": [20, 12, 10, 10, 8, 10, 10, 5, 5, 10]
    })
    st.caption("※ 실제 비즈니스/사회적 영향도와 상관관계를 고려하여 수치화")

# ---------------------- 확장 전략 ----------------------
def render_roadmap():
    st.markdown("## 향후 확장 전략")
    st.markdown("""
    ### 1. 지리적 정밀도 강화
    - 현재: 구 단위 → 목표: 행정동/상권/건물 단위로 확대
    - 데이터 소스: 부동산 실거래가 API, 상가 건물 등급 등 추가 확보 예정

    ### 2. 예측 기반 정책 시뮬레이션
    - Snowflake ML SQL (`FORECAST`, `ANOMALY_DETECTION`)로 수치 예측
    - 예: "3개월 후 위험 급등 예상 지역 TOP5" 자동 추천

    ### 3. Slack/Email 알림 연동
    - 위험도 급등 감지 시 Slack 메시지 자동 발송
    - 담당자에게 주간 이메일 보고서 전송 기능

    ### 4. 사용자 맞춤형 리포트 / 로그인 시스템
    - 즐겨찾기 지역 저장 → 사용자 대시보드에 반영
    - 자동화된 개인화 리포트 (예: 내 동네 위험도 리포트)

    """)

# ---------------------- 실행 ----------------------
def main():
    render_header()
    render_summary()
    st.divider()
    render_roadmap()

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