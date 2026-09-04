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
# 그래프 2: 장르 안에 영화가 들어 있는 트리맵 (칸 크기: 총 관객수)
# =========================================================
st.header("2. 장르별 영화의 총 관객수 (트리맵)")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],  # 장르 -> 영화명 계층 구조
    values="total_audi",         # 칸의 크기는 총 관객수
    custom_data=["movieNm", "total_audi"],
    title="장르 안의 영화별 총 관객수"
)

# 마우스를 올리면 영화명과 총 관객수가 보이도록 hovertemplate 설정
fig2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>총 관객: %{customdata[1]:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("2번 그래프 해석을 적어보세요.", key="insight2_treemap", height=80)

st.divider()

# =========================================================
# 그래프 3: 총 관객수 히스토그램
# =========================================================
st.header("3. 총 관객수 분포")

fig3_audi = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객수"},
    title="영화별 총 관객수 분포"
)
fig3_audi.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig3_audi, use_container_width=True)

# ---- 자동 계산: 가장 많이 몰려 있는 구간 찾기 ----
bin_counts, bin_edges = pd.cut(df["total_audi"], bins=30, retbins=True)
most_common_bin = bin_counts.value_counts().idxmax()
most_common_bin_count = bin_counts.value_counts().max()

# ---- 자동 계산: 가장 관객이 많은 영화 찾기 ----
top_movie_row = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie_row["movieNm"]
top_movie_audi = top_movie_row["total_audi"]

st.markdown(f"""
- 📊 **가장 많은 영화가 몰려 있는 구간:** 약 `{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명` 구간에 **{most_common_bin_count}편**이 분포합니다.
- 🏆 **총 관객수가 가장 많은 영화:** **{top_movie_name}** (총 관객 `{top_movie_audi:,.0f}명`)
""")

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("3번 그래프 해석을 적어보세요.", key="insight3_audi", height=80)

st.divider()

# =========================================================
# 그래프 4: 개봉일 스크린수 vs 총 관객수 - 산점도 (장르별 색상 구분)
# =========================================================
st.header("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre": "장르"
    },
    title="개봉일 스크린수 vs 총 관객수 (장르별 색상)"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("4번 그래프 해석을 적어보세요.", key="insight4_scatter", height=80)

st.divider()

# =========================================================
# 그래프 5: 영화 10편 이상 장르의 총 관객수 박스플롯 (이상치에 영화명 표시)
# =========================================================
st.header("5. 영화 10편 이상 장르의 총 관객수 분포")

# 장르별 영화 편수를 세어 10편 이상인 장르만 선택
genre_movie_counts = df["genre"].value_counts()
major_genres = genre_movie_counts[genre_movie_counts >= 10].index.tolist()
df_major = df[df["genre"].isin(major_genres)]

st.caption(f"영화가 10편 이상인 장르: {', '.join(major_genres)}")

fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    points="outliers",       # 상자 밖 이상치만 점으로 표시
    hover_data=["movieNm"],  # 이상치에 마우스를 올리면 영화명이 보이도록 설정
    labels={"genre": "장르", "total_audi": "총 관객수"},
    title="영화 10편 이상 장르의 총 관객수 박스플롯"
)
fig5.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("5번 그래프 해석을 적어보세요.", key="insight5_box", height=80)

st.divider()

# =========================================================
# 그래프 6: 개봉일 스크린수 vs 총 관객수 - 버블 그래프
# (4번 산점도에 점 크기를 첫 주 관객수로 추가한 버전)
# =========================================================
st.header("6. 개봉일 스크린수와 총 관객수의 관계 (버블 크기: 첫 주 관객수)")

fig6_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",   # 점 크기를 첫 주 관객수로 설정
    color="genre",
    hover_name="movieNm",
    size_max=40,               # 버블이 너무 커지지 않도록 최대 크기 제한
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "first_week_audi": "첫 주 관객수",
        "genre": "장르"
    },
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 첫 주 관객수)"
)

st.plotly_chart(fig6_bubble, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("6번 그래프 해석을 적어보세요.", key="insight6_bubble", height=80)

st.divider()

# =========================================================
# 그래프 7: 국가 -> 장르 선버스트 그래프 (칸 크기: 영화 편수)
# =========================================================
st.header("7. 제작 국가별 장르 분포 (선버스트)")

# 국가-장르별 영화 편수 집계
nation_genre_counts = (
    df.groupby(["nation", "genre"])
    .size()
    .reset_index(name="count")
)

fig7_sunburst = px.sunburst(
    nation_genre_counts,
    path=["nation", "genre"],  # 국가 -> 장르 계층 구조
    values="count",             # 칸의 크기는 영화 편수
    custom_data=["count"],
    title="제작 국가별 장르 구성"
)

fig7_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{customdata[0]}편<extra></extra>"
)

st.plotly_chart(fig7_sunburst, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("7번 그래프 해석을 적어보세요.", key="insight7_sunburst", height=80)

st.divider()

# =========================================================
# 그래프 8: 개봉일 스크린수 분포 - 히스토그램
# =========================================================
st.header("8. 개봉일 스크린수 분포")

fig8_hist = px.histogram(
    df,
    x="first_scrn",
    nbins=30,
    labels={"first_scrn": "개봉일 스크린수"},
    title="개봉일 스크린수 분포"
)
fig8_hist.update_layout(yaxis_title="영화 편수")

st.plotly_chart(fig8_hist, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("8번 그래프 해석을 적어보세요.", key="insight8_hist", height=80)

st.divider()

# =========================================================
# 그래프 9: 10위권 유지 일수와 총 관객수의 관계 - 산점도 (버블 크기 활용)
# =========================================================
st.header("9. 10위권 유지 일수와 총 관객수의 관계")

fig9 = px.scatter(
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

st.plotly_chart(fig9, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("9번 그래프 해석을 적어보세요.", key="insight9", height=80)

st.divider()

st.info("각 그래프 아래 텍스트 상자에 스스로 발견한 내용을 정리해 보세요!")
