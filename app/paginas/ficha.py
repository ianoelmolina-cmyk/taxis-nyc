import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def cargar():
    ruta = Path(__file__).parent.parent / "data" / "ficha.json"
    return json.loads(ruta.read_text(encoding="utf-8"))

f = cargar()

st.title("Ficha del modelo")

# 1. Para qué sirve
with st.container(border=True):
    st.subheader("Para qué sirve")
    st.write(f"Pronóstica la cantidad de viajes en taxis amarillos por hora y 58 zonas de NYC.")

# 2. Qué tan bien funciona
st.subheader("Qué tan bien funciona")
c1, c2, c3 = st.columns(3)
c1.metric("Error del modelo", f"{f['mae_modelo']:.1f} viajes/hora", border=True)
c2.metric("Cobertura del rango 10%-90%", f"{f['cobertura']:.1%}", border=True)
c3.metric("Horas-zona evaluadas",f"{f['horas_evaluadas']}" , border=True)

reglas = pd.DataFrame({"regla": ["Modelo(mediana)", "Igual que hace una semana", "Igual que ayer"], 
                       "error": [f["mae_modelo"], f["mae_semana"], f["mae_ayer"]]})
st.plotly_chart(px.bar(reglas, x="error", y="regla", orientation="h"), use_container_width=True)
st.write(f"el modelo (11.97) queda casi igual que “igual que hace una semana” (11.88), una diferencia de unos 0.09 viajes por hora, "
"y mucho mejor que “igual que ayer” (21.29). Su valor está en el rango de incertidumbre, que la regla simple no da, "
"y ese rango cubre cerca del 90% de los casos, más del 80% prometido.")

# 3. Dónde se equivoca más
st.subheader("Dónde se equivoca más")
st.plotly_chart(px.bar(pd.DataFrame(f["error_por_grupo"]), x="mean", y="nombre_grupo", orientation="h"), use_container_width=True)
st.dataframe(pd.DataFrame(f["zonas_mas_error"]), hide_index=True)

# 4. Limitaciones y usos no recomendados
st.subheader("Limitaciones")
st.markdown(f"Para la preparación del modelo se usaron datos del mes de Enero, correspondiente a la estación de invierno, lo que podría "
            "derivar en una mayor incertidumbre en otras estaciones. La calibración mostró que los cuantiles de las colas eran más anchos de lo necesario " 
            "(p10 = 0.07 y p90 = 0.96), esto significa que alguien que use p90 estaría enviando más taxis de los necesarios por zona")
st.subheader("Usos no recomendados")
st.markdown(
    "- **1. Recortar el servicio en barrios con pocos viajes de taxi amarillo.** "
    "El modelo solo pronostica 58 de las 265 zonas de la ciudad (las que superan "
    "los 3,000 viajes en enero) y mide viajes de taxi amarillo, no la necesidad de "
    "transporte de las personas. Poca demanda de taxi amarillo no significa poca "
    "necesidad de transporte. Los más perjudicados serían los residentes de esos "
    "barrios, que quedarían con menos opciones para moverse."
    "- **2. Pronosticar más de 1 día** "
    "El modelo hace su pronóstico teniendo en cuenta datos de días anteriores, "
    "y al tener una predicción de un segundo día el dato correspondienta a lag_24 no existiría. "
    "Haciendo que el pronóstico sea errado o menos exacto."
)