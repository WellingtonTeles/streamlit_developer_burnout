import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Portfólio Analítico | Burnout de Desenvolvedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    numeric_cols = [
        "age",
        "experience_years",
        "daily_work_hours",
        "sleep_hours",
        "caffeine_intake",
        "bugs_per_day",
        "commits_per_day",
        "meetings_per_day",
        "screen_time",
        "exercise_hours",
        "stress_level",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eixo temporal sintético para análises de tendência em portfólio.
    df["analysis_date"] = pd.date_range("2024-01-01", periods=len(df), freq="D")

    burnout_map = {"Low": 1, "Medium": 2, "High": 3}
    df["burnout_score"] = df["burnout_level"].map(burnout_map).astype(float)

    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 25, 35, 45, 60],
        labels=["18-25", "26-35", "36-45", "46-60"],
        include_lowest=True,
    )
    df["job_role"] = pd.cut(
        df["experience_years"],
        bins=[-1, 2, 5, 10, 50],
        labels=["Júnior", "Pleno", "Sênior", "Staff/Lead"],
    )

    # Proxies explícitos para segmentação executiva quando a fonte não traz
    # gênero/cargo/empresa nominal.
    idx_mod = np.arange(len(df)) % 3
    df["gender_proxy"] = np.select(
        [idx_mod == 0, idx_mod == 1, idx_mod == 2],
        ["Feminino", "Masculino", "Não-binário"],
        default="Não informado",
    )

    df["company_profile"] = np.select(
        [
            (df["meetings_per_day"] <= 2) & (df["commits_per_day"] >= 15),
            (df["meetings_per_day"] >= 6),
            (df["daily_work_hours"] >= 10),
        ],
        ["Produto Ágil", "Corporativa", "Operação Intensiva"],
        default="Balanced Tech",
    )
    df["high_burnout"] = (df["burnout_level"] == "High").astype(int)
    return df


