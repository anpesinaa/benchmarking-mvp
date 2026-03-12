import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="PROBOCA | Benchmarking de Proveedores", layout="wide")

PROBOCA_RED = "#E10600"
DARK_GRAY = "#2E2E2E"
MID_GRAY = "#6B6B6B"
LIGHT_GRAY = "#BDBDBD"
GRID_GRAY = "#E6E6E6"

st.markdown(
    f"""
    <style>
      .block-container {{
        padding-top: 4rem !important;
        padding-left: 2.2rem !important;
        padding-right: 2.2rem !important;
      }}
      h2, h3 {{ margin-top: 1.1rem !important; }}
      /* Tarjetas (metrics) estilo ejecutivo */
      div[data-testid="stMetric"] {{
        border: 1px solid rgba(0,0,0,0.08);
        padding: 16px 16px;
        border-radius: 16px;
        background: white;
      }}
      section[data-testid="stSidebar"] {{
        border-right: 1px solid rgba(0,0,0,0.06);
      }}
      .proboca-title {{
        font-size: 28px;
        font-weight: 850;
        margin: 0;
      }}
      .proboca-sub {{
        color: rgba(0,0,0,0.58);
        margin-top: 0.15rem;
        margin-bottom: 1rem;
      }}
      .pill {{
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(0,0,0,0.10);
        font-size: 12px;
        color: rgba(0,0,0,0.65);
        margin-right: 8px;
      }}
      .accent {{
        border-left: 6px solid {PROBOCA_RED};
        padding-left: 12px;
        margin-bottom: 0.75rem;
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# diccionario para predefinir pesos y kpi's 
CONFIG = {
    "transporte": {
        "weights": {"operativo": 0.60, "economico": 0.30, "calidad": 0.10},
        "kpis": {
            "puntualidad_pct": {"higher": True,  "block": "operativo", "label": "Puntualidad (%)"},
            "tasa_danos_pct": {"higher": False, "block": "operativo", "label": "Daños (%)"},
            "ventana_horaria_pct": {"higher": True, "block": "operativo", "label": "Ventana horaria (%)"},
            "costo_por_envio": {"higher": False, "block": "economico", "label": "Costo por envío"},
            "variacion_tarifaria_pct": {"higher": False, "block": "economico", "label": "Variación tarifaria (%)"},
            "desviacion_cotizacion_pct": {"higher": False, "block": "economico", "label": "Desviación vs cotización (%)"},
            "rapidez_respuesta_1a5": {"higher": True, "block": "calidad", "label": "Rapidez respuesta (1–5)"},
            "comunicacion_1a5": {"higher": True, "block": "calidad", "label": "Comunicación (1–5)"},
        }
    },
    "agencia_aduanal_mx": {
        "weights": {"operativo": 0.60, "economico": 0.30, "calidad": 0.10},
        "kpis": {
            "exactitud_documental_pct": {"higher": True,  "block": "operativo", "label": "Exactitud documental (%)"},
            "tiempo_liberacion_dias": {"higher": False, "block": "operativo", "label": "Tiempo liberación (días)"},
            "incidencias_regulatorias_pct": {"higher": False, "block": "operativo", "label": "Incidencias regulatorias (%)"},
            "coste_por_operacion": {"higher": False, "block": "economico", "label": "Coste por operación"},
            "multas_recargos": {"higher": False, "block": "economico", "label": "Multas/recargos"},
            "asesoria_1a5": {"higher": True, "block": "calidad", "label": "Asesoría (1–5)"},
            "rapidez_gestion_doc_1a5": {"higher": True, "block": "calidad", "label": "Rapidez gestión doc (1–5)"},
        }
    },
    "agencia_logistica": {
        "weights": {"operativo": 0.60, "economico": 0.30, "calidad": 0.10},
        "kpis": {
            "otd_pct": {"higher": True,  "block": "operativo", "label": "On-time delivery (%)"},
            "variabilidad_transito_dias": {"higher": False, "block": "operativo", "label": "Variabilidad tránsito (días)"},
            "incidencias_logisticas_pct": {"higher": False, "block": "operativo", "label": "Incidencias logísticas (%)"},
            "desviacion_presupuestaria_pct": {"higher": False, "block": "economico", "label": "Desviación presupuestaria (%)"},
            "visibilidad_1a5": {"higher": True, "block": "calidad", "label": "Visibilidad (1–5)"},
            "proactividad_1a5": {"higher": True, "block": "calidad", "label": "Proactividad (1–5)"},
        }
    },
    "broker": {
        "weights": {"operativo": 0.60, "economico": 0.30, "calidad": 0.10},
        "kpis": {
            "ahorro_generado_pct": {"higher": True,  "block": "operativo", "label": "Ahorro generado (%)"},
            "estabilidad_condiciones_1a5": {"higher": True, "block": "operativo", "label": "Estabilidad (1–5)"},
            "transparencia_comisiones_1a5": {"higher": True, "block": "economico", "label": "Transparencia (1–5)"},
            "variabilidad_tarifas_pct": {"higher": False, "block": "economico", "label": "Variabilidad tarifas (%)"},
            "negociacion_1a5": {"higher": True, "block": "calidad", "label": "Negociación (1–5)"},
            "confianza_1a5": {"higher": True, "block": "calidad", "label": "Confianza (1–5)"},
        }
    },
    "warehousing": {
        "weights": {"operativo": 0.60, "economico": 0.25, "calidad": 0.15},
        "kpis": {
            "exactitud_inventario_pct": {"higher": True,  "block": "operativo", "label": "Exactitud inventario (%)"},
            "tiempo_preparacion_horas": {"higher": False, "block": "operativo", "label": "Prep. pedidos (horas)"},
            "tasa_errores_pct": {"higher": False, "block": "operativo", "label": "Errores (%)"},
            "costo_almacenamiento": {"higher": False, "block": "economico", "label": "Costo almacenamiento"},
            "costo_manejo": {"higher": False, "block": "economico", "label": "Costo manejo"},
            "coordinacion_1a5": {"higher": True, "block": "calidad", "label": "Coordinación (1–5)"},
            "flexibilidad_1a5": {"higher": True, "block": "calidad", "label": "Flexibilidad (1–5)"},
        }
    },
    "carriers": {
        "weights": {"operativo": 0.60, "economico": 0.25, "calidad": 0.15},
        "kpis": {
            "on_time_pct": {"higher": True,  "block": "operativo", "label": "On-time (%)"},
            "cancelaciones_rollovers_pct": {"higher": False, "block": "operativo", "label": "Cancelaciones/Rollover (%)"},
            "estabilidad_tarifaria_1a5": {"higher": True, "block": "economico", "label": "Estabilidad tarifaria (1–5)"},
            "recargos_inesperados": {"higher": False, "block": "economico", "label": "Recargos inesperados"},
            "gestion_espacio_1a5": {"higher": True, "block": "calidad", "label": "Gestión espacio (1–5)"},
            "soporte_operativo_1a5": {"higher": True, "block": "calidad", "label": "Soporte operativo (1–5)"},
        }
    },
}

# Para estética de los textos desde la base de datos 
def pretty_text(s: str) -> str:
    s = s.replace("_", " ").strip()
    s = s.replace("Mx", "MX").replace("Usa", "USA")
    return s.title().replace("Mx", "MX").replace("Usa", "USA")

# min-max scaling para unificar escalas en los KPI's
def minmax_0_100(s: pd.Series, higher_is_better: bool) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    mn, mx = s.min(), s.max()
    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series([100.0] * len(s), index=s.index)
    scaled = (s - mn) / (mx - mn) * 100.0
    return scaled if higher_is_better else (100.0 - scaled)

# taransforma cualquier número en un valor tipo curva 
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))

# sirve para detectar un nivel de riesgo en cada categoría 
def risk_score_from_blocks(operativo: float, economico: float, calidad: float) -> float:
    op_bad = (100 - operativo) / 100
    ca_bad = (100 - calidad) / 100
    ec_bad = (100 - economico) / 100
    raw = (0.55 * op_bad) + (0.30 * ca_bad) + (0.15 * ec_bad)
    prob = sigmoid((raw - 0.35) * 8)
    return float(np.clip(prob * 100, 0, 100))

# hace un nivel de riesgo según parámetros dados
def risk_label(x: float) -> str:
    if x >= 70: return "Alto"
    if x >= 40: return "Medio"
    return "Bajo"

# lectura del csv actual
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


st.sidebar.markdown("### PROBOCA")
st.sidebar.caption("Benchmarking automatizado de proveedores")

data_file = "data_mvp.csv"
df = load_data(data_file)

# categorías 
cats = sorted(df["category"].dropna().unique())
cat_labels = {c: pretty_text(c) for c in cats}

category = st.sidebar.selectbox(
    "Categoría",
    options=cats,
    format_func=lambda c: cat_labels.get(c, c),
)

# umbral por el que se consideraría empate (desepata por calidad)
tie_threshold = st.sidebar.slider("Umbral de empate", 0.0, 10.0, 3.0, 1.0)


with st.sidebar.expander("Ajustes de pesos (what-if)", expanded=False):
    w_op = st.slider("Operativo", 0.0, 1.0, CONFIG[category]["weights"]["operativo"], 0.05)
    w_ec = st.slider("Económico", 0.0, 1.0, CONFIG[category]["weights"]["economico"], 0.05)
    w_ca = st.slider("Calidad", 0.0, 1.0, CONFIG[category]["weights"]["calidad"], 0.05)

# hace una normalización para que la suma de pesos de 1 siempre 
wsum = w_op + w_ec + w_ca
w_op, w_ec, w_ca = (0.55, 0.30, 0.15) if wsum == 0 else (w_op/wsum, w_ec/wsum, w_ca/wsum)

# muestra último mes disponible 
months = sorted(df["month"].dropna().unique())
month = months[-1] 


st.markdown(
    f"""
    <div class="accent">
      <div class="proboca-title">Selección óptima de proveedores</div>
      <div class="proboca-sub">Comparación por categoría con score multicriterio y riesgo operativo.</div>
      <span class="pill">Categoría: <b>{cat_labels.get(category, category)}</b></span>
      <span class="pill">Periodo: <b>{month}</b></span>
    </div>
    """,
    unsafe_allow_html=True
)

cfg = CONFIG[category]
kpis_cfg = cfg["kpis"]

sub = df[(df["category"] == category) & (df["month"] == month)].copy()

# score 

# normaliza de 0 a 100 para poder mezclar columnas (que todos queden en la misma escala)
for kpi, meta in kpis_cfg.items():
    sub[f"{kpi}__score"] = minmax_0_100(sub[kpi], meta["higher"])

# promedia el score por bloque 
for block in ["operativo", "economico", "calidad"]:
    block_cols = [f"{k}__score" for k, m in kpis_cfg.items() if m["block"] == block]
    sub[f"{block}_score"] = sub[block_cols].mean(axis=1)

# saca score total con los pesos asignados 
sub["total_score"] = sub["operativo_score"] * w_op + sub["economico_score"] * w_ec + sub["calidad_score"] * w_ca
# calcula riesgos y los interpreta 
sub["riesgo_pct"] = sub.apply(lambda r: risk_score_from_blocks(r["operativo_score"], r["economico_score"], r["calidad_score"]), axis=1)
sub["riesgo_nivel"] = sub["riesgo_pct"].apply(risk_label)

# ordenar por score para el ranking
sub = sub.sort_values("total_score", ascending=False).reset_index(drop=True)
sub["rank"] = sub.index + 1

# toma el primer y segundo del ranking 
top = sub.iloc[0]
second = sub.iloc[1] if len(sub) > 1 else None

c1, c2, c3, c4 = st.columns([1.6, 1, 1, 1])
c1.metric("Recomendación", f"#{int(top['rank'])} {top['provider']}")
c2.metric("Score total", f"{top['total_score']:.1f}/100")
c3.metric("Riesgo", f"{top['riesgo_nivel']} ({top['riesgo_pct']:.0f}%)")
c4.metric("Calidad", f"{top['calidad_score']:.1f}/100")

# Mensaje de empate 
if second is not None:
    diff = float(top["total_score"] - second["total_score"])
    if diff <= tie_threshold:
        winner = top["provider"] if top["calidad_score"] >= second["calidad_score"] else second["provider"]
        st.warning(
            f"Empate técnico ({diff:.2f} ≤ {tie_threshold}). "
            f"Desempate sugerido por **Calidad** → **{winner}**."
        )

st.markdown("---")


left, right = st.columns([1.25, 1])

with left:
    st.subheader("Ranking (Score total)")
    # === CAMBIO COLORES: top en rojo, resto en gris ===
    sub_plot = sub.copy()
    top_name = sub_plot.loc[0, "provider"]
    sub_plot["highlight"] = np.where(sub_plot["provider"] == top_name, "Top", "Resto")

    fig = px.bar(
        sub_plot,
        x="provider",
        y="total_score",
        text="total_score",
        color="highlight",
        color_discrete_map={"Top": PROBOCA_RED, "Resto": LIGHT_GRAY},
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", cliponaxis=False)
    fig.update_layout(height=380, yaxis_title="Score (0–100)", xaxis_title="", margin=dict(t=10, r=10, b=40, l=40))
    # === CAMBIO COLORES: fondo y grid en gris (no azul) ===
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_GRAY),
        yaxis=dict(showgrid=True, gridcolor=GRID_GRAY, zeroline=False),
        xaxis=dict(showgrid=False),
        legend=dict(title="", font=dict(color=DARK_GRAY)),
    )
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader("Desglose por bloques")
    melt = sub[["provider", "operativo_score", "economico_score", "calidad_score"]].melt(
        id_vars=["provider"], var_name="bloque", value_name="score"
    )
    melt["bloque"] = melt["bloque"].str.replace("_score", "", regex=False).str.capitalize()

    # === CAMBIO COLORES: operativo rojo, económico gris oscuro, calidad gris ===
    fig2 = px.bar(
        melt,
        x="provider",
        y="score",
        color="bloque",
        barmode="group",
        color_discrete_map={
            "Operativo": PROBOCA_RED,
            "Economico": DARK_GRAY,
            "Calidad": MID_GRAY,
        },
    )
    fig2.update_layout(height=380, yaxis_title="Score (0–100)", xaxis_title="", margin=dict(t=10, r=10, b=40, l=40))
    # === CAMBIO COLORES: fondo y grid en gris (no azul) ===
    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=DARK_GRAY),
        yaxis=dict(showgrid=True, gridcolor=GRID_GRAY, zeroline=False),
        xaxis=dict(showgrid=False),
        legend=dict(title="", font=dict(color=DARK_GRAY)),
    )
    st.plotly_chart(fig2, width='stretch')


st.subheader("Tabla ejecutiva")
tabla = sub[["rank", "provider", "total_score", "operativo_score", "economico_score", "calidad_score", "riesgo_pct", "riesgo_nivel"]].copy()
tabla.columns = ["Ranking", "Proveedor", "Score total", "Operativo", "Económico", "Calidad", "Riesgo (%)", "Nivel de riesgo"]
st.dataframe(tabla, width='stretch', hide_index=True)

csv_out = sub.to_csv(index=False).encode("utf-8")
st.download_button(
    "Descargar ranking (CSV)",
    data=csv_out,
    file_name=f"ranking_{category}_{month}.csv",
    mime="text/csv"
)

# ver los kpi's originales 
with st.expander("Ver KPIs (detalle)", expanded=False):
    cols_show = ["provider"] + list(kpis_cfg.keys())
    detalle = sub[cols_show].copy()
    detalle = detalle.rename(columns={k: v.get("label", k) for k, v in kpis_cfg.items()})
    detalle = detalle.rename(columns={"provider": "Proveedor"})
    st.dataframe(detalle, width='stretch' , hide_index=True)