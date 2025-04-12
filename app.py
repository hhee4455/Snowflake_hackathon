# app.py
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="젠트리피케이션 위험도 분석 플랫폼",
    page_icon="🌇",
    layout="wide"
)

# Custom CSS for layout and branding
st.markdown("""
    <style>
        .hero {
            background: linear-gradient(to right, rgba(0,0,0,0.5), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1549924231-f129b911e442');
            padding: 4rem 2rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            background-size: cover;
            background-position: center;
        }
        .hero h1 {
            font-size: 3rem;
            font-weight: bold;
        }
        .hero p {
            font-size: 1.25rem;
            margin-top: 1rem;
        }
        .section-title {
            font-size: 1.8rem;
            font-weight: bold;
            color: #2C3E50;
            margin-top: 3rem;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>젠트리피케이션 위험도 분석 플랫폼</h1>
    <p>젠트리피케이션 위험도를 데이터 기반으로 분석하고 예측하는 시각화 플랫폼입니다.</p>
</div>
""", unsafe_allow_html=True)

# 프로젝트 개요
st.markdown("<div class='section-title'>📌 프로젝트 개요</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.subheader("🎯 프로젝트 목적")
    st.write("""
    - 상권 변화와 부동산 가격 상승에 따른 젠트리피케이션 위험을 조기에 감지
    - 시계열 및 다변량 지표를 활용한 점수화로 정량적 판단 근거 제공
    """)
with col2:
    st.subheader("📊 데이터 출처 및 분석 방식")
    st.write("""
    - APT, MOBILITY, ASSET, CONSUMPTION 등 상권 데이터 활용
    - LEFT JOIN & 정규화 후 가중치 기반 점수 계산
    - 위험도는 FINAL_SCORE 및 DANGER_LEVEL로 분류
    """)

# 시스템 아키텍처
st.markdown("<div class='section-title'>🧱 시스템 아키텍처</div>", unsafe_allow_html=True)
col3, col4, col5, col6 = st.columns(4)
col3.metric("📦 Snowflake", "데이터 저장 및 처리")
col4.metric("🧮 SQL + 정규화", "가중치 점수 생성")
col5.metric("📈 GENTRIFICATION_SCORE", "최종 테이블")
col6.metric("💻 Streamlit", "시각화 및 인터페이스")

# 데이터 구성
st.markdown("<div class='section-title'>🗂 데이터 구성</div>", unsafe_allow_html=True)
data1, data2 = st.columns(2)
with data1:
    st.subheader("📄 GENTRIFICATION_SCORE")
    st.markdown("""
    - 전체 지역 + 월 포함 (결측 허용)
    - 주요 컬럼: `month`, `region_name`, `final_score`, `danger_level`
    """)
with data2:
    st.subheader("📑 GENTRIFICATION_STRICT")
    st.markdown("""
    - 결측 없는 완전 정합 데이터셋
    - 학습 및 모델링에 적합
    """)

# 주요 변수 시각화 (예시 Plotly 그래프)
st.markdown("<div class='section-title'>📊 주요 변수 시계열</div>", unsafe_allow_html=True)
st.plotly_chart(px.line(
    x=["2022-01", "2022-06", "2023-01", "2023-06", "2024-01"],
    y=[0.42, 0.48, 0.52, 0.59, 0.66],
    labels={'x': '월', 'y': 'Final Score'},
    title="샘플 지역 위험도 점수 추이"
), use_container_width=True)

# 주요 기능 카드
st.markdown("<div class='section-title'>🛠 주요 기능</div>", unsafe_allow_html=True)
f1, f2, f3 = st.columns(3)
with f1:
    st.info("📍 위험도 지도", icon="📍")
    st.write("지역별 젠트리피케이션 점수를 지도 기반으로 시각화")
with f2:
    st.info("📋 리포트 생성", icon="📝")
    st.write("지역별 주요 요인을 정리하여 텍스트 리포트 제공")
with f3:
    st.info("📈 데이터 탐색", icon="📊")
    st.write("다변량 지표 및 상관관계 시각화 기능")

# 추가 정보
st.markdown("<div class='section-title'>🔍 추가 정보</div>", unsafe_allow_html=True)
extra1, extra2 = st.columns(2)
with extra1:
    st.subheader("🌱 향후 발전 방향")
    st.markdown("""
    - LLM 활용 자연어 리포트 생성
    - 유사 지역 추천 모델 도입
    - 실시간 API/자동화 시스템 연동
    """)
with extra2:
    st.subheader("🏛 정책 적용 가능성")
    st.markdown("""
    - 지역별 위험도에 따른 선제 개입 타이밍 도출
    - 지자체별 정책 성과 분석 리포트 생성
    - 도시재생 정책의 타겟 설정 도우미로 활용 가능
    """)