def inject_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg-main: radial-gradient(circle at 10% 10%, #132238 0%, #0b1220 45%, #070d16 100%);
                --card-bg: linear-gradient(135deg, #101826 0%, #1b2a41 100%);
                --surface: rgba(13, 25, 44, 0.7);
                --border: rgba(214, 231, 255, 0.18);
                --accent: #66d9ff;
                --text-strong: #f4f8ff;
                --text-soft: #d5e4f4;
                --text-muted: #b9cde0;
                --radius: 14px;
                --space-1: 0.4rem;
                --space-2: 0.7rem;
                --space-3: 1rem;
                --space-4: 1.4rem;
                --fs-0: 0.85rem;
                --fs-1: 0.95rem;
                --fs-2: 1.05rem;
                --fs-3: 1.3rem;
                --fs-4: 1.65rem;
                --ok: #2dd4bf;
                --warn: #f59e0b;
                --danger: #ef4444;
            }
            @media (prefers-color-scheme: light) {
                :root {
                    --bg-main: linear-gradient(180deg, #f3f7ff 0%, #e9f0fb 100%);
                    --card-bg: linear-gradient(180deg, #ffffff 0%, #f5f8ff 100%);
                    --surface: rgba(255, 255, 255, 0.95);
                    --border: rgba(31, 58, 100, 0.16);
                    --accent: #0068c9;
                    --text-strong: #0f1b2d;
                    --text-soft: #243b57;
                    --text-muted: #3a516a;
                }
            }
            .stApp {
                background: var(--bg-main);
            }
            .stApp [data-testid="stAppViewContainer"] > .main .block-container {
                padding-top: 1.1rem;
                padding-bottom: 1.4rem;
                max-width: 1450px;
            }
            .stApp [data-testid="stHorizontalBlock"] {
                gap: 0.9rem;
            }
            .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
                color: var(--text-strong) !important;
                font-weight: 700;
                letter-spacing: 0.2px;
                line-height: 1.2;
            }
            .stApp p, .stApp li, .stApp label, .stApp small {
                color: var(--text-soft);
                line-height: 1.5;
                font-size: var(--fs-1);
            }
            .stApp h1 { font-size: calc(var(--fs-4) + 0.35rem); margin-bottom: var(--space-2); }
            .stApp h2 { font-size: var(--fs-4); margin-bottom: var(--space-2); }
            .stApp h3 { font-size: var(--fs-3); margin-bottom: var(--space-2); }
            .stApp h4 { font-size: var(--fs-2); margin-bottom: var(--space-1); }
            .stMarkdown {
                margin-bottom: var(--space-2);
            }
            .hero-card, .kpi-card {
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: var(--radius);
                padding: var(--space-3) calc(var(--space-3) + 0.2rem);
                box-shadow: 0 12px 26px rgba(0, 0, 0, 0.24);
                animation: fadeIn 0.45s ease-in-out;
            }
            .hero-title {
                font-size: var(--fs-4);
                font-weight: 700;
                color: var(--text-strong);
                margin-bottom: var(--space-1);
            }
            .hero-sub {
                color: var(--text-soft);
                font-size: var(--fs-2);
                margin-bottom: 0;
            }
            .kpi-label {
                color: var(--text-muted);
                font-size: var(--fs-0);
            }
            .kpi-value {
                color: var(--text-strong);
                font-size: var(--fs-4);
                font-weight: 700;
                margin: var(--space-1) 0;
            }
            .kpi-help {
                color: var(--text-muted);
                font-size: var(--fs-0);
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.45rem;
                overflow-x: auto;
                scrollbar-width: thin;
                padding-bottom: 0.2rem;
                margin-bottom: 0.25rem;
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: var(--radius);
                background: var(--surface);
                border: 1px solid var(--border);
                color: var(--text-strong);
                transition: transform .2s ease, background .2s ease, border-color .2s ease;
                white-space: normal !important;
                word-break: break-word;
                min-height: 2.6rem;
                height: auto;
                line-height: 1.25;
                padding: 0.5rem 0.8rem;
                flex: 0 0 auto;
                max-width: 15rem;
                font-weight: 600;
            }
            .stTabs [aria-selected="true"] {
                border-color: color-mix(in oklab, var(--accent) 45%, var(--border));
                background: color-mix(in oklab, var(--accent) 16%, transparent);
                color: var(--text-strong);
            }
            .stTabs [data-baseweb="tab"]:hover {
                transform: translateY(-1px);
                background: color-mix(in oklab, var(--accent) 14%, transparent);
                border-color: color-mix(in oklab, var(--accent) 35%, var(--border));
            }
            .stButton > button {
                border-radius: var(--radius) !important;
                border: 1px solid var(--border) !important;
                background: var(--surface) !important;
                color: var(--text-strong) !important;
                font-weight: 600 !important;
                white-space: normal !important;
                word-break: break-word;
                overflow-wrap: anywhere;
                min-height: 2.6rem;
                height: auto !important;
                line-height: 1.25 !important;
                padding: 0.55rem 0.8rem !important;
                font-size: var(--fs-1) !important;
            }
            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input,
            .stDateInput input,
            .stSelectbox [data-baseweb="select"],
            .stMultiSelect [data-baseweb="select"] {
                border-radius: var(--radius) !important;
                border: 1px solid var(--border) !important;
                color: var(--text-strong) !important;
                background: var(--surface) !important;
                font-size: var(--fs-1) !important;
            }
            div[data-testid="stDataFrame"],
            div[data-testid="stPlotlyChart"],
            div[data-testid="stAlert"],
            div[data-testid="stMetric"] {
                border-radius: var(--radius) !important;
                overflow: hidden;
                border: 1px solid var(--border);
                background: var(--surface);
            }
            div[data-testid="stMetricValue"] {
                color: var(--text-strong) !important;
                font-weight: 700 !important;
                font-size: var(--fs-3) !important;
            }
            div[data-testid="stMetricLabel"] {
                color: var(--text-muted) !important;
                font-size: var(--fs-0) !important;
            }
            div[data-testid="stPlotlyChart"] .js-plotly-plot,
            div[data-testid="stPlotlyChart"] .plot-container,
            div[data-testid="stPlotlyChart"] .svg-container {
                border-radius: var(--radius) !important;
            }
            .stApp a, .stApp a:visited {
                color: var(--accent);
            }
            .stApp *:focus-visible {
                outline: 2px solid var(--accent) !important;
                outline-offset: 2px !important;
                border-radius: 8px;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(6px);}
                to {opacity: 1; transform: translateY(0);}
            }
            @media (max-width: 1200px) {
                .stApp [data-testid="stHorizontalBlock"] {
                    gap: 0.7rem;
                }
                .kpi-value { font-size: var(--fs-3); }
                .hero-title { font-size: 1.45rem; }
            }
            @media (max-width: 900px) {
                .stApp [data-testid="stAppViewContainer"] > .main .block-container {
                    padding-top: 0.8rem;
                    padding-left: 0.6rem;
                    padding-right: 0.6rem;
                }
                .hero-title { font-size: 1.25rem; }
                .hero-sub { font-size: 0.95rem; }
                .kpi-value { font-size: 1.15rem; }
                .stTabs [data-baseweb="tab"] {
                    max-width: 12rem;
                    font-size: 0.9rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(title: str, value: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-help">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def inject_density_css(mode: str) -> None:
    if mode == "compact":
        css = """
        <style>
            :root {
                --space-1: 0.3rem;
                --space-2: 0.55rem;
                --space-3: 0.8rem;
                --space-4: 1.1rem;
                --fs-0: 0.8rem;
                --fs-1: 0.9rem;
                --fs-2: 0.98rem;
                --fs-3: 1.18rem;
                --fs-4: 1.45rem;
                --radius: 12px;
            }
            .stApp [data-testid="stAppViewContainer"] > .main .block-container {
                padding-top: 0.75rem !important;
                padding-bottom: 0.9rem !important;
            }
            .stApp [data-testid="stHorizontalBlock"] {
                gap: 0.6rem !important;
            }
            .stButton > button {
                min-height: 2.3rem !important;
                padding: 0.42rem 0.7rem !important;
            }
            .stTabs [data-baseweb="tab"] {
                min-height: 2.35rem !important;
                padding: 0.42rem 0.65rem !important;
                max-width: 12.5rem !important;
            }
            .hero-card, .kpi-card {
                padding: 0.8rem 0.95rem !important;
            }
        </style>
        """
    else:
        css = """
        <style>
            :root {
                --space-1: 0.4rem;
                --space-2: 0.7rem;
                --space-3: 1rem;
                --space-4: 1.4rem;
                --fs-0: 0.85rem;
                --fs-1: 0.95rem;
                --fs-2: 1.05rem;
                --fs-3: 1.3rem;
                --fs-4: 1.65rem;
                --radius: 14px;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)


I18N = {
    "PT_BR": {
        "lang_toggle": "Idioma / Language",
        "density_label": "Densidade visual",
        "density_comfortable": "Confortavel",
        "density_compact": "Compacto",
        "sidebar_header": "Filtros Dinamicos",
        "sidebar_caption": "Combine os filtros para analises granulares e comparativas.",
        "period": "Periodo",
        "age_range": "Faixa etaria",
        "work_hours": "Horas de trabalho/dia",
        "stress_level": "Nivel de estresse",
        "burnout_class": "Classe de burnout",
        "all": "Todas",
        "gender_proxy": "Genero (proxy)",
        "job_role": "Cargo (derivado)",
        "company_profile": "Perfil de empresa (proxy)",
        "empty_filter_warning": "Nenhum registro encontrado para os filtros atuais. Ajuste os criterios no menu lateral.",
        "tab_exec": "📌 Portfolio Executivo",
        "tab_explore": "🔎 Exploracao de Dados",
        "tab_segment": "🧩 Segmentacao",
        "tab_corr": "📈 Correlacoes e Relacoes",
        "tab_temporal": "🕒 Padroes Temporais",
        "tab_about": "ℹ️ Sobre",
        "hero_sub": "Portfolio analitico para demonstrar capacidade de diagnostico organizacional, monitoramento de risco psicossocial e suporte a decisao com dados.",
        "kpi_burnout": "Taxa de Burnout Alto",
        "kpi_burnout_sub": "Percentual da classe High",
        "kpi_stress": "Estresse Medio",
        "kpi_stress_sub": "Escala de 0 a 100",
        "kpi_hours": "Horas de Trabalho",
        "kpi_hours_sub": "Media diaria",
        "kpi_sleep": "Sono Medio",
        "kpi_sleep_sub": "Media de descanso",
        "key_indicators": "Principais Indicadores",
        "risk_factor": "Fator de risco predominante",
        "records": "Registros analisados",
        "window": "Janela temporal",
        "exec_layer": "Camada de segmentacao executiva com filtros em tempo real.",
        "burnout_distribution": "Distribuicao de Burnout (%)",
        "explore_title": "Exploracao Inicial e Estatisticas Descritivas",
        "mean": "Media",
        "median": "Mediana",
        "std": "Desvio Padrao",
        "hist_var": "Histograma da variavel:",
        "hist_dist_of": "Distribuicao de",
        "hist_age": "Distribuicao por Idade e Classe de Burnout",
        "segment_title": "Padroes por Genero, Experiencia, Cargo e Empresa",
        "segment_compare": "Comparar taxa de burnout alto por dimensao:",
        "high_rate_by": "Taxa de Burnout Alto por",
        "rate": "Taxa (%)",
        "hier_map": "Mapa Hierarquico de Intensidade de Burnout",
        "corr_title": "Correlacoes e Relacoes Entre Variaveis",
        "corr_heatmap": "Heatmap de Correlacao",
        "axis_x": "Eixo X",
        "axis_y": "Eixo Y",
        "relation_between": "Relacao entre",
        "temporal_title": "Mapa de Calor Temporal e Tendencias",
        "temporal_heat_title": "Intensidade Media de Burnout por Dia da Semana x Mes",
        "trend_title": "Tendencia Temporal de Risco",
        "high_burnout_pct": "Burnout Alto (%)",
        "avg_stress": "Estresse Medio",
        "about_title": "Metodologia e Fonte dos Dados",
        "about_info": "Personalize marca, cores e textos para usar este app como case comercial da sua empresa.",
    },
    "EN_US": {
        "lang_toggle": "Language / Idioma",
        "density_label": "Visual density",
        "density_comfortable": "Comfortable",
        "density_compact": "Compact",
        "sidebar_header": "Dynamic Filters",
        "sidebar_caption": "Combine filters for granular and comparative analysis.",
        "period": "Period",
        "age_range": "Age range",
        "work_hours": "Work hours/day",
        "stress_level": "Stress level",
        "burnout_class": "Burnout class",
        "all": "All",
        "gender_proxy": "Gender (proxy)",
        "job_role": "Role (derived)",
        "company_profile": "Company profile (proxy)",
        "empty_filter_warning": "No records found for current filters. Please adjust criteria in the sidebar.",
        "tab_exec": "📌 Executive Portfolio",
        "tab_explore": "🔎 Data Exploration",
        "tab_segment": "🧩 Segmentation",
        "tab_corr": "📈 Correlations and Relations",
        "tab_temporal": "🕒 Temporal Patterns",
        "tab_about": "ℹ️ About",
        "hero_sub": "Analytical portfolio to demonstrate organizational diagnostics, psychosocial risk monitoring, and data-driven decision support.",
        "kpi_burnout": "High Burnout Rate",
        "kpi_burnout_sub": "Percentage in High class",
        "kpi_stress": "Average Stress",
        "kpi_stress_sub": "Scale from 0 to 100",
        "kpi_hours": "Work Hours",
        "kpi_hours_sub": "Daily average",
        "kpi_sleep": "Average Sleep",
        "kpi_sleep_sub": "Average rest time",
        "key_indicators": "Key Indicators",
        "risk_factor": "Primary risk factor",
        "records": "Records analyzed",
        "window": "Time window",
        "exec_layer": "Executive segmentation layer with real-time filters.",
        "burnout_distribution": "Burnout Distribution (%)",
        "explore_title": "Initial Exploration and Descriptive Statistics",
        "mean": "Mean",
        "median": "Median",
        "std": "Std. Deviation",
        "hist_var": "Histogram variable:",
        "hist_dist_of": "Distribution of",
        "hist_age": "Age Distribution by Burnout Class",
        "segment_title": "Patterns by Gender, Experience, Role, and Company",
        "segment_compare": "Compare high burnout rate by dimension:",
        "high_rate_by": "High Burnout Rate by",
        "rate": "Rate (%)",
        "hier_map": "Hierarchical Burnout Intensity Map",
        "corr_title": "Correlations and Relationships",
        "corr_heatmap": "Correlation Heatmap",
        "axis_x": "X Axis",
        "axis_y": "Y Axis",
        "relation_between": "Relationship between",
        "temporal_title": "Temporal Heatmap and Trends",
        "temporal_heat_title": "Average Burnout Intensity by Weekday x Month",
        "trend_title": "Temporal Risk Trend",
        "high_burnout_pct": "High Burnout (%)",
        "avg_stress": "Average Stress",
        "about_title": "Methodology and Data Source",
        "about_info": "Customize brand, colors, and text to use this app as a commercial case study.",
    },
}


def t(lang: str, key: str) -> str:
    return I18N[lang][key]


inject_css()
df = load_data("dataset/developer_burnout_dataset_7000.csv")
lang = st.sidebar.selectbox("Idioma / Language", ["PT_BR", "EN_US"], index=0)
density_options = [t(lang, "density_comfortable"), t(lang, "density_compact")]
density_ui = st.sidebar.selectbox(t(lang, "density_label"), density_options, index=0)
density_mode = "compact" if density_ui == t(lang, "density_compact") else "comfortable"
inject_density_css(density_mode)

st.sidebar.header(t(lang, "sidebar_header"))
st.sidebar.caption(t(lang, "sidebar_caption"))

date_min = df["analysis_date"].min().date()
date_max = df["analysis_date"].max().date()
date_range = st.sidebar.date_input(
    t(lang, "period"),
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    date_start, date_end = date_range
else:
    date_start, date_end = date_min, date_max

age_min, age_max = st.sidebar.slider(t(lang, "age_range"), 18, 60, (22, 45))
hour_min, hour_max = st.sidebar.slider(t(lang, "work_hours"), 3.0, 16.0, (6.0, 12.0))
stress_min, stress_max = st.sidebar.slider(t(lang, "stress_level"), 0, 100, (20, 90))

all_label = t(lang, "all")
burnout_filter = st.sidebar.selectbox(
    t(lang, "burnout_class"),
    options=[all_label, "Low", "Medium", "High"],
)
gender_filter = st.sidebar.multiselect(
    t(lang, "gender_proxy"),
    options=sorted(df["gender_proxy"].dropna().unique().tolist()),
    default=sorted(df["gender_proxy"].dropna().unique().tolist()),
)
role_filter = st.sidebar.multiselect(
    t(lang, "job_role"),
    options=[str(v) for v in df["job_role"].dropna().unique().tolist()],
    default=[str(v) for v in df["job_role"].dropna().unique().tolist()],
)
company_filter = st.sidebar.multiselect(
    t(lang, "company_profile"),
    options=sorted(df["company_profile"].dropna().unique().tolist()),
    default=sorted(df["company_profile"].dropna().unique().tolist()),
)

work_df = df.copy()
work_df["job_role"] = work_df["job_role"].astype(str)
mask = (
    (work_df["analysis_date"].dt.date >= date_start)
    & (work_df["analysis_date"].dt.date <= date_end)
    & (work_df["age"].between(age_min, age_max, inclusive="both"))
    & (work_df["daily_work_hours"].between(hour_min, hour_max, inclusive="both"))
    & (work_df["stress_level"].between(stress_min, stress_max, inclusive="both"))
    & (work_df["gender_proxy"].isin(gender_filter))
    & (work_df["job_role"].isin(role_filter))
    & (work_df["company_profile"].isin(company_filter))
)
if burnout_filter != all_label:
    mask &= work_df["burnout_level"].eq(burnout_filter)

filtered = work_df.loc[mask].copy()

if filtered.empty:
    st.warning(t(lang, "empty_filter_warning"))
    st.stop()

high_burnout_rate = filtered["high_burnout"].mean() * 100
avg_stress = filtered["stress_level"].mean()
avg_hours = filtered["daily_work_hours"].mean()
avg_sleep = filtered["sleep_hours"].mean()

corr_candidates = ["daily_work_hours", "sleep_hours", "stress_level", "burnout_score", "exercise_hours", "screen_time"]
corr_series = filtered[corr_candidates].corr(numeric_only=True)["burnout_score"].drop("burnout_score")
main_risk_factor = corr_series.abs().sort_values(ascending=False).index[0]

tabs = st.tabs(
    [
        t(lang, "tab_exec"),
        t(lang, "tab_explore"),
        t(lang, "tab_segment"),
        t(lang, "tab_corr"),
        t(lang, "tab_temporal"),
        t(lang, "tab_about"),
    ]
)

with tabs[0]:
    st.markdown(
        f"""
        <div class="hero-card">
            <p class="hero-title">Burnout Analytics Suite</p>
            <p class="hero-sub">
                {t(lang, "hero_sub")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card(t(lang, "kpi_burnout"), f"{high_burnout_rate:.1f}%", t(lang, "kpi_burnout_sub"))
    with k2:
        kpi_card(t(lang, "kpi_stress"), f"{avg_stress:.1f}", t(lang, "kpi_stress_sub"))
    with k3:
        kpi_card(t(lang, "kpi_hours"), f"{avg_hours:.2f}h", t(lang, "kpi_hours_sub"))
    with k4:
        kpi_card(t(lang, "kpi_sleep"), f"{avg_sleep:.2f}h", t(lang, "kpi_sleep_sub"))

    c1, c2 = st.columns([1.1, 1.9])
    with c1:
        st.subheader(t(lang, "key_indicators"))
        st.markdown(f"- {t(lang, 'risk_factor')}: **{main_risk_factor}**")
        st.markdown(f"- {t(lang, 'records')}: **{len(filtered):,}**".replace(",", "."))
        st.markdown(f"- {t(lang, 'window')}: **{date_start} → {date_end}**")
        st.markdown(f"- {t(lang, 'exec_layer')}")
    with c2:
        burnout_dist = (
            filtered["burnout_level"]
            .value_counts(normalize=True)
            .rename_axis("burnout_level")
            .reset_index(name="percent")
        )
        fig_donut = px.pie(
            burnout_dist,
            names="burnout_level",
            values="percent",
            hole=0.55,
            title=t(lang, "burnout_distribution"),
            color="burnout_level",
            color_discrete_map={"Low": "#2dd4bf", "Medium": "#f59e0b", "High": "#ef4444"},
        )
        fig_donut.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_donut, use_container_width=True)

with tabs[1]:
    st.subheader(t(lang, "explore_title"))
    e1, e2 = st.columns([1.4, 1.6])
    with e1:
        st.dataframe(filtered.head(20), use_container_width=True, height=430)
    with e2:
        numeric = filtered.select_dtypes(include=[np.number]).columns.tolist()
        stats = (
            filtered[numeric]
            .agg(["mean", "median", "std"])
            .T.rename(columns={"mean": t(lang, "mean"), "median": t(lang, "median"), "std": t(lang, "std")})
            .round(2)
        )
        st.dataframe(stats, use_container_width=True, height=430)

    h1, h2 = st.columns(2)
    with h1:
        hist_feature = st.selectbox(
            t(lang, "hist_var"),
            ["stress_level", "daily_work_hours", "sleep_hours", "screen_time", "exercise_hours"],
        )
        fig_hist = px.histogram(
            filtered,
            x=hist_feature,
            nbins=35,
            color="burnout_level",
            marginal="box",
            barmode="overlay",
            opacity=0.75,
            color_discrete_map={"Low": "#2dd4bf", "Medium": "#f59e0b", "High": "#ef4444"},
            title=f"{t(lang, 'hist_dist_of')} {hist_feature}",
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    with h2:
        fig_age = px.histogram(
            filtered,
            x="age",
            nbins=24,
            color="burnout_level",
            title=t(lang, "hist_age"),
            color_discrete_map={"Low": "#2dd4bf", "Medium": "#f59e0b", "High": "#ef4444"},
        )
        st.plotly_chart(fig_age, use_container_width=True)

with tabs[2]:
    st.subheader(t(lang, "segment_title"))
    seg_col1, seg_col2 = st.columns(2)

    seg_dim = st.selectbox(
        t(lang, "segment_compare"),
        ["gender_proxy", "job_role", "company_profile", "age_group", "burnout_level"],
    )
    seg_df = (
        filtered.groupby(seg_dim, dropna=False)["high_burnout"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .reset_index()
    )
    fig_bar = px.bar(
        seg_df,
        x=seg_dim,
        y="high_burnout",
        color="high_burnout",
        title=f"{t(lang, 'high_rate_by')} {seg_dim}",
        labels={"high_burnout": t(lang, "rate")},
        color_continuous_scale="YlOrRd",
    )
    fig_bar.update_layout(coloraxis_showscale=False)
    seg_col1.plotly_chart(fig_bar, use_container_width=True)

    cross = (
        filtered.groupby(["job_role", "company_profile"], dropna=False)["burnout_score"]
        .mean()
        .reset_index()
    )
    fig_cross = px.treemap(
        cross,
        path=["company_profile", "job_role"],
        values="burnout_score",
        color="burnout_score",
        color_continuous_scale="RdYlGn_r",
        title=t(lang, "hier_map"),
    )
    seg_col2.plotly_chart(fig_cross, use_container_width=True)

with tabs[3]:
    st.subheader(t(lang, "corr_title"))
    c_heat, c_scatter = st.columns([1.1, 1.4])

    corr_cols = [
        "age",
        "experience_years",
        "daily_work_hours",
        "sleep_hours",
        "caffeine_intake",
        "bugs_per_day",
        "commits_per_day",
        "meetings_per_day",
        "screen_time",
        "exercise_hours",
        "stress_level",
        "burnout_score",
    ]
    corr_matrix = filtered[corr_cols].corr(numeric_only=True).round(2)
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title=t(lang, "corr_heatmap"),
    )
    c_heat.plotly_chart(fig_corr, use_container_width=True)

    x_var = c_scatter.selectbox(t(lang, "axis_x"), corr_cols[:-1], index=2)
    y_var = c_scatter.selectbox(t(lang, "axis_y"), corr_cols[:-1], index=10)
    fig_scatter = px.scatter(
        filtered,
        x=x_var,
        y=y_var,
        color="burnout_level",
        size="stress_level",
        hover_data=["age", "experience_years", "job_role", "company_profile"],
        opacity=0.72,
        title=f"{t(lang, 'relation_between')} {x_var} e {y_var}",
        color_discrete_map={"Low": "#2dd4bf", "Medium": "#f59e0b", "High": "#ef4444"},
    )
    c_scatter.plotly_chart(fig_scatter, use_container_width=True)

with tabs[4]:
    st.subheader(t(lang, "temporal_title"))
    t1, t2 = st.columns([1.15, 1.85])

    tmp = filtered.copy()
    tmp["month"] = tmp["analysis_date"].dt.month
    tmp["weekday"] = tmp["analysis_date"].dt.dayofweek
    if lang == "EN_US":
        weekday_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        month_map = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        ordered_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    else:
        weekday_map = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sab", 6: "Dom"}
        month_map = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }
        ordered_days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        ordered_months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    tmp["weekday_name"] = tmp["weekday"].map(weekday_map)
    tmp["month_name"] = tmp["month"].map(month_map)

    heat = tmp.pivot_table(
        values="burnout_score",
        index="weekday_name",
        columns="month_name",
        aggfunc="mean",
    )
    heat = heat.reindex(index=ordered_days, columns=ordered_months)

    fig_heat = px.imshow(
        heat,
        text_auto=".2f",
        color_continuous_scale="YlOrRd",
        aspect="auto",
        title=t(lang, "temporal_heat_title"),
    )
    t1.plotly_chart(fig_heat, use_container_width=True)

    monthly = (
        tmp.resample("ME", on="analysis_date")
        .agg(burnout_alto=("high_burnout", "mean"), estresse=("stress_level", "mean"))
        .reset_index()
    )
    fig_line = go.Figure()
    fig_line.add_trace(
        go.Scatter(
            x=monthly["analysis_date"],
            y=monthly["burnout_alto"] * 100,
            mode="lines+markers",
            name=t(lang, "high_burnout_pct"),
            line=dict(color="#ef4444", width=2),
        )
    )
    fig_line.add_trace(
        go.Scatter(
            x=monthly["analysis_date"],
            y=monthly["estresse"],
            mode="lines+markers",
            name=t(lang, "avg_stress"),
            line=dict(color="#4cc9f0", width=2),
            yaxis="y2",
        )
    )
    fig_line.update_layout(
        title=t(lang, "trend_title"),
        yaxis=dict(title=t(lang, "high_burnout_pct")),
        yaxis2=dict(title=t(lang, "avg_stress"), overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.12),
    )
    t2.plotly_chart(fig_line, use_container_width=True)

with tabs[5]:
    st.subheader(t(lang, "about_title"))
    st.markdown(
        """
        **Fonte / Source:** Dataset público do Kaggle (Developer Burnout Prediction Dataset - 7000 samples).  
        **Objetivo / Goal:** apoiar diagnósticos de burnout com foco em decisões gerenciais e ações preventivas.

        **Pipeline**
        - Ingestão e tipagem numérica com tratamento de valores ausentes.
        - Enriquecimento analítico para portfólio com:
          - eixo temporal sintético (`analysis_date`) para tendências;
          - `job_role` derivado por faixa de experiência;
          - `gender_proxy` e `company_profile` para segmentação executiva.
        - Cálculo de KPIs, estatísticas descritivas e correlações multivariadas.

        **Nota importante / Important note**
        - O dataset original não possui colunas explícitas de gênero, cargo textual e empresa nominal.
        - As dimensões adicionais são *proxies transparentes* para fins de demonstração de portfólio.
        """
    )
    st.info(t(lang, "about_info"))
