import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob, os

st.set_page_config(page_title="Climate Analytics", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:      #0b150d;
  --bg2:     #111e13;
  --bg3:     #172019;
  --card:    #131d14;
  --accent:  #4e9e6a;
  --text:    #e8f0e0;
  --muted:   #6e8870;
  --border:  #1e3022;
  --hot:     #d4845a;
  --cold:    #5a9ec8;
}

html, body, [class*="css"] {
  font-family: 'Syne', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1400px !important; }

section[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
  font-family: 'DM Mono', monospace !important;
  font-size: 10px !important; letter-spacing: 2px !important;
  text-transform: uppercase !important; color: var(--accent) !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}

.dash-header {
  border-left: 5px solid var(--accent);
  background: linear-gradient(135deg, var(--bg2) 0%, var(--bg) 100%);
  padding: 40px 36px 32px;
  margin: 0 -2rem 32px -2rem;
  border-bottom: 1px solid var(--border);
}
.dash-tag { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; color: var(--accent); text-transform: uppercase; margin-bottom: 12px; }
.dash-title { font-size: 42px; font-weight: 800; color: var(--text); line-height: 1.1; margin-bottom: 10px; }
.dash-title span { color: var(--accent); }
.dash-sub { font-size: 13px; color: var(--muted); line-height: 1.7; max-width: 600px; }

.kpi-row { display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
.kpi-card { flex: 1; min-width: 140px; background: var(--card); border: 1px solid var(--border); border-top: 3px solid var(--accent); border-radius: 10px; padding: 18px 20px; }
.kpi-value { font-family: 'DM Mono', monospace; font-size: 26px; color: var(--accent); margin-bottom: 4px; }
.kpi-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; }

.section-label { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; color: var(--accent); border-left: 3px solid var(--accent); padding-left: 12px; margin-bottom: 6px; text-transform: uppercase; }
.section-desc { font-size: 13px; color: var(--muted); margin-bottom: 24px; padding-left: 15px; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { background: var(--bg2) !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; padding: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; border-bottom: 3px solid transparent !important; color: var(--muted) !important; font-family: 'Syne', sans-serif !important; font-size: 13px !important; font-weight: 600 !important; padding: 14px 22px !important; border-radius: 0 !important; }
.stTabs [aria-selected="true"] { color: var(--accent) !important; border-bottom: 3px solid var(--accent) !important; background: transparent !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding-top: 24px !important; }

.stPlotlyChart { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; padding: 20px !important; margin-bottom: 18px !important; }

.stDataFrame { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }
.stDataFrame th { background: var(--bg3) !important; color: var(--accent) !important; font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; }
.stDataFrame td { color: var(--text) !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; }

.sidebar-divider { border: none; border-top: 1px solid var(--border); margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

PLOTLY_THEME = dict(
    paper_bgcolor="#131d14", plot_bgcolor="#131d14",
    font=dict(family="DM Mono, monospace", color="#6e8870", size=12),
    legend=dict(bgcolor="#111e13", bordercolor="#1e3022", borderwidth=1, font_color="#e8f0e0"),
    hoverlabel=dict(bgcolor="#111e13", bordercolor="#4e9e6a", font_color="#e8f0e0", font_family="DM Mono, monospace")
)
AXIS_STYLE = dict(gridcolor="#1e3022", linecolor="#1e3022", tickcolor="#6e8870",
                  title_font_color="#6e8870", tickfont=dict(color="#6e8870"))
PALETTE = ["#4e9e6a","#7ec89a","#5a9ec8","#9ea882","#d4845a","#a8c87e",
           "#6abca8","#c8a87e","#8e6ac8","#c8c87e","#6a9ec8","#c86a9e"]

def apply_theme(fig, height=420):
    fig.update_layout(height=height, margin=dict(l=20, r=20, t=30, b=20), **PLOTLY_THEME)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig

# Load data 
@st.cache_data
def load_data():
    for path in ["output/task4_climate_stats", "output/task2_avg_temp"]:
        files = glob.glob(os.path.join(path, "part-*.csv")) or \
                glob.glob(os.path.join(path, "*.csv"))
        if not files:
            continue
        df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
        df.columns = [c.lower() for c in df.columns]
        df = df.rename(columns={"average_temperature": "avg_temp"})
        for col in ["std_temp","min_temp","max_temp","name"]:
            if col not in df.columns:
                df[col] = np.nan
        df["station"]  = df["station"].astype(str)
        df["year"]     = df["year"].astype(int)
        df["avg_temp"] = pd.to_numeric(df["avg_temp"], errors="coerce")
        df["label"]    = df["name"].apply(
            lambda n: n.split(",")[0].strip() if pd.notna(n) else None
        ).fillna("Station " + df["station"])
        return df.dropna(subset=["avg_temp"])
    return None

df = load_data()
if df is None:
    st.error("No data found. Run task2.py or task4_prepare.py first.")
    st.stop()

# Header 
st.markdown("""
<div class="dash-header">
  <div class="dash-tag">GSOD · NOAA · Global Weather Stations</div>
  <div class="dash-title">Climate Analytics <span>Dashboard</span></div>
  <div class="dash-sub">Long-term temperature trends, station comparisons, variability analysis and extreme weather detection across global GSOD weather stations.</div>
</div>
""", unsafe_allow_html=True)

# Sidebar 
with st.sidebar:
    st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)

    all_years  = sorted(df["year"].unique())
    year_range = st.slider("Year Range",
        min_value=int(min(all_years)), max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years))))

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    all_labels  = sorted(df[["station","label"]].drop_duplicates()["label"].tolist())
    top_default = df.groupby("label")["avg_temp"].count().nlargest(8).index.tolist()

    selected_labels = st.multiselect("Stations",
        options=all_labels, default=sorted(top_default))

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:DM Mono,monospace;font-size:10px;color:#6e8870;letter-spacing:1px">'
        f'Total records: {len(df)}<br>Stations in dataset: {df["station"].nunique()}</div>',
        unsafe_allow_html=True)

