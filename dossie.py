import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Alveus™ · Dossiê Mercadológico 2026",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Theme / CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background:#0d0d0d; color:#ddd; }
  [data-testid="stHeader"] { background:#000; }
  [data-testid="stSidebar"] { background:#111; }
  h1,h2,h3 { color:#fff !important; }
  .metric-box {
    background:#111; border:1px solid #2a2a2a; border-radius:8px;
    padding:18px 14px; text-align:center;
  }
  .metric-val { font-size:2rem; font-weight:900; line-height:1; margin-bottom:4px; }
  .metric-lbl { font-size:0.7rem; font-weight:700; color:#888;
    text-transform:uppercase; letter-spacing:1px; }
  .lang-card {
    background:#1a1a1a; border-radius:8px; padding:14px;
    border-left:4px solid;
  }
  .section-label {
    font-size:0.7rem; font-weight:700; color:#555;
    text-transform:uppercase; letter-spacing:2px; margin-bottom:6px;
  }
  .quote-box {
    background:#1a1000; border:1px solid #ff8c00; border-radius:8px;
    padding:20px; text-align:center; margin-top:16px;
  }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────
LANG_META = {
    "pt": {"label":"Português", "color":"#1a7a42", "paises":9,  "falantes":"~280 mi"},
    "es": {"label":"Español",   "color":"#e07b00", "paises":20, "falantes":"~500 mi"},
    "fr": {"label":"Français",  "color":"#2255b0", "paises":29, "falantes":"~320 mi"},
    "it": {"label":"Italiano",  "color":"#c0392b", "paises":2,  "falantes":"~65 mi" },
}

COUNTRIES = [
    {"name":"Brasil",            "lang":"pt","pme":22.0, "flag":"🇧🇷","region":"América do Sul",   "ne":"Brazil"},
    {"name":"Portugal",          "lang":"pt","pme":1.3,  "flag":"🇵🇹","region":"Europa",            "ne":"Portugal"},
    {"name":"Angola",            "lang":"pt","pme":0.8,  "flag":"🇦🇴","region":"África",            "ne":"Angola"},
    {"name":"Moçambique",        "lang":"pt","pme":0.5,  "flag":"🇲🇿","region":"África",            "ne":"Mozambique"},
    {"name":"Cabo Verde",        "lang":"pt","pme":0.05, "flag":"🇨🇻","region":"África",            "ne":"Cape Verde"},
    {"name":"Guiné-Bissau",      "lang":"pt","pme":0.04, "flag":"🇬🇼","region":"África",            "ne":"Guinea-Bissau"},
    {"name":"Timor-Leste",       "lang":"pt","pme":0.03, "flag":"🇹🇱","region":"Ásia",             "ne":"Timor-Leste"},
    {"name":"Guiné Equatorial",  "lang":"pt","pme":0.03, "flag":"🇬🇶","region":"África",            "ne":"Equatorial Guinea"},
    {"name":"S. Tomé e Príncipe","lang":"pt","pme":0.02, "flag":"🇸🇹","region":"África",            "ne":"São Tomé and Príncipe"},
    {"name":"México",            "lang":"es","pme":13.0, "flag":"🇲🇽","region":"América do Norte",  "ne":"Mexico"},
    {"name":"Colômbia",          "lang":"es","pme":3.5,  "flag":"🇨🇴","region":"América do Sul",   "ne":"Colombia"},
    {"name":"Argentina",         "lang":"es","pme":3.0,  "flag":"🇦🇷","region":"América do Sul",   "ne":"Argentina"},
    {"name":"Espanha",           "lang":"es","pme":3.0,  "flag":"🇪🇸","region":"Europa",            "ne":"Spain"},
    {"name":"Peru",              "lang":"es","pme":2.5,  "flag":"🇵🇪","region":"América do Sul",   "ne":"Peru"},
    {"name":"Chile",             "lang":"es","pme":2.0,  "flag":"🇨🇱","region":"América do Sul",   "ne":"Chile"},
    {"name":"Venezuela",         "lang":"es","pme":1.5,  "flag":"🇻🇪","region":"América do Sul",   "ne":"Venezuela"},
    {"name":"Equador",           "lang":"es","pme":1.2,  "flag":"🇪🇨","region":"América do Sul",   "ne":"Ecuador"},
    {"name":"Guatemala",         "lang":"es","pme":0.9,  "flag":"🇬🇹","region":"América Central",  "ne":"Guatemala"},
    {"name":"Bolívia",           "lang":"es","pme":0.7,  "flag":"🇧🇴","region":"América do Sul",   "ne":"Bolivia"},
    {"name":"Cuba",              "lang":"es","pme":0.5,  "flag":"🇨🇺","region":"América Central",  "ne":"Cuba"},
    {"name":"Rep. Dominicana",   "lang":"es","pme":0.5,  "flag":"🇩🇴","region":"América Central",  "ne":"Dominican Rep."},
    {"name":"Honduras",          "lang":"es","pme":0.4,  "flag":"🇭🇳","region":"América Central",  "ne":"Honduras"},
    {"name":"Costa Rica",        "lang":"es","pme":0.4,  "flag":"🇨🇷","region":"América Central",  "ne":"Costa Rica"},
    {"name":"Paraguai",          "lang":"es","pme":0.35, "flag":"🇵🇾","region":"América do Sul",   "ne":"Paraguay"},
    {"name":"El Salvador",       "lang":"es","pme":0.3,  "flag":"🇸🇻","region":"América Central",  "ne":"El Salvador"},
    {"name":"Panamá",            "lang":"es","pme":0.3,  "flag":"🇵🇦","region":"América Central",  "ne":"Panama"},
    {"name":"Uruguai",           "lang":"es","pme":0.3,  "flag":"🇺🇾","region":"América do Sul",   "ne":"Uruguay"},
    {"name":"Nicarágua",         "lang":"es","pme":0.25, "flag":"🇳🇮","region":"América Central",  "ne":"Nicaragua"},
    {"name":"França",            "lang":"fr","pme":4.0,  "flag":"🇫🇷","region":"Europa",            "ne":"France"},
    {"name":"Rep. Dem. Congo",   "lang":"fr","pme":2.5,  "flag":"🇨🇩","region":"África",            "ne":"Dem. Rep. Congo"},
    {"name":"Marrocos",          "lang":"fr","pme":1.8,  "flag":"🇲🇦","region":"África",            "ne":"Morocco"},
    {"name":"Argélia",           "lang":"fr","pme":1.5,  "flag":"🇩🇿","region":"África",            "ne":"Algeria"},
    {"name":"Canadá",            "lang":"fr","pme":1.2,  "flag":"🇨🇦","region":"América do Norte",  "ne":"Canada"},
    {"name":"Bélgica",           "lang":"fr","pme":0.9,  "flag":"🇧🇪","region":"Europa",            "ne":"Belgium"},
    {"name":"Costa do Marfim",   "lang":"fr","pme":1.0,  "flag":"🇨🇮","region":"África",            "ne":"Ivory Coast"},
    {"name":"Camarões",          "lang":"fr","pme":0.8,  "flag":"🇨🇲","region":"África",            "ne":"Cameroon"},
    {"name":"Senegal",           "lang":"fr","pme":0.7,  "flag":"🇸🇳","region":"África",            "ne":"Senegal"},
    {"name":"Tunísia",           "lang":"fr","pme":0.7,  "flag":"🇹🇳","region":"África",            "ne":"Tunisia"},
    {"name":"Madagascar",        "lang":"fr","pme":0.6,  "flag":"🇲🇬","region":"África",            "ne":"Madagascar"},
    {"name":"Suíça",             "lang":"fr","pme":0.6,  "flag":"🇨🇭","region":"Europa",            "ne":"Switzerland"},
    {"name":"Mali",              "lang":"fr","pme":0.5,  "flag":"🇲🇱","region":"África",            "ne":"Mali"},
    {"name":"Burkina Faso",      "lang":"fr","pme":0.45, "flag":"🇧🇫","region":"África",            "ne":"Burkina Faso"},
    {"name":"Guiné",             "lang":"fr","pme":0.4,  "flag":"🇬🇳","region":"África",            "ne":"Guinea"},
    {"name":"Ruanda",            "lang":"fr","pme":0.35, "flag":"🇷🇼","region":"África",            "ne":"Rwanda"},
    {"name":"Níger",             "lang":"fr","pme":0.35, "flag":"🇳🇪","region":"África",            "ne":"Niger"},
    {"name":"Haiti",             "lang":"fr","pme":0.3,  "flag":"🇭🇹","region":"América Central",  "ne":"Haiti"},
    {"name":"Chade",             "lang":"fr","pme":0.3,  "flag":"🇹🇩","region":"África",            "ne":"Chad"},
    {"name":"Benin",             "lang":"fr","pme":0.3,  "flag":"🇧🇯","region":"África",            "ne":"Benin"},
    {"name":"Togo",              "lang":"fr","pme":0.25, "flag":"🇹🇬","region":"África",            "ne":"Togo"},
    {"name":"Congo",             "lang":"fr","pme":0.2,  "flag":"🇨🇬","region":"África",            "ne":"Republic of Congo"},
    {"name":"Burundi",           "lang":"fr","pme":0.2,  "flag":"🇧🇮","region":"África",            "ne":"Burundi"},
    {"name":"Rep. Centro-Afr.",  "lang":"fr","pme":0.15, "flag":"🇨🇫","region":"África",            "ne":"Central African Rep."},
    {"name":"Gabão",             "lang":"fr","pme":0.15, "flag":"🇬🇦","region":"África",            "ne":"Gabon"},
    {"name":"Luxemburgo",        "lang":"fr","pme":0.08, "flag":"🇱🇺","region":"Europa",            "ne":"Luxembourg"},
    {"name":"Comores",           "lang":"fr","pme":0.04, "flag":"🇰🇲","region":"África",            "ne":"Comoros"},
    {"name":"Djibuti",           "lang":"fr","pme":0.04, "flag":"🇩🇯","region":"África",            "ne":"Djibouti"},
    {"name":"Itália",            "lang":"it","pme":5.0,  "flag":"🇮🇹","region":"Europa",            "ne":"Italy"},
    {"name":"San Marino",        "lang":"it","pme":0.01, "flag":"🇸🇲","region":"Europa",            "ne":"San Marino"},
]

df = pd.DataFrame(COUNTRIES)
TOTAL = df["pme"].sum()
LANG_TOTALS = df.groupby("lang")["pme"].sum()

# ── Colors ────────────────────────────────────────────────────────────────
C_BG    = "#0d0d0d"
C_OCEAN = "#0b1220"
C_LAND  = "#161616"
C_BORDER= "#252525"
COLORS  = {k: v["color"] for k, v in LANG_META.items()}

# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#000;border-bottom:3px solid #ff8c00;
  padding:20px 32px;margin:-1rem -1rem 1.5rem;display:flex;
  align-items:center;justify-content:space-between;">
  <div>
    <div style="font-size:1.8rem;font-weight:900;color:#fff;letter-spacing:-1px;">
      Alve<span style="color:#ff8c00;">us</span>™
    </div>
    <div style="font-size:0.7rem;color:#444;text-transform:uppercase;
      letter-spacing:2px;margin-top:2px;">
      Dossiê Mercadológico 2026
    </div>
  </div>
  <div style="text-align:right;">
    <div style="font-size:1.5rem;font-weight:900;color:#ff8c00;">~125M PMEs</div>
    <div style="font-size:0.75rem;color:#666;">59 países · 4 idiomas</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["◈ Visão Geral", "🌍 Países", "📊 Gráficos", "🗺️ Mapa"])

# ══ TAB 1 — VISÃO GERAL ═══════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Indicadores-chave</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "~59",   "Países cobertos", "#ff8c00"),
        (c2, "4",     "Idiomas",          "#1a7a42"),
        (c3, "~125M", "PMEs totais",      "#2255b0"),
        (c4, "~81M",  "Endereçável",      "#c0392b"),
    ]
    for col, val, lbl, color in kpis:
        with col:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-val" style="color:{color};">{val}</div>
              <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Cobertura por idioma</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (k, m) in enumerate(LANG_META.items()):
        total = LANG_TOTALS[k]
        top = df[df["lang"]==k].sort_values("pme", ascending=False).iloc[0]
        with cols[i]:
            st.markdown(f"""
            <div class="lang-card" style="border-color:{m['color']};">
              <div style="font-weight:900;font-size:0.85rem;color:{m['color']};
                margin-bottom:4px;">{m['label']}</div>
              <div style="font-size:1.8rem;font-weight:900;color:#fff;
                line-height:1;margin-bottom:2px;">{total:.1f}M</div>
              <div style="font-size:0.7rem;color:#555;margin-bottom:10px;">
                PMEs estimadas</div>
              <div style="font-size:0.7rem;color:#666;">
                <span style="color:{m['color']};font-weight:700;">{m['paises']}</span>
                países · {m['falantes']}</div>
              <div style="font-size:0.7rem;color:#444;margin-top:4px;">
                Maior: {top['flag']} {top['name']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Funil de oportunidade</div>',
                unsafe_allow_html=True)

    funnel = [
        ("Total de PMEs nos 59 países", 124.8, "#333333"),
        ("Vendem a prazo (~65%)",        81.1,  "#555555"),
        ("Mercado endereçável Alveus™",  81.1,  "#ff8c00"),
    ]
    for label, val, color in funnel:
        pct = val / 124.8 * 100
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;
          margin-bottom:4px;align-items:center;">
          <span style="font-size:0.85rem;
            color:{'#ff8c00' if color=='#ff8c00' else '#ccc'};">{label}</span>
          <span style="font-size:1rem;font-weight:700;
            color:{'#ff8c00' if color=='#ff8c00' else '#ccc'};">{val}M</span>
        </div>
        <div style="background:#1a1a1a;border-radius:3px;height:8px;
          margin-bottom:14px;overflow:hidden;">
          <div style="width:{pct}%;height:100%;background:{color};
            border-radius:3px;"></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1a1000;border:1px solid #ff8c00;border-radius:8px;
      padding:14px;text-align:center;margin-top:8px;">
      <span style="font-size:0.9rem;color:#ff8c00;font-weight:700;">
        0,1% de penetração → ~81.000 assinantes
      </span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Projeções de penetração</div>',
                unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    projs = [
        (p1, "Conservador", "0,05%", "~40K",  "#555",    "Operação sustentável",  False),
        (p2, "Moderado",    "0,10%", "~80K",  "#ff8c00", "Crescimento acelerado", True),
        (p3, "Otimista",    "0,25%", "~200K", "#22a05a", "Liderança regional",    False),
    ]
    for col, cen, pct, ass, cor, perf, hi in projs:
        with col:
            border = "#ff8c00" if hi else "#2a2a2a"
            st.markdown(f"""
            <div style="background:#111;border:1px solid {border};
              border-radius:8px;padding:16px;text-align:center;">
              <div style="font-size:0.75rem;color:#666;margin-bottom:6px;">{cen}</div>
              <div style="font-size:1.8rem;font-weight:900;color:{cor};">{ass}</div>
              <div style="font-size:0.7rem;color:#555;">assinantes · {pct}</div>
              <div style="font-size:0.75rem;color:#444;margin-top:6px;">{perf}</div>
            </div>""", unsafe_allow_html=True)

# ══ TAB 2 — PAÍSES ════════════════════════════════════════════════════════
with tab2:
    col_f, col_s = st.columns([3, 1])
    with col_f:
        lang_filter = st.multiselect(
            "Filtrar por idioma",
            options=list(LANG_META.keys()),
            format_func=lambda k: LANG_META[k]["label"],
            default=list(LANG_META.keys()),
        )
    with col_s:
        sort_by = st.selectbox("Ordenar", ["Volume (↓)", "Nome (A-Z)"])

    filtered = df[df["lang"].isin(lang_filter)].copy()
    if sort_by == "Volume (↓)":
        filtered = filtered.sort_values("pme", ascending=False)
    else:
        filtered = filtered.sort_values("name")

    total_f = filtered["pme"].sum()
    st.markdown(f"""
    <div style="background:#111;border:1px solid #2a2a2a;border-radius:4px;
      padding:10px 16px;margin-bottom:12px;display:flex;gap:24px;">
      <span style="font-size:0.85rem;">
        <span style="color:#666;">Países: </span>
        <span style="color:#ff8c00;font-weight:700;">{len(filtered)}</span>
      </span>
      <span style="font-size:0.85rem;">
        <span style="color:#666;">PMEs: </span>
        <span style="color:#ff8c00;font-weight:700;">{total_f:.1f}M</span>
      </span>
    </div>""", unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        m = LANG_META[row["lang"]]
        bar_w = row["pme"] / 22 * 100
        val = f"{row['pme']:.1f}M" if row["pme"] >= 1 else f"{int(row['pme']*1000)}K"
        st.markdown(f"""
        <div style="background:#111;border:1px solid #1e1e1e;border-radius:4px;
          padding:10px 14px;margin-bottom:5px;display:flex;align-items:center;gap:10px;">
          <div style="font-size:1.2rem;width:28px;text-align:center;flex-shrink:0;">
            {row['flag']}</div>
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
              <span style="font-weight:700;font-size:0.9rem;color:#fff;">
                {row['name']}</span>
              <span style="font-size:0.65rem;font-weight:700;padding:2px 6px;
                border-radius:20px;background:{m['color']}22;color:{m['color']};
                border:1px solid {m['color']}55;">{m['label']}</span>
              <span style="font-size:0.7rem;color:#333;margin-left:auto;">
                {row['region']}</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
              <div style="flex:1;background:#1a1a1a;border-radius:2px;
                height:4px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;
                  background:{m['color']};border-radius:2px;"></div>
              </div>
              <span style="font-size:0.85rem;font-weight:700;color:{m['color']};
                min-width:48px;text-align:right;">{val}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══ TAB 3 — GRÁFICOS ══════════════════════════════════════════════════════
with tab3:
    BG = "#0d0d0d"

    # ── Bar chart: Top 15 ─────────────────────────────────────────────────
    st.markdown("**Top 15 países por volume de PMEs**")
    top15 = df.sort_values("pme", ascending=False).head(15)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    fig1.patch.set_facecolor(BG); ax1.set_facecolor("#111")
    bars = ax1.barh(
        [f"{r['flag']} {r['name']}" for _, r in top15.iterrows()],
        top15["pme"],
        color=[COLORS[r["lang"]] for _, r in top15.iterrows()],
        height=0.65
    )
    for bar, val in zip(bars, top15["pme"]):
        ax1.text(bar.get_width()+0.15, bar.get_y()+bar.get_height()/2,
            f"{val:.1f}M", va="center", color="#fff", fontsize=8.5,
            fontweight="bold")
    ax1.invert_yaxis()
    ax1.set_xlabel("Milhões de PMEs", color="#666", fontsize=9)
    ax1.tick_params(colors="#aaa", labelsize=9)
    for spine in ax1.spines.values(): spine.set_edgecolor("#222")
    ax1.grid(axis="x", color="#1a1a1a", linewidth=0.5)
    ax1.set_xlim(0, 26)
    plt.tight_layout(pad=1)
    st.pyplot(fig1, use_container_width=True)
    plt.close()

    st.markdown("<br>", unsafe_allow_html=True)

    gc1, gc2 = st.columns(2)

    # ── Pie ───────────────────────────────────────────────────────────────
    with gc1:
        st.markdown("**Distribuição por idioma**")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
        vals   = [LANG_TOTALS[k] for k in LANG_META]
        colors = [m["color"] for m in LANG_META.values()]
        labels = [f"{m['label']}\n{LANG_TOTALS[k]:.1f}M"
                  for k, m in LANG_META.items()]
        wedges, texts = ax2.pie(
            vals, labels=labels, colors=colors,
            startangle=140, pctdistance=0.75,
            wedgeprops={"edgecolor":"#0d0d0d","linewidth":2},
            textprops={"color":"#aaa","fontsize":8},
        )
        ax2.add_artist(plt.Circle((0,0), 0.55, color=BG))
        ax2.text(0, 0, f"{TOTAL:.0f}M", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#fff")
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close()

    # ── Lang summary bars ─────────────────────────────────────────────────
    with gc2:
        st.markdown("**PMEs por idioma**")
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor("#111")
        lang_names = [LANG_META[k]["label"] for k in LANG_META]
        lang_vals  = [LANG_TOTALS[k] for k in LANG_META]
        lang_colors= [LANG_META[k]["color"] for k in LANG_META]
        bars3 = ax3.barh(lang_names, lang_vals, color=lang_colors, height=0.5)
        for bar, val in zip(bars3, lang_vals):
            ax3.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                f"{val:.1f}M", va="center", color="#fff", fontsize=9,
                fontweight="bold")
        ax3.invert_yaxis()
        ax3.set_xlabel("Milhões de PMEs", color="#666", fontsize=9)
        ax3.tick_params(colors="#aaa", labelsize=10)
        for spine in ax3.spines.values(): spine.set_edgecolor("#222")
        ax3.grid(axis="x", color="#1a1a1a", linewidth=0.5)
        ax3.set_xlim(0, 62)
        plt.tight_layout(pad=1)
        st.pyplot(fig3, use_container_width=True)
        plt.close()

    # ── Projections ───────────────────────────────────────────────────────
    st.markdown("<br>**Projeções de penetração de mercado**")
    fig4, ax4 = plt.subplots(figsize=(10, 3))
    fig4.patch.set_facecolor(BG); ax4.set_facecolor("#111")
    scenarios = ["Conservador\n0,05%", "Moderado\n0,10%", "Otimista\n0,25%"]
    vals4     = [40, 80, 200]
    cols4     = ["#555555", "#ff8c00", "#22a05a"]
    bars4 = ax4.bar(scenarios, vals4, color=cols4, width=0.4,
                    edgecolor="#1a1a1a", linewidth=0.5)
    for bar, val in zip(bars4, vals4):
        ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2,
            f"~{val}K", ha="center", va="bottom", color="#fff",
            fontsize=10, fontweight="bold")
    ax4.set_ylabel("Assinantes (mil)", color="#666", fontsize=9)
    ax4.tick_params(colors="#aaa", labelsize=9)
    for spine in ax4.spines.values(): spine.set_edgecolor("#222")
    ax4.grid(axis="y", color="#1a1a1a", linewidth=0.5)
    ax4.set_ylim(0, 230)
    plt.tight_layout(pad=1)
    st.pyplot(fig4, use_container_width=True)
    plt.close()

# ══ TAB 4 — MAPA ══════════════════════════════════════════════════════════
with tab4:
    st.markdown("**Cobertura geográfica — países cobertos pelos 4 idiomas**")

    lang_sel = st.multiselect(
        "Filtrar idioma no mapa",
        options=list(LANG_META.keys()),
        format_func=lambda k: LANG_META[k]["label"],
        default=list(LANG_META.keys()),
        key="map_filter",
    )

    @st.cache_data
    def load_world():
        return gpd.read_file('/home/claude/ne_110m.geojson')

    try:
        world = load_world()

        ne_to_lang = {r["ne"]: r["lang"] for r in COUNTRIES}

        def color_country(name):
            lang = ne_to_lang.get(name)
            if lang and lang in lang_sel:
                return LANG_META[lang]["color"]
            return C_LAND

        world["clr"] = world["NAME_EN"].apply(color_country)
        world["pme"] = world["NAME_EN"].map(
            {r["ne"]: r["pme"] for r in COUNTRIES}
        ).fillna(0)

        C_PT = "#1a7a42"; C_ES = "#e07b00"; C_FR = "#2255b0"; C_IT = "#c0392b"

        fig_m, ax_m = plt.subplots(figsize=(14, 7))
        fig_m.patch.set_facecolor(C_BG); ax_m.set_facecolor(C_OCEAN)

        world.plot(ax=ax_m, color=world["clr"],
                   edgecolor=C_BORDER, linewidth=0.35)

        # Bubbles
        covered = world[world["pme"] > 0].copy()
        centroids = covered.geometry.centroid
        adjustments = {
            "Brazil":(0,-4),"France":(0,0),"Canada":(-12,0),
            "Argentina":(0,-2),"Mexico":(2,2),"Dem. Rep. Congo":(2,0),
        }
        max_pme = 22
        for idx, row in covered.iterrows():
            pme_val = row["pme"]
            if pme_val == 0: continue
            lang = ne_to_lang.get(row["NAME_EN"])
            if lang and lang not in lang_sel: continue
            cx = centroids[idx].x; cy = centroids[idx].y
            adj = adjustments.get(row["NAME_EN"], (0,0))
            cx += adj[0]; cy += adj[1]
            size = (pme_val/max_pme)**0.55 * 1400
            clr = LANG_META[lang]["color"] if lang else C_LAND
            ax_m.scatter(cx, cy, s=size, color=clr, alpha=0.3,
                         zorder=3, linewidths=0)
            ax_m.scatter(cx, cy, s=size*0.15, color=clr, alpha=0.9,
                         zorder=4, linewidths=0)
            if pme_val >= 0.5:
                lbl = f"{pme_val:.0f}M" if pme_val >= 1 else f"{pme_val*1000:.0f}K"
                ax_m.text(cx, cy+(size**0.5)*0.012+0.6, lbl,
                    ha="center", va="bottom", fontsize=7, color="white",
                    fontweight="bold", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.12", facecolor="#000",
                              edgecolor="none", alpha=0.6))

        legend_items = [
            mpatches.Patch(facecolor=LANG_META[k]["color"], edgecolor="#2a2a2a",
                label=f"{LANG_META[k]['label']}  ·  {LANG_META[k]['paises']} países  ·  {LANG_TOTALS[k]:.1f}M PMEs")
            for k in lang_sel if k in LANG_META
        ]
        leg = ax_m.legend(handles=legend_items, loc="lower left",
            bbox_to_anchor=(0.005, 0.03), frameon=True, framealpha=0.92,
            facecolor="#111", edgecolor="#2a2a2a", fontsize=9,
            labelcolor="#ccc", title="  Idioma · cobertura · PMEs",
            title_fontsize=9, borderpad=1, labelspacing=0.6)
        leg.get_title().set_color("#ff8c00")
        leg.get_title().set_fontweight("bold")

        ax_m.text(0.992, 0.035,
            f"  ~{sum(LANG_TOTALS[k] for k in lang_sel if k in LANG_TOTALS):.0f}M PMEs\n  selecionadas  ",
            transform=ax_m.transAxes, ha="right", va="bottom",
            fontsize=9, color="#ff8c00", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#111",
                      edgecolor="#ff8c00", linewidth=1))

        ax_m.set_axis_off()
        ax_m.set_xlim(-170, 170); ax_m.set_ylim(-60, 82)
        plt.tight_layout(pad=0.3)
        st.pyplot(fig_m, use_container_width=True)
        plt.close()

    except Exception as e:
        st.error(f"Erro ao carregar mapa: {e}")
        st.info("Certifique-se de que o arquivo ne_110m.geojson está disponível.")

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="quote-box">
  <div style="font-size:1rem;font-weight:700;color:#ff8c00;
    font-style:italic;line-height:1.6;margin-bottom:8px;">
    "O Alveus™ não compete com ERPs.<br>
    Compete com o caderninho, a planilha e o WhatsApp.<br>
    Em 59 países."
  </div>
  <div style="font-size:0.7rem;color:#444;margin-top:8px;">
    Plataforma Alveus™ · Dossiê Mercadológico 2026
  </div>
</div>
""", unsafe_allow_html=True)
