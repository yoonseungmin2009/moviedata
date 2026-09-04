import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown("""
이 앱은 1년간 박스오피스 10위권에 든 영화 216편의 데이터를 활용하여
**분포와 관계**를 다양한 그래프로 살펴봅니다.
""")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # genre 열에서 세로막대(|)로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # 개봉일(openDt)을 날짜 형식으로 변환 (여덟 자리 숫자 -> 날짜)
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    return df

df = load_data()

# 데이터 미리보기
with st.expander("원본 데이터 미리보기"):
    st.dataframe(df)

st.divider()

# =========================================================
# 그래프 1: 장르별 영화 편수 - 도넛 그래프
# =========================================================
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = go.Figure(
    data=[
        go.Pie(
            labels=genre_counts["genre"],
            values=genre_counts["count"],
            hole=0.5,  # 도넛 모양을 위한 구멍 크기
            hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
        )
    ]
)
fig1.update_layout(
    title="장르별 영화 편수 비율",
    legend_title="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("1번 그래프 해석을 적어보세요.", key="insight1", height=80)

st.divider()

# =========================================================
# 그래프 2: 개봉일 스크린수 분포 - 히스토그램
# =========================================================
st.header("2. 개봉일 스크린수 분포")

fig2 = px.histogram(
    df,
    x="first_scrn",
    nbins=30,
    labels={"first_scrn": "개봉일 스크린수"},
    title="개봉일 스크린수 분포"
)
fig2.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("2번 그래프 해석을 적어보세요.", key="insight2", height=80)

st.divider()

# =========================================================
# 그래프 3: 개봉일 스크린수 vs 총 관객수 - 산점도
# =========================================================
st.header("3. 개봉일 스크린수와 총 관객수의 관계")

fig3 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    hover_name="movieNm",
    color="genre",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르"
    },
    title="개봉일 스크린수 vs 총 관객수"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("3번 그래프 해석을 적어보세요.", key="insight3", height=80)

st.divider()

# =========================================================
# 그래프 4: 장르별 총 관객수 분포 - 박스플롯
# =========================================================
st.header("4. 장르별 총 관객수 분포")

fig4 = px.box(
    df,
    x="genre",
    y="total_audi",
    labels={"genre": "장르", "total_audi": "총 관객수"},
    title="장르별 총 관객수 분포"
)
fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("4번 그래프 해석을 적어보세요.", key="insight4", height=80)

st.divider()

# =========================================================
# 그래프 5: 10위권 유지 일수와 총 관객수의 관계 - 산점도 (버블 크기 활용)
# =========================================================
st.header("5. 10위권 유지 일수와 총 관객수의 관계")

fig5 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    size="first_show",
    color="genre",
    hover_name="movieNm",
    labels={
        "days_in_top10": "10위권 유지 일수",
        "total_audi": "총 관객수",
        "first_show": "개봉일 상영횟수",
        "genre": "장르"
    },
    title="10위권 유지 일수 vs 총 관객수 (버블 크기: 개봉일 상영횟수)"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("5번 그래프 해석을 적어보세요.", key="insight5", height=80)

st.divider()

st.info("각 그래프 아래 텍스트 상자에 스스로 발견한 내용을 정리해 보세요!")