if not selected_labels:
    st.warning("Select at least one station in the sidebar.")
    st.stop()

# Filter
label_to_station  = df[["station","label"]].drop_duplicates().set_index("label")["station"].to_dict()
selected_stations = [label_to_station[l] for l in selected_labels]
filtered = df[
    df["station"].isin(selected_stations) &
    df["year"].between(year_range[0], year_range[1])
].copy()

if filtered.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# KPI row
hottest     = filtered.loc[filtered["avg_temp"].idxmax()]
coldest     = filtered.loc[filtered["avg_temp"].idxmin()]
overall_avg = filtered["avg_temp"].mean()

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card"><div class="kpi-value">{filtered['station'].nunique()}</div><div class="kpi-label">Stations Selected</div></div>
  <div class="kpi-card"><div class="kpi-value">{year_range[0]}–{year_range[1]}</div><div class="kpi-label">Year Range</div></div>
  <div class="kpi-card"><div class="kpi-value">{overall_avg:.1f} °F</div><div class="kpi-label">Overall Avg Temp</div></div>
  <div class="kpi-card"><div class="kpi-value">{hottest['avg_temp']:.1f} °F</div><div class="kpi-label">Hottest · {hottest['label'][:22]} ({int(hottest['year'])})</div></div>
  <div class="kpi-card"><div class="kpi-value">{coldest['avg_temp']:.1f} °F</div><div class="kpi-label">Coldest · {coldest['label'][:22]} ({int(coldest['year'])})</div></div>
