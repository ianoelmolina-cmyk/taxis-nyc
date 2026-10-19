from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def cargar():
    ruta = Path(__file__).parent.parent / "data" / "zonas_segmentadas.csv"
    return pd.read_csv(ruta)

df = cargar()

st.title("Segmentación de zonas")

# 1. Filtro de grupos con botones
grupos = sorted(df["nombre_grupo"].unique())
elegidos = st.pills("Grupos", grupos, selection_mode="multi", default=grupos)
dff = df[ df["nombre_grupo"].isin(elegidos) ]

# 2. Una tarjeta con borde por grupo
cols = st.columns(len(grupos))
for col, g in zip(cols, grupos):
    with col.container(border=True):
        st.badge(g)
        sub = df[ df["nombre_grupo"] == g ]
        st.metric("Zonas", len(sub))
        st.caption(f"{sub['viajes_dia'].mean():.0f} viajes al día · {sub['dist_mediana'].mean():.1f} millas")

# 3. Gráfico PCA con selección de puntos
fig = px.scatter(dff, x="pc1", y="pc2", color="nombre_grupo",
                 hover_name="Zone", custom_data=["LocationID"], labels={"pc1": "Componente 1 (38.8%)", "pc2": "Componente 2 (27.1%)"})
evento = st.plotly_chart(fig, on_select="rerun", selection_mode=("points", "box", "lasso"))

# 4. Tabla de detalle (todas las zonas filtradas, o solo las seleccionadas)
puntos = evento.selection.points
if puntos:
    ids = [p["customdata"][0] for p in puntos]
    detalle = dff[ dff["LocationID"].isin(ids) ]
else:
    detalle = dff

st.dataframe(detalle[["Zone", "Borough", "nombre_grupo", "viajes_dia", "dist_mediana", "propina_mediana", "pct_22_5"]], column_config={
    "pct_22_5": st.column_config.ProgressColumn("Viajes de noche", min_value=0, max_value=1, format="percent"),
    "viajes_dia": st.column_config.NumberColumn("Viajes al día", format="%.0f")
}, hide_index=True)