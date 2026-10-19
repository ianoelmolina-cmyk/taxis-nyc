import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data(ttl=3600)
def llamar_api(ruta, **params):
    r = requests.get(f"{st.secrets['API_URL']}{ruta}", params=params, timeout=90)
    r.raise_for_status()
    return r.json()


st.title("Pronóstico de demanda")

try:
    with st.status("Conectando con la API...") as estado:
        info = llamar_api("/info")
        estado.update(label="API conectada", state="complete")
except requests.RequestException as e:
    st.error("Lo lamentamos! No hemos podido ejecutar tu consulta")       # tu mensaje para la gerente
    st.caption(f"Detalle: {e}")
    st.stop()

# 1. Selectores, armados con lo que devolvió /info
zonas = {z["id"]: f'{z["nombre"]} ({z["distrito"]})' for z in info["zonas"]}
zona_id = st.selectbox("Zona", options=list(zonas.keys()), format_func=lambda i: zonas[i])
fecha = st.segmented_control("Fecha", info["fechas"], default=info["fechas"][0])

if not fecha:
    st.stop()

# 2. Pedir el pronóstico (con su propio try/except)
try:
    datos = llamar_api("/pronostico", zona_id=zona_id, fecha=fecha)
except requests.RequestException as e:
    st.error("Lo sentimos!Pero quizá hayas ingresado mal los datos")
    st.caption(f"Detalle: {e}")
    st.stop()

# 3. De la respuesta a una tabla
df = pd.DataFrame(datos["horas"])
for c in ["p10", "p50", "p90"]:
    df[c] = df["cuantiles"].apply(lambda q: q[c])


if df["real"].isna().all(): st.info("No existen datos reales para un pronóstico")
# 4. El gráfico
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["hora"], y=df["p90"], line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=df["hora"], y=df["p10"], fill="tonexty", line=dict(width=0), name="Rango 10%-90%"))
fig.add_trace(go.Scatter(x=df["hora"], y=df["p50"], name="Pronóstico (mediana)"))
fig.add_trace(go.Scatter(x=df["hora"], y=df["hace_una_semana"], name="Hace una semana", line=dict(dash="dot")))
fig.add_trace(go.Scatter(x=df["hora"], y=df["real"], mode="markers", name="Real"))
st.plotly_chart(fig, use_container_width=True)