</div>
""", unsafe_allow_html=True)

# Tabs 
tab1, tab2, tab3, tab4 = st.tabs([
    "Long-Term Trends", "Station Comparison",
    "Temperature Variability", "Extreme Weather"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Long-Term Trends
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Long-Term Temperature Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Average annual temperature per station across the selected year range.</div>', unsafe_allow_html=True)

    t1 = filtered.copy()
    t1["year"] = t1["year"].astype(str)

    fig1 = px.line(t1.sort_values("year"), x="year", y="avg_temp", color="label",
                   markers=True, color_discrete_sequence=PALETTE,
                   labels={"year": "Year", "avg_temp": "Avg Temperature (°F)", "label": "Station"})
    fig1.update_traces(line_width=2, marker_size=7)
    apply_theme(fig1, 450)
    fig1.update_xaxes(type="category")
    st.plotly_chart(fig1, use_container_width=True)

    overall = filtered.groupby("year")["avg_temp"].mean().reset_index()
    overall["year"] = overall["year"].astype(str)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=overall["year"], y=overall["avg_temp"],
        fill="tozeroy", mode="lines+markers",
        line=dict(color="#4e9e6a", width=2.5),
        fillcolor="rgba(78,158,106,0.12)",
        marker=dict(color="#4e9e6a", size=8), name="Overall Mean"
    ))
    apply_theme(fig2, 300)
    fig2.update_xaxes(type="category")
    st.markdown('<div class="section-label" style="margin-top:8px">Overall Mean — All Selected Stations</div>', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Station Comparison
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Station Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Side-by-side temperature comparison across stations and years. The heatmap reveals spatial and temporal patterns at a glance.</div>', unsafe_allow_html=True)

    pivot = filtered.pivot_table(index="label", columns="year", values="avg_temp")
    pivot.columns = [str(y) for y in pivot.columns]

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values, x=list(pivot.columns), y=pivot.index.tolist(),
        colorscale=[[0.0,"#1a4a6a"],[0.35,"#2d7a5a"],[0.65,"#6aaa4a"],[0.85,"#c87a2a"],[1.0,"#c84a1a"]],
        colorbar=dict(title="°F", tickfont=dict(family="DM Mono, monospace", color="#6e8870")),
        hovertemplate="Station: %{y}<br>Year: %{x}<br>Temp: %{z:.1f} °F<extra></extra>",
        xgap=3, ygap=3
    ))
    fig_heat.update_layout(
        height=max(380, len(selected_labels) * 40 + 80),
        margin=dict(l=20, r=20, t=20, b=20), **PLOTLY_THEME
    )
    fig_heat.update_xaxes(type="category", **AXIS_STYLE)
    fig_heat.update_yaxes(**AXIS_STYLE)
    st.plotly_chart(fig_heat, use_container_width=True)

    latest_year = filtered["year"].max()
    latest = filtered[filtered["year"] == latest_year].sort_values("avg_temp")
    fig_bar = px.bar(latest, x="avg_temp", y="label", orientation="h",
                     color="avg_temp",
                     color_continuous_scale=["#1a4a6a","#2d7a5a","#6aaa4a","#c87a2a","#c84a1a"],
                     labels={"avg_temp": "Avg Temperature (°F)", "label": "Station"})
    fig_bar.update_coloraxes(showscale=False)
    apply_theme(fig_bar, max(350, len(selected_labels) * 36 + 80))
    st.markdown(f'<div class="section-label" style="margin-top:8px">Station Rankings — {latest_year}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Temperature Variability
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Temperature Variability</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Year-over-year temperature spread across stations. Warm-colored bars indicate years with anomalously high variability relative to the mean.</div>', unsafe_allow_html=True)

    has_std = filtered["std_temp"].notna().any()

    if has_std:
        t3 = filtered.copy()
        t3["year"] = t3["year"].astype(str)
        fig_std = px.line(t3.sort_values("year"), x="year", y="std_temp", color="label",
                          markers=True, color_discrete_sequence=PALETTE,
                          labels={"year": "Year", "std_temp": "Std Dev (°F)", "label": "Station"})
        fig_std.update_traces(line_width=2, marker_size=6)
        apply_theme(fig_std, 420)
        fig_std.update_xaxes(type="category")
        st.plotly_chart(fig_std, use_container_width=True)

    year_spread = (
        filtered.groupby("year")["avg_temp"]
        .agg(lambda x: x.max() - x.min()).reset_index()
        .rename(columns={"avg_temp": "spread"})
    )
    mean_s = year_spread["spread"].mean()
    std_s  = year_spread["spread"].std()
    year_spread["anomaly"] = (year_spread["spread"] - mean_s).abs() > std_s
    colors = ["#d4845a" if a else "#4e9e6a" for a in year_spread["anomaly"]]
    year_spread["year"] = year_spread["year"].astype(str)

    fig_spread = go.Figure(go.Bar(
        x=year_spread["year"], y=year_spread["spread"],
        marker_color=colors, marker_line_width=0,
        hovertemplate="Year: %{x}<br>Spread: %{y:.1f} °F<extra></extra>"
    ))
    fig_spread.add_hline(y=mean_s, line_dash="dash", line_color="#9ea882",
                         annotation_text=f"Mean {mean_s:.1f} °F",
                         annotation_font_color="#9ea882")
    apply_theme(fig_spread, 320)
    fig_spread.update_xaxes(type="category")
    fig_spread.update_yaxes(title="Temperature Spread (°F)")
    st.markdown('<div class="section-label" style="margin-top:8px">Annual Temperature Spread — Anomalous Years Highlighted</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_spread, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Extreme Weather
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-label">Extreme Weather Indicators</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Outlier detection via Z-score (threshold ± 1.5 standard deviations). Warm markers indicate unusually hot stations; cool markers indicate unusually cold.</div>', unsafe_allow_html=True)

    mean_t = filtered["avg_temp"].mean()
    std_t  = filtered["avg_temp"].std()
    t4 = filtered.copy()
    t4["z_score"]  = (t4["avg_temp"] - mean_t) / std_t
    t4["category"] = t4["z_score"].apply(
        lambda z: "Hot Extreme" if z > 1.5 else ("Cold Extreme" if z < -1.5 else "Normal")
    )
    t4["year"] = t4["year"].astype(str)

    fig_scatter = px.scatter(
        t4.sort_values("year"), x="year", y="avg_temp",
        color="category", symbol="category",
        color_discrete_map={"Hot Extreme":"#d4845a","Cold Extreme":"#5a9ec8","Normal":"#3a4a3c"},
        symbol_map={"Hot Extreme":"circle","Cold Extreme":"diamond","Normal":"circle-open"},
        hover_data={"label":True,"avg_temp":":.1f","z_score":":.2f","category":False},
        labels={"year":"Year","avg_temp":"Avg Temp (°F)","category":"Category"}
    )
    hot_thresh  = mean_t + 1.5 * std_t
    cold_thresh = mean_t - 1.5 * std_t
    fig_scatter.add_hline(y=mean_t, line_dash="dash", line_color="#9ea882",
                          annotation_text=f"Mean {mean_t:.1f} °F", annotation_font_color="#9ea882")
    fig_scatter.add_hline(y=hot_thresh, line_dash="dot", line_color="#d4845a",
                          annotation_text="Hot threshold", annotation_font_color="#d4845a")
    fig_scatter.add_hline(y=cold_thresh, line_dash="dot", line_color="#5a9ec8",
                          annotation_text="Cold threshold", annotation_font_color="#5a9ec8")
    fig_scatter.update_traces(marker_size=10)
    apply_theme(fig_scatter, 480)
    fig_scatter.update_xaxes(type="category", categoryorder="category ascending")
    st.plotly_chart(fig_scatter, use_container_width=True)

    extremes = t4[t4["category"] != "Normal"][
        ["label","year","avg_temp","z_score","category"]
    ].sort_values("z_score", ascending=False).rename(columns={
        "label":"Station","year":"Year",
        "avg_temp":"Avg Temp (°F)","z_score":"Z-Score","category":"Category"
    })

    if not extremes.empty:
        st.markdown(f'<div class="section-label" style="margin-top:8px">{len(extremes)} Extreme Data Points Identified</div>', unsafe_allow_html=True)
        st.dataframe(extremes.style.format({"Avg Temp (°F)":"{:.1f}","Z-Score":"{:.2f}"}),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No extreme outliers detected in the current selection.")

# Footer
st.markdown("""
<div style="text-align:center;padding:36px 0 16px;border-top:1px solid #1e3022;
     font-family:DM Mono,monospace;font-size:10px;color:#6e8870;
     letter-spacing:1px;margin-top:36px">
  NOAA Global Surface Summary of Day (GSOD) &nbsp;·&nbsp;
  2020–2022 &nbsp;·&nbsp; Task 4 — Climate Analytics Dashboard
</div>
""", unsafe_allow_html=True